---
title: "How Pinterest Built a Production MCP Ecosystem"
category: "System Design"
categoryOrder: 1
order: 1
---

Engineers at Pinterest work across a sprawling set of internal systems every day. They query data through Presto, debug batch jobs in Spark, manage workflows in Airflow, search internal documentation, and track bugs in ticketing platforms.

When Pinterest started building AI agents, they wanted those agents to do more than answer questions. They wanted agents that could reach into these systems directly, pulling logs, investigating bug reports, querying databases, and proposing fixes, all within the surfaces engineers already use.

The challenge was surface maths: if you have five AI-powered surfaces (an internal chat app, IDE plugins, chatbots, CLI agents, and other autonomous agents) and ten internal tools, you'd need fifty bespoke integrations without a shared protocol. In other words, every new surface or tool multiplies the work.

The Model Context Protocol (MCP) promised to collapse that multiplication into addition. Build one MCP client per surface and one MCP server per tool, and they all speak the same language.

Pinterest adopted MCP as the foundation for this vision. However, implementing the protocol turned out to be the easy part. The real engineering effort went into everything around it, such as a central registry, a two-layer auth system, a unified deployment pipeline, and observability baked in from day one.

In this article, we look at how Pinterest designed that ecosystem and what they had to get right beyond the protocol itself.

*Disclaimer: This post is based on publicly shared details from the Pinterest Engineering Team. Please comment if you notice any inaccuracies.*
What is MCP
Model Context Protocol (MCP) is an open-source standard that gives large language models a unified way to talk to external tools and data sources.

![Pinterest MCP Architecture](https://substackcdn.com/image/fetch/$s_!qn5M!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0acd8c0-dcbb-4462-914c-207889b0bd28_2576x1520.png)

Instead of writing custom glue code between every AI application and every tool it needs to access, MCP defines a shared client-server protocol. An AI surface acts as the client, an MCP server wraps a tool or data source, and they communicate using a standardized format for discovering tools, invoking them, and returning structured results.


Before MCP, connecting AI surfaces to internal tools was an N x M problem. Five surfaces times ten tools equals fifty custom integrations to build and maintain. MCP turns that into an N+M problem. You build five clients and ten servers, and any client can talk to any server. That is fifteen pieces of work instead of fifty, and the gap widens as you add more surfaces or tools.
