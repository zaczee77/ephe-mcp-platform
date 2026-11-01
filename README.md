# ephe

ephe is a Model Context Protocol platform that Nirmeet Rao designed and built to make agent tooling easier to ship, test, and trust in production LLM workflows.

## What ephe is

ephe gives LLM applications a structured way to discover tools, call tools, and pass context between a client, a model, and external systems. A tool is exposed through an MCP server with a clear name, a clear description, and a typed input schema. The client can list what exists before it asks a model to act. That small discipline turns fragile prompt glue into a product surface that can be versioned, tested, and improved.

The problem it solves is simple to state and hard to live with. Agent demos are easy. Agent systems that people trust at work are not. Tools fail in quiet ways. Inputs arrive incomplete. Outputs look plausible while being wrong. Without shared contracts for tools and context, every new integration becomes custom work and every failure becomes a debugging session with no shared language.

## Why I built it

I built ephe after shipping production LLM products and learning where the real cost sits. At Concordia Pharma I shipped PharmFlows, a set of LLM workflows that cut operational errors by 80 percent and cycle time by 30 percent. I also built the Paxei MVP, which used EHR sandbox APIs to cut prior authorization prep from 45 minutes to 10 minutes. In the same body of work, SQL anomaly detection cut fraud by 35 percent.

Those projects taught me that model quality is only part of the story. The surrounding system decides whether a workflow survives contact with real users. Tool contracts, context discipline, failure handling, and evals are product work. I founded Zeinloop, a compliance SaaS product, and that founder experience reinforced the same lesson from the business side. A feature is not done when it works once. It is done when a team can operate it, explain it, and improve it.

My published research on bias mitigation in generative AI, IJISRT24JUL1248, added one more lesson. Outputs need structured scrutiny before anyone calls them good.

## Architecture overview

ephe follows the MCP shape of hosts, clients, and servers.

1. **Host application.** The product surface where a person states intent and reviews outcomes.
2. **MCP client.** The client connects to servers, lists tools, and carries tool calls and results between the host, the model, and each server.
3. **MCP server.** A server owns a focused set of tools for one domain and validates every call against the schema for that tool.
4. **Context flow.** Context moves in explicit steps. A request is formed, a tool is selected, a call is made, a result returns, and a person or a model reviews what happened.
5. **Evaluation layer.** Sample tasks and scoring checks sit beside the tools so quality is measured on purpose, not by anecdote.

A fuller note lives in the docs folder of this repository, in the architecture file.

## Design principles

1. **Tool schemas are the product surface.** A schema is a promise. Names, descriptions, and required fields tell both humans and models what a tool accepts and what it returns. If a human cannot predict what a tool will accept, a model will struggle too.
2. **Design for failure modes first.** Timeouts, empty results, malformed inputs, and partial outputs are normal events. Each tool should say what failed in plain language and leave the caller with a next step.
3. **Context is a budget.** Pass the smallest context that lets the tool do the job. Extra context adds cost, latency, and confusion.
4. **Evals belong beside the tool.** Every tool needs sample inputs, expected traits in the output, and edge cases. A tool without evals is a hope, not a product.
5. **Small tools, clear jobs.** A tool that does one job well is easier to test, reuse, and replace than a giant tool that tries to do everything.

## What I learned

Building ephe changed how I scope AI products. The model is rarely the hardest part for long. The hard part is the contract around the model. Who provides context. What a tool may change. How errors surface. How a team knows an output is good enough to act on.

It also changed how I write product requirements. A requirement for an agent feature should name the tool, the schema, the failure modes, the eval cases, and the human review point. When those five things are clear, engineering estimates get better and demos turn into systems people can trust.

## The demo in this repository

The demo folder contains a minimal reference implementation of the patterns described here. It is not the full ephe platform. It exists so a reader can run a small MCP style server, list its tools, call its tools, and see the contract in action without any external packages.

## Links

1. Portfolio: https://nirmeetrao.com
2. LinkedIn: https://www.linkedin.com/in/nirmeet-rao
3. GitHub: https://github.com/Zaczee77
