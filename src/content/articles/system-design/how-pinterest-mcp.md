---
title: "How Pinterest Built a Production MCP Ecosystem"
category: "System Design"
order: 1
---

Engineers at Pinterest work across a sprawling set of internal systems every day. They query data through Presto, debug batch jobs in Spark, manage workflows in Airflow, search internal documentation, and track bugs in ticketing platforms.

When Pinterest started building AI agents, they wanted those agents to do more than answer questions. They wanted agents that could reach into these systems directly, pulling logs, investigating bug reports, querying databases, and proposing fixes, all within the surfaces engineers already use.

The challenge was surface maths: if you have five AI-powered surfaces (an internal chat app, IDE plugins, chatbots, CLI agents, and other autonomous agents) and ten internal tools, you'd need fifty bespoke integrations without a shared protocol. In other words, every new surface or tool multiplies the work.

The Model Context Protocol (MCP) promised to collapse that multiplication into addition. Build one MCP client per surface and one MCP server per tool, and they all speak the same language.

Pinterest adopted MCP as the foundation for this vision. However, implementing the protocol turned out to be the easy part. The real engineering effort went into everything around it, such as a central registry, a two-layer auth system, a unified deployment pipeline, and observability baked in from day one.

In this article, we look at how Pinterest designed that ecosystem and what they had to get right beyond the protocol itself.

*Disclaimer: This post is based on publicly shared details from the Pinterest Engineering Team. Please comment if you notice any inaccuracies.*
