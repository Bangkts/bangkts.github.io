---
title: "Container Design Patterns for Distributed Systems"
category: "AI Notes"
categoryOrder: 3
order: 2
sourceLabel: "ByteByteGo"
---

For most of their life, containers have been considered more as a deployment concern. Package your code with its dependencies, ship it as one unit, and run it the same way everywhere.

That story was true, and it was also pretty useful, but it's just one half of what containers were good for. The other half is what happens when we stop thinking of a container as a way to deliver one application and start thinking of it as a building block we can compose with others.

Software engineering has been here before. In the 1990s, object-oriented programming gave application code a clean boundary we could compose against. Out of that boundary came design patterns, the small library of standard solutions every working programmer eventually internalizes. With containers, distributed systems have gone through the same transition.

In this article, we'll walk through the patterns that have crystallized over the past decade, organized by the scope of their coordination. Three of them describe how containers cooperate when they share a single machine. The other three describe how containers coordinate when the work spans many machines. None of these patterns is a rule. They're answers to problems that distributed-systems engineers kept solving over and over.

![Container Design Patterns](https://substackcdn.com/image/fetch/$s_!UbG9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1812b094-e384-4825-a301-4b942ef5976b_2250x2624.png)

The Abstraction Layer
