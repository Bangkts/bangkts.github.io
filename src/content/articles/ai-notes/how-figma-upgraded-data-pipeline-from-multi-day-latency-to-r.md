---
title: "How Figma Upgraded Data Pipeline from Multi-Day Latency to Real-Time"
category: "AI Notes"
categoryOrder: 3
order: 5
source: "https://blog.bytebytego.com/p/how-figma-upgraded-data-pipeline"
sourceLabel: "ByteByteGo"
---

Underneath every review sits a purpose-built, independent context engine. It’s the layer that decides what the agent actually sees before a single token of generation happens.

Purpose-built because code review demands a different context than chat or autocomplete: placing the relevant context fragments assembled for each review.

The engine assembles inputs across four planes:

*   Sandbox. Cloned repo, dependency analysis, multi-repo context and linters/SAST (ESLint, Semgrep) running on the change.

*   Review instructions. Your coding guidelines, AGENTS.md, path, and AST-scoped rules, tone, and learnings from past reviews.

*   Integrations. MCP tools, issue trackers (Jira, Linear), CI/CD failures, and web search.

*   LLMs. Routing across OpenAI and Anthropic.

[Try For Free](https://go.bytebytego.com/Coderabbit_051226)

* * *

In 2020, Figma’s data synchronization architecture was about five lines of logic. A cron job ran once a day, queried every row from a database table, dumped it into S3, and loaded it into Snowflake.

It was straightforward, easy to reason about, and it worked.

Three years later, that same simplicity was costing Figma millions of dollars a year and leaving their analytics team looking at data that was already days old by the time they could query it.

For reference, Figma is a collaborative design platform where teams create, prototype, and iterate on user interfaces together in real time. If you’ve used a modern app or website, there’s a high chance the screens were designed in Figma or that Figma was part of the workflow.

Since its early days, the product has expanded well beyond its core design tool. FigJam added collaborative whiteboarding in 2021. Dev Mode launched in 2023 to bridge the gap between designers and developers. Figma Make brought AI-powered app prototyping into the mix. The company also localized for the Brazilian, Japanese, Spanish, and Korean markets.

All of that growth meant an explosion in the volume and complexity of data flowing through Figma’s systems every day.

In this article, we will learn what happened as Figma grew and how its engineering team handled the growth in terms of the data pipeline issues.

_Disclaimer: This post is based on publicly shared details from the Figma Engineering Team. Please comment if you notice any inaccuracies._

## When SELECT * Becomes Your Bottleneck

Figma’s original data pipeline did what’s called a full sync. Every run copied the entire contents of a database table, regardless of how much had actually changed since the last run. If a table had ten million rows and only fifty changed that day, the pipeline still copied all ten million. When tables are small, this is fast and cheap.

To start with, Figma’s production databases were hosted on Amazon RDS PostgreSQL and served live user traffic. Every time someone opens a file, saves a change, or loads a project, those databases handle the request. Running heavy analytical queries on these same databases, things like computing company-wide KPIs or analyzing usage trends across millions of users, would compete with live traffic and slow down the product. So like most companies at this scale, Figma maintains a separate analytics warehouse in Snowflake, a database built specifically for these kinds of large, complex queries. The catch is that data has to get from one to the other. That transfer is the synchronization pipeline.

[![Image 5](https://substackcdn.com/image/fetch/$s_!AWAB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48641814-0011-44b5-81e5-d031311c05d0_1938x1246.png)](https://substackcdn.com/image/fetch/$s_!AWAB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48641814-0011-44b5-81e5-d031311c05d0_1938x1246.png)

But Figma’s tables didn’t stay small.

As mentioned, between 2021 and 2025, they launched FigJam, Dev Mode, Figma Make, and expanded localization to serve the Brazilian, Japanese, Spanish, and Korean markets. The user base grew rapidly, and so did the data.

By 2023, daily synchronization tasks were taking around six hours to complete. The largest tables took several days. To make things worse, the pipeline required dedicated database replicas just to handle the export load without affecting production traffic. Those replicas alone cost millions of dollars annually.

Figma evaluated three options to handle this:

*   They could keep the existing system, but sync delays and replica costs made that untenable.

*   They could add parallelism to speed up the full copies, but this was a band-aid that wouldn’t scale as tables continued to grow.

*   Or they could overhaul the pipeline entirely.

They chose the overhaul, committing to incremental synchronization. Instead of copying entire tables every run, they’d capture only what changed and apply those changes to the destination. The concept is simple, but the execution is not.

## Incremental Synchronization

Incremental synchronization flips the model. Rather than asking “what does the whole table look like right now?” it asks “what changed since last time?” Only the inserts, updates, and deletes since the last sync get transferred and applied. For a table with ten million rows where fifty changed, you’re now moving fifty rows instead of ten million.

The mechanism that makes this possible is called Change Data Capture, or CDC. Every database keeps an internal log of every write operation, known as the write-ahead log, for its own crash-recovery purposes. CDC reads that log and converts it into a stream of change events. This does not add overhead to the database, and we are piggybacking on bookkeeping that the database is already doing.

The diagram below shows how CDC works on a high-level:

[![Image 6](https://substackcdn.com/image/fetch/$s_!aa_c!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5070bf1f-f0ea-414f-9d35-1276cefc933d_2086x2572.png)](https://substackcdn.com/image/fetch/$s_!aa_c!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5070bf1f-f0ea-414f-9d35-1276cefc933d_2086x2572.png)

Those change events need somewhere to go. Figma uses Kafka, a distributed streaming platform that acts as a buffer between the production database and Snowflake.

As CDC captures changes, it publishes them to Kafka topics, one topic per table. Snowflake then consumes from those topics at its own pace. This decoupling ensures that the production database doesn’t need to know or care whether Snowflake is online, busy, or behind. It just writes events to Kafka, and Kafka holds onto them until the consumer is ready. If Snowflake goes down for maintenance, no data is lost. The events queue up in Kafka and get processed once Snowflake comes back.

One point to note, however, is that the stream only captures changes from the moment you start listening. It doesn’t contain the full history of the table. So on day one, the destination database is empty, and the change stream only knows about changes happening right now. There is a need for a starting point.

That starting point is a snapshot. In this approach, we take a full copy of the table at a specific moment in time, then start applying changes from before that moment forward. Here’s why the timing matters. For example, Ssy Figma kicks off a snapshot export at 2:00 AM, and the export takes two hours to complete. During those two hours, users are still active. Records are being created, updated, and deleted. The snapshot finishes at 4:00 AM, but it only reflects the state of the table as of 2:00 AM. If the change stream starts capturing events at 4:00 AM, every change between 2:00 and 4:00 AM is lost. The destination table will be missing two hours of data, with no error to flag the gap. To avoid this, Figma ensures the Kafka CDC stream’s start offset precedes the snapshot timestamp. That overlap means some events will be duplicates of what’s already in the snapshot, but duplicates can be handled during the merge step. Missing data cannot.

Figma also had to decide whether to buy an off-the-shelf solution or build its own setup. They evaluated vendor options seriously and found three problems:

*   Generic CDC tools couldn’t leverage Amazon RDS-specific APIs, like the ability to export snapshots directly to S3 without maintaining a separate database replica.

*   Vendor pricing at Figma’s scale came out to five to ten times more than an in-house build.

*   The tools they evaluated couldn’t reliably handle Figma’s data volume, which was still growing.

Therefore, they assembled their pipeline from lower-level components:

*   Amazon RDS handles snapshot exports to S3.

*   Kafka streams the CDC events.

*   Snowflake stored procedures perform the incremental merge, in other words, applying the stream of changes to bring the destination tables up to date.

*   Merge jobs run on a configurable schedule, defaulting to every three hours.

See the diagram below:

[![Image 7](https://substackcdn.com/image/fetch/$s_!aeFj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85e21def-74c8-411a-a7a1-c4b35ed6b178_2404x1334.png)](https://substackcdn.com/image/fetch/$s_!aeFj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85e21def-74c8-411a-a7a1-c4b35ed6b178_2404x1334.png)

That three-hour default is a deliberate design choice, not a limitation. More frequent merges mean fresher data but higher Snowflake compute costs. Figma lets teams override the default where it matters. Their billing pipeline, for example, runs on 30-minute merge cycles. Each team pays only for the freshness they actually need.

## Trust But Verify

Building the pipeline is half the job. The other half is knowing whether it’s actually working correctly.

Data pipelines can fail in ways multiple ways that don’t produce errors. For example:

*   A partial failure during a snapshot export

*   A misconfigured CDC connector

*   An unexpected data format from the source.

These issues don’t crash the pipeline. They just produce wrong data. And wrong data in an analytics warehouse leads to wrong KPIs, wrong business decisions, and a slow erosion of trust in the entire data platform.

Figma’s answer to this scenario is quite rigorous. They built a dedicated validation workflow that clones the live base table, runs the entire bootstrap process independently into a temporary schema, aligns both copies to the same point in time using CDC data, and then compares them cell by cell. This runs weekly for every table in the pipeline. Most teams settle for row-count checks or sampling. Figma treats its analytical warehouse with the same correctness guarantees you’d expect from a production database.

The reason this approach works is independence. If a bug exists somewhere in the main pipeline, say a CDC connector silently drops certain types of update events, any validation that reuses the same pipeline path would inherit the same bug. The corrupted data would match the corrupted check, and everything would look fine. By bootstrapping a completely separate copy through an independent process and comparing the two, Figma guarantees that an error in one path can’t silently pass the other’s checks.

Figma also built a zero-downtime re-bootstrap capability by versioning all bootstrap artifacts except the final user-facing view. When schemas evolve, or a full re-bootstrap is needed, the new version is built in parallel and promoted via an atomic view update. Live queries are never disrupted.

The other piece that holds it all together is automation. Figma structured its automation into two tiers:

*   First-level automations handle the actual execution. You give them a table name, and they run the bootstrap or validation and alert if something goes wrong.

*   Second-level automations sit above and decide when to trigger the first tier. A controller workflow checks every few hours for new tables that need onboarding. A dispatcher workflow kicks off validation for each table weekly.

[![Image 8](https://substackcdn.com/image/fetch/$s_!cubB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4cae3d9f-2766-4de2-b45b-397ae875d137_2944x2020.png)](https://substackcdn.com/image/fetch/$s_!cubB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4cae3d9f-2766-4de2-b45b-397ae875d137_2944x2020.png)

The system is largely self-operating, and developers get involved only when alerts fire.

The payoff came early. One week into testing in their staging environment, the automated re-bootstrap routine caught a severe failure mode. Had it reached production, it would have triggered a site-wide outage lasting at least twenty minutes. The old system, a daily cron job with no automated validation, could never have caught this.

## Conclusion

The numbers tell the story quite clearly:

*   Data freshness went from 30-plus hours to under three hours, with the option to configure it down to minutes.

*   The pipeline handles tables over ten times larger than the old system could manage, with consistent and predictable performance.

*   Eliminating the dedicated export replicas produced multimillion-dollar annual savings.

*   Operations have seen zero major incidents during and after launch.

Beyond raw performance, the rebuild unlocked new capabilities.

For example, a sync-on-demand CLI tool lets developers trigger immediate synchronization outside the regular schedule. CDC data is now exposed to end users, so developers can query the full change history of any entity and not just its current state. During incident response, this means questions like “show me every change to this user’s record in the last 48 hours” get answered in minutes.

However, this project took a significant investment of time, effort, and resources.

The new system is much more complex than a daily cron job. Figma compensated with aggressive automation and validation, but that’s additional complexity layered on top. Ultimately, this tradeoff was worth it at Figma’s scale.

**References:**

*   [From multi-day latency to near real-time insights: Figma’s Data Pipeline Upgrade](https://www.figma.com/blog/figmas-data-pipeline-upgrade/)

*   [Change Data Capture](https://en.wikipedia.org/wiki/Change_data_capture)

* * *

#### Subscribe to ByteByteGo Newsletter

Explain complex systems with simple terms, from the authors of the best-selling system design book series. Join over 1,000,000 friendly readers.

Subscribe

By subscribing, you agree Substack's [Terms of Use](https://substack.com/tos), and acknowledge its [Information Collection Notice](https://substack.com/ccpa#personal-data-collected) and [Privacy Policy](https://substack.com/privacy).

 

[![Image 9: Arianna's avatar](https://substackcdn.com/image/fetch/$s_!6ian!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F51f167f5-a9f0-4b7d-ab73-9ed0c858ca23_144x144.png)](https://substack.com/profile/17024640-arianna)[![Image 10: Tanner Barcelos's avatar](https://substackcdn.com/image/fetch/$s_!Wh4T!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fecbc79d6-8552-4e7a-bd96-5529c3bd1560_932x1242.jpeg)](https://substack.com/profile/130907445-tanner-barcelos)[![Image 11: K Young's avatar](https://substackcdn.com/image/fetch/$s_!LCmW!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd786f06-8dad-4cca-937b-c35e231b1788_144x144.png)](https://substack.com/profile/131251865-k-young)[![Image 12: Kevin Clayton's avatar](https://substackcdn.com/image/fetch/$s_!kFui!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F3dc8c7b0-05f1-4c1f-8224-a29deb09959d_500x815.jpeg)](https://substack.com/profile/19403805-kevin-clayton)[![Image 13: Henry Ogedegbe Jr.'s avatar](https://substackcdn.com/image/fetch/$s_!LMaJ!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25460006-68f9-4baa-8e21-b4b0439559b8_444x444.png)](https://substack.com/profile/3346222-henry-ogedegbe-jr)

[248 Likes](https://blog.bytebytego.com/p/how-figma-upgraded-data-pipeline)∙

[2 Restacks](https://substack.com/note/p-193057411/restacks?utm_source=substack&utm_content=facepile-restacks)

248

3

2

Share

#### Discussion about this post

Comments Restacks

![Image 14: User's avatar](https://substackcdn.com/image/fetch/$s_!TnFC!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack.com%2Fimg%2Favatars%2Fdefault-light.png)

[![Image 15: ToxSec's avatar](https://substackcdn.com/image/fetch/$s_!J0tu!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbcc231af-becb-46d7-a503-8314a6b5e870_3840x3840.png)](https://substack.com/profile/8759131-toxsec?utm_source=comment)

[ToxSec](https://substack.com/profile/8759131-toxsec?utm_source=substack-feed-item)

[13h](https://blog.bytebytego.com/p/how-figma-upgraded-data-pipeline/comment/257858320 "May 12, 2026, 3:46 PM")

“These issues don’t crash the pipeline. They just produce wrong data. And wrong data in an analytics warehouse leads to wrong KPIs, wrong business decisions, and a slow erosion of trust in the entire data platform.”

really well put. i’d say the danger here is much more than a crashed pipeline.

[Like (2)](javascript:void(0))[Reply](https://blog.bytebytego.com/p/how-figma-upgraded-data-pipeline)[Share](https://blog.bytebytego.com/p/how-figma-upgraded-data-pipeline)

[![Image 16: Mitchell Kosowski's avatar](https://substackcdn.com/image/fetch/$s_!fodl!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8277a897-41f2-40f2-aeb3-30c6a8bed25d_400x400.jpeg)](https://substack.com/profile/803879-mitchell-kosowski?utm_source=comment)

[Mitchell Kosowski](https://substack.com/profile/803879-mitchell-kosowski?utm_source=substack-feed-item)

[5h](https://blog.bytebytego.com/p/how-figma-upgraded-data-pipeline/comment/258088011 "May 12, 2026, 11:31 PM")

The validation pattern here is the underrated hero of this story. Most teams settle for row counts, but any check that reuses the same pipeline path will silently inherit the same bugs the pipeline has.

An independent re-bootstrap is the only way to catch the failure modes that don't throw errors and the fact that it caught a site-wide outage in staging is the whole ROI argument in one bullet.

[Like](javascript:void(0))[Reply](https://blog.bytebytego.com/p/how-figma-upgraded-data-pipeline)[Share](https://blog.bytebytego.com/p/how-figma-upgraded-data-pipeline)

[1 more comment...](https://blog.bytebytego.com/p/how-figma-upgraded-data-pipeline/comments)

Top Latest Discussions

[Top AI Agentic Workflow Patterns](https://blog.bytebytego.com/p/top-ai-agentic-workflow-patterns)

[In this article, we will look at the most popular agentic workflow patterns and how they work.](https://blog.bytebytego.com/p/top-ai-agentic-workflow-patterns)

Dec 15, 2025•[ByteByteGo](https://substack.com/@bytebytego399569)

437

6

36

![Image 17](https://substackcdn.com/image/fetch/$s_!DIBU!,w_320,h_213,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F90fbbefd-20c5-41e4-90ac-c2f554630e66_1216x1600.png)

[EP198: Best Resources to Learn AI in 2026](https://blog.bytebytego.com/p/ep198-best-resources-to-learn-ai)

[The AI resources can be divided into different types such as](https://blog.bytebytego.com/p/ep198-best-resources-to-learn-ai)

Jan 17•[ByteByteGo](https://substack.com/@bytebytego399569)

215

1

30

![Image 18](https://substackcdn.com/image/fetch/$s_!iSG2!,w_320,h_213,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf105c7e-dcf2-4584-b4b2-d6b126043918_3000x3900.jpeg)

[Understanding Database Types](https://blog.bytebytego.com/p/understanding-database-types)

[The success of a software application often hinges on the choice of the right databases. As developers, we're faced with a vast array of database…](https://blog.bytebytego.com/p/understanding-database-types)

Apr 19, 2023•[Alex Xu](https://substack.com/@bytebytego)

1,304

12

70

![Image 19](https://substackcdn.com/image/fetch/$s_!QMIV!,w_320,h_213,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcb5bb38f-5383-495d-aed8-cf1d0a44e03b_1600x1600.png)

See all

### Ready for more?

Subscribe

© 2026 ByteByteGo · [Privacy](https://substack.com/privacy) ∙ [Terms](https://substack.com/tos) ∙ [Collection notice](https://substack.com/ccpa#personal-data-collected)

[Start your Substack](https://substack.com/signup?utm_source=substack&utm_medium=web&utm_content=footer)[Get the app](https://substack.com/app/app-store-redirect?utm_campaign=app-marketing&utm_content=web-footer-button)

[Substack](https://substack.com/) is the home for great culture

![Image 23](https://t.co/1/i/adsct?bci=4&dv=UTC%26en-US%26Google%20Inc.%26Linux%20x86_64%26255%26800%26600%268%2624%26800%26600%260%26na&eci=3&event=%7B%7D&event_id=d85feba7-3031-4307-a49a-6520cae819da&integration=advertiser&p_id=Twitter&p_user_id=0&pl_id=1e1a8f9f-0103-4a13-9be4-b8877bace2c8&pt=How%20Figma%20Upgraded%20Data%20Pipeline%20from%20Multi-Day%20Latency%20to%20Real-Time&tw_document_href=https%3A%2F%2Fblog.bytebytego.com%2Fp%2Fhow-figma-upgraded-data-pipeline&tw_iframe_status=0&tw_pid_src=1&twpid=tw.1778646498657.748447127397472488&txn_id=oesry&type=javascript&version=2.3.53)![Image 24](https://analytics.twitter.com/1/i/adsct?bci=4&dv=UTC%26en-US%26Google%20Inc.%26Linux%20x86_64%26255%26800%26600%268%2624%26800%26600%260%26na&eci=3&event=%7B%7D&event_id=d85feba7-3031-4307-a49a-6520cae819da&integration=advertiser&p_id=Twitter&p_user_id=0&pl_id=1e1a8f9f-0103-4a13-9be4-b8877bace2c8&pt=How%20Figma%20Upgraded%20Data%20Pipeline%20from%20Multi-Day%20Latency%20to%20Real-Time&tw_document_href=https%3A%2F%2Fblog.bytebytego.com%2Fp%2Fhow-figma-upgraded-data-pipeline&tw_iframe_status=0&tw_pid_src=1&twpid=tw.1778646498657.748447127397472488&txn_id=oesry&type=javascript&version=2.3.53)
