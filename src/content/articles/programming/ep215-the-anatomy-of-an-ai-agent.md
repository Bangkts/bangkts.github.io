---
title: "EP215: The Anatomy of an AI Agent"
category: "Art of Programming Computer"
categoryOrder: 2
order: 3
source: "https://blog.bytebytego.com/p/ep215-the-anatomy-of-an-ai-agent"
sourceLabel: "ByteByteGo"
---

## Prompt Injection, Clearly Explained

[Video 1](https://www.youtube.com/watch?v=KDcayRssGbw)

## The Anatomy of an AI Agent

An AI agent can be thought of as a simple While-loop.

[![Image 5: Image](https://substackcdn.com/image/fetch/$s_!lOfS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F20aada1f-cc38-4c94-8778-eeaa7b63aceb_2484x3002.png)](https://substackcdn.com/image/fetch/$s_!lOfS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F20aada1f-cc38-4c94-8778-eeaa7b63aceb_2484x3002.png)

It uses an LLM to select an action, executes that action, evaluates the result, and repeats the process until the task is complete. Let’s take a closer look at each of these components:

*   Brain: The LLM is the core. It reads the situation, thinks, and decides what to do next. The big shift from chatbot to agent: the model isn't writing text anymore, it's making choices.

*   Planning: Hard tasks need more than one step. Agents break them down using methods like Chain of Thought (think step by step), Tree of Thoughts (try options, pick the best), or 

Reflexion (learn from mistakes and retry). Planning turns a fuzzy goal into clear actions.

*   Tools: An LLM without tools is a brain in a jar. Tools are functions the model can call, like web search, code execution, APIs, files, or browsers (often using the MCP standard). The model requests a tool, the system runs it, and the result comes back.

*   Memory: Without memory, every turn starts from zero. Short-term memory is the context window. Long-term memory lives in vector stores, files, and knowledge bases. When the window fills up, agents summarize old turns and carry the summary forward.

*   Loop: All four pieces work together in a cycle. The agent looks at the current state, decides what to do, uses a tool, sees the result, and repeats. It keeps going until it gives a final answer.

*   Guardrails: Not strictly anatomy, but important. Sandboxing, human checks, token limits, output validation, and scope limits keep autonomy from turning into expensive chaos. The more autonomy you give, the more these matter.

Over to you: when you build an agent, which of these five takes the most work to get right?

## REST vs GraphQL vs gRPC

REST, GraphQL, and gRPC are three distinct approaches to designing APIs. Each offers a different trade-off between simplicity, performance, and flexibility.

[![Image 6: Image](https://substackcdn.com/image/fetch/$s_!eDv8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffafb183d-5c2f-4a6e-994e-ecba33663b11_2484x3002.png)](https://substackcdn.com/image/fetch/$s_!eDv8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffafb183d-5c2f-4a6e-994e-ecba33663b11_2484x3002.png)

1.   REST: Each URL represents a resource, and you use standard HTTP verbs (GET, POST, PUT, DELETE) to act on it. Simple and universal, but it often requires multiple requests to assemble related data.

Trade-offs: Easy to learn, cache-friendly, and works with any HTTP client, but tends to over-fetch or under-fetch data, leading to chatty clients and version drift as endpoints proliferate.

2.   GraphQL: The client sends a query describing exactly the data shape it needs, and the server returns precisely that data through a single endpoint.

Trade-offs: Eliminates over-fetching and lets frontends evolve independently, but shifts complexity to the server (resolvers, N+1 queries), complicates caching, and makes rate-limiting and query-cost analysis harder.

3.   gRPC: Services communicate via strongly-typed method calls over HTTP/2 using compact binary (protobuf) encoding, making it ideal for fast, low-latency service-to-service communication with built-in streaming support.

Trade-offs: Excellent performance and strict contracts via protobuf schemas, but the binary format isn't human-readable, browser support requires a proxy (gRPC-Web), and debugging is harder than with plain JSON over HTTP.

Rule of thumb: REST for public APIs and broad compatibility, GraphQL when clients need flexible, aggregated views, and gRPC for internal microservices where latency and throughput matter most.

## If Claude Code is a burger...

Before each model call, Claude Code assembles a context window from 9 distinct sources.

Think of it as a burger, each layer adds something different.

[![Image 7: Image](https://substackcdn.com/image/fetch/$s_!N0Ju!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fae110097-f828-4b76-ba3c-de2a774a4ea7_2484x3002.jpeg)](https://substackcdn.com/image/fetch/$s_!N0Ju!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fae110097-f828-4b76-ba3c-de2a774a4ea7_2484x3002.jpeg)

1.   System Prompt: Defines Claude's role, behavior, and tone. This sets the foundation.

2.   Environment Info: Git status, branch info, and current date. Pulled in via getSystemContext()

3.   CLAUDE. md: A four-level instruction hierarchy: managed → user → project → local. Plain-text Markdown, so users can read, edit, and version-control everything the model sees.

4.   Auto Memory: Contextually relevant memory entries prefetched asynchronously. An LLM scans memory-file headers and surfaces up to 5 relevant files on demand.

5.   Path-scoped Rules: Conditional rules that load lazily when the agent reads files

6.   Tool Metadata: Skill descriptions, MCP tool names, and deferred tool definitions.

7.   Conversation History: Carried forward across iterations.

8.   Tool Results: File reads, command outputs, and subagent summaries.

9.   Compact Summaries: When history grows too long, older segments are replaced by model-generated summaries.

The whole design treats context as a scarce resource.

Over to you: Which of these 9 layers do you tune the most when working with Claude Code?

## git fetch vs git pull vs git pull —rebase

Most Git mistakes do not come from a bad commit. Your branch is behind, you have local commits, and now you need to bring in upstream changes. That is when the difference between git fetch, git pull, and git pull —rebase matters.

[![Image 8: Image](https://substackcdn.com/image/fetch/$s_!71ii!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F68416644-193b-4b64-8e50-2e36a950b890_2484x3002.png)](https://substackcdn.com/image/fetch/$s_!71ii!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F68416644-193b-4b64-8e50-2e36a950b890_2484x3002.png)

git fetch downloads remote changes and updates origin/main. Your local main does not move. Nothing in your working directory changes. That makes fetch the safest option when you want to inspect what changed upstream before integrating anything.

git pull goes one step further. It fetches first and then merges the upstream branch into your current branch. Your local commits stay intact, and Git adds a merge commit to connect the two histories.

git pull —rebase is the clean one. It starts with a fetch, but instead of merging, it reapplies your local commits on top of the updated upstream branch. The result is a linear history with no merge commit.

Fetch when you just want to see what's on the remote before deciding anything. Pull when you're on your own branch and don't mind merge commits showing up in the log. Rebase when you're cleaning up a feature branch before opening a PR and want the history to read cleanly.

Over to you: How do you handle a feature branch that's a few days old while main has moved 10 commits ahead?
