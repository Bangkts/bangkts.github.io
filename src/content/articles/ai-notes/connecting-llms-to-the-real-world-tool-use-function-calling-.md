---
title: "Connecting LLMs to the Real World: Tool Use, Function Calling, and MCP"
category: "AI Notes"
categoryOrder: 3
order: 4
source: "https://blog.bytebytego.com/p/connecting-llms-to-the-real-world"
sourceLabel: "ByteByteGo"
---

LLMs can search the web, pull up your calendar, book reservations, and send emails on your behalf. From the user’s perspective, it seems like typing a request, and the thing just happens.

There is, however, a lot happening underneath to make this work.

The model needs to know which tools are available, how to request them, and what to do with the results. The software surrounding the model needs to figure out what it actually wants, execute it safely, and feed the answer back.

Getting all of this right took several iterations, a couple of failed experiments, and eventually an open protocol that every major AI company is now adopting.

In this article, we will look at this progression that has happened from basic tool use to function calling to the Model Context Protocol, allowing the LLMs to go from isolated text generation tools to assistants that can do interesting stuff for the end users.

To understand why connecting LLMs to external systems is an interesting engineering problem, it helps to understand what an LLM actually does.

At their core, large language models are text-prediction engines. They take text in and produce text out. They are extraordinarily good at this. In fact, so good that the output often looks like real reasoning, but the underlying mechanism is always the same: predict the next token based on everything that came before.

This means an LLM has no built-in ability to call an API, query a database, or perform any action in the real world. Ask it “What’s the weather in Tokyo right now?” and it can give a plausible-sounding answer based on patterns in its training data, but it cannot actually check. It has no network access. It has no way to reach outside the boundaries of its own context window, the finite amount of text it can consider at once.

[![Image 2](https://substackcdn.com/image/fetch/$s_!wSzf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1df71e21-5907-42aa-8eac-313641100529_2450x1228.png)](https://substackcdn.com/image/fetch/$s_!wSzf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1df71e21-5907-42aa-8eac-313641100529_2450x1228.png)

This is a direct result of what the technology is at its core. But it creates an obvious question: if LLMs can only generate text, how do applications like ChatGPT, Claude, and Gemini end up doing things like searching the web, sending emails, or pulling data from internal systems?

The answer is that the LLM itself doesn’t perform those actions directly. Each of these products has an application layer, the surrounding software infrastructure, built around the model. That layer lets the model request actions. When ChatGPT searches the web, the model generates a structured request saying “search for X,” and OpenAI’s application infrastructure carries out the actual search and returns the results. The same pattern holds for Claude, Gemini, and any other AI assistant with tool access.

In short, the model reasons about what needs to happen, and the surrounding software makes it happen.

When an LLM-powered application supports tool use, the model receives a menu of available functions alongside each user prompt.

Each function is described with a name, a purpose, and the parameters it accepts, typically defined as a JSON schema (a structured format that specifies what inputs the function expects and what types they should be). When the model encounters a question it cannot answer from its training data alone, it can respond not with a final answer, but with a structured request asking for a specific function to be called with specific arguments.

Here are the steps:

*   The model generates this request as structured text, usually JSON. It does not execute the function itself.

*   The application layer receives that structured output, validates it, and actually runs the function (hits a weather API, queries a database, sends an email).

*   It sends the result back to the model as a new message.

*   The model then uses that result to compose its final response to the user.

For example, a user asks the application, “What’s the weather in Tokyo?”

The model has a tool called get_weather available, which accepts a location parameter. Rather than guessing, the model generates something like {”function”: “get_weather”, “arguments”: {”location”: “Tokyo”}}.

The application layer receives this, calls a real weather API, gets back “22°C, partly cloudy,” and sends that data to the model. The model then responds with a natural language answer grounded in real-time data.

This back-and-forth is called the agentic loop, as shown in the diagram below:

[![Image 3](https://substackcdn.com/image/fetch/$s_!1zI9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02aed492-3a33-44c9-8199-f77386f2a5f9_3206x1902.png)](https://substackcdn.com/image/fetch/$s_!1zI9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02aed492-3a33-44c9-8199-f77386f2a5f9_3206x1902.png)

This loop can also run for multiple rounds, with the model calling several tools in sequence to fulfill a single request. For example, a user saying “find me flights to Tokyo and check the weather there” might trigger a flight search tool call first, then a weather tool call, with the model synthesizing both results into a single response. This multi-step looping is the foundation of AI agents that are systems where the model autonomously plans and executes complex tasks.

The separation between the model deciding what should happen and the application layer actually doing it has some advantages. The application can restrict which functions the model has access to, validate arguments before executing anything, and require human approval for high-stakes actions like transferring money or deleting data.

This mechanism, formalized as “function calling” or “tool calling,” became widely available in mid-2023 when OpenAI added it as a first-class API feature.

Just a few months earlier, OpenAI had launched ChatGPT Plugins, which let third-party developers expose arbitrary APIs to ChatGPT. However, discovery was difficult, plugin quality varied wildly, and the security model was not mature enough to handle untrusted third-party tools interacting with a language model. OpenAI deprecated plugins entirely by April 2024, moving to the more controlled function-calling approach where developers explicitly define the tools the model can use.

See the timeline of evolution as below:

[![Image 4](https://substackcdn.com/image/fetch/$s_!tZRr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbd11d75-4642-4140-a2b4-cb390a5f77f0_3258x1558.png)](https://substackcdn.com/image/fetch/$s_!tZRr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbd11d75-4642-4140-a2b4-cb390a5f77f0_3258x1558.png)

Function calling worked, but it introduced a new problem. Every LLM provider implemented it differently. OpenAI had one schema format, Anthropic had another, and Google had its own. A tool built for one provider’s API wouldn’t work with another without rewriting the integration code. For developers who wanted their tools to work across multiple LLMs, or who wanted flexibility to switch providers, this fragmentation was a genuine obstacle.

The fragmentation problem gets worse as the ecosystem grows.

For example, iff there are 3 LLM providers and 5 tools to integrate, there are 15 possible custom integrations, one for each provider-tool combination. Add a sixth tool, and 3 more integrations are needed. Add a fourth provider and 5 more. The total grows as the product of providers times tools. This is called the N×M problem, and it becomes unmanageable quickly.

The Model Context Protocol was designed to solve exactly this.

Introduced by Anthropic as an open standard, MCP defines a common protocol that both LLM applications and tool providers can implement once. Each LLM client implements MCP once. Each tool server implements MCP once. The total number of integrations drops from N×M to N+M. Three providers plus five tools equals 8 implementations instead of 15.

[![Image 5](https://substackcdn.com/image/fetch/$s_!iMxs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7738e3c4-be8c-4831-8997-660ab2309778_3206x1902.png)](https://substackcdn.com/image/fetch/$s_!iMxs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7738e3c4-be8c-4831-8997-660ab2309778_3206x1902.png)

MCP works through a client-server architecture with three components.

*   An MCP Host is the AI application a user interacts with, something like Claude Desktop or an AI-powered IDE.

*   Inside the host lives an MCP Client, which handles communication with external tool providers.

*   On the other side, MCP Servers are lightweight programs that wrap around existing tools, databases, or APIs and expose them in MCP’s standard format.

[![Image 6](https://substackcdn.com/image/fetch/$s_!iC-I!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4299e65-2fcf-4ad2-84b2-f577e148855f_2772x1708.png)](https://substackcdn.com/image/fetch/$s_!iC-I!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4299e65-2fcf-4ad2-84b2-f577e148855f_2772x1708.png)

When the host starts up, its client connects to available MCP servers and asks each one to describe its capabilities. Those descriptions get fed to the model, and from there, the familiar function calling mechanism takes over.

The model sees the available tools, generates structured requests when it needs them, and the MCP infrastructure routes each request to the right server and returns the result.

Beyond tools, MCP servers can also surface resources (data the model can read, like files or database records) and prompt templates, though tools remain the core capability driving most adoption today.

See the diagram below that shows a typical request flow using MCP:

[![Image 7](https://substackcdn.com/image/fetch/$s_!F2TT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f9534a6-7dc2-41a4-b688-c2803d8d1459_1938x1624.png)](https://substackcdn.com/image/fetch/$s_!F2TT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f9534a6-7dc2-41a4-b688-c2803d8d1459_1938x1624.png)

MCP does not replace function calling. Function calling is the mechanism by which the model signals it wants to use a tool. MCP standardizes how those tools are described, discovered, and invoked so that the same tool works with any model that speaks the protocol.

In other words, they are complementary layers solving different parts of the same problem. The model doesn’t know or care whether MCP is involved behind the scenes. It sees a list of tool definitions and generates calls against them, the same way it always has.

Adoption has been remarkably fast.

In 2025, OpenAI announced MCP support across its products. Google DeepMind confirmed support for Gemini shortly after. By late 2025, over 10,000 publicly available MCP servers were listed in online directories. At the end of 2025, Anthropic donated the protocol to the newly formed Agentic AI Foundation under the Linux Foundation, co-founded by Anthropic, Block, and OpenAI, with support from AWS, Google, Microsoft, Cloudflare, and Bloomberg. What started as an open-source experiment became an industry standard in roughly a year.

That rapid growth, however, has surfaced real costs and risks that are important to understand.

The most significant is security. Every tool exposed to an LLM expands the system’s attack surface. In September 2025, this became concrete. A developer published an npm package that looked like an official email integration for MCP, mimicking the name and structure of a legitimate library from Postmark, a well-known email service. Hundreds of developers installed it. Later, it was found that a hidden code in the package was silently forwarding copies of every outgoing email to the attacker. This was a supply chain attack, where malicious code is hidden inside a dependency that looks trustworthy, and it was described as the first such attack targeting MCP servers.

Security challenges go beyond individual attacks. The protocol initially prioritized ease of adoption over robust security, and the authentication specifications went through multiple revisions as the community worked to close gaps. This is a familiar pattern in technology standards: interoperability and adoption come first, and security matures with time. The MCP specification continues to evolve, with recent revisions addressing authentication, server identity, and governance.

Beyond security, there is a subtler cost. Every tool definition exposed to the model consumes tokens in the context window. The name, description, and parameter schema of each tool all occupy space in the same finite context that holds the conversation history and task instructions. A handful of tools creates negligible overhead. Dozens or hundreds start crowding out the room the model needs to reason about the task. An agent with access to hundreds of tools sounds powerful in theory, but in practice, each additional tool slightly degrades the model’s ability to focus on the actual problem.

Tool use also does not make LLMs deterministic. The model can still hallucinate function names, pass malformed arguments, or chain tools in unexpected ways. Validation, error handling, and human approval steps are essential parts of any production system that gives an LLM access to real-world capabilities.

LLMs started as isolated text predictors, powerful but unable to interact with external systems.

Function calling gave them a structured way to request actions while keeping execution in the hands of the surrounding application. MCP standardized how tools are described and discovered, so that integrations work across providers without custom code for every combination.

Through all of these layers, however, one principle remains constant. The model reasons about what should happen, and the application layer controls whether it actually does. That boundary is where security, reliability, and control are designed in.

The space is moving fast. MCP went from launch to industry-wide standard in roughly a year. But the core concepts covered here, tool definitions, the agentic loop, the separation of reasoning from execution, and the tradeoffs that come with expanding what an LLM can reach, are ideas that will transfer regardless of which framework, provider, or protocol version ends up being used.

**References:**

*   [Function calling and other API updates by OpenAI](https://openai.com/index/function-calling-and-other-api-updates/)

*   [OpenAI ChatGPT plugins](https://openai.com/index/chatgpt-plugins/)

*   [Introducing the Model Context Protocol](https://www.anthropic.com/news/introducing-the-model-context-protocol)

*   [New tools for building agents](https://openai.com/index/new-tools-for-building-agents/)

*   [Model Context Protocol](https://en.wikipedia.org/wiki/Model_Context_Protocol)

*   [Donating the Model Context Protocol and establishing the Agentic AI Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)

*   [First Malicious MCP Server Found Stealing Emails in Rogue Postmark-MCP Package](https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html)
