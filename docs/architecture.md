# ephe architecture note

This note describes the working architecture behind ephe, the Model Context Protocol platform designed and built by Nirmeet Rao. It focuses on roles, tool registration, context flow, error handling, and evals.

## Roles

1. **Host.** The host is the application a person uses. It owns the session, the user intent, and the final presentation of results.
2. **Client.** The client speaks the protocol. It connects to one or more servers, discovers tools, sends calls, and returns results in a shape the host and the model can use.
3. **Server.** The server owns tools and resources for one domain. It validates inputs, does the work, and returns structured results or clear errors.
4. **Model.** The model reasons over the conversation and the tool results. It does not bypass the client. Tool access stays mediated and observable.

## Tool registration

Registration is the moment a tool becomes part of the product. A registered tool should carry five things.

1. A stable name that reads like a verb phrase.
2. A description written for both a human reader and a model reader.
3. An input schema with required fields, types, and sensible limits.
4. Example inputs that show the intended use.
5. A failure contract that names common errors and what the caller should do next.

Registration should be cheap to inspect. A client should be able to list tools at startup and after a server change. When two servers offer similar tools, names and descriptions must make the difference obvious. Ambiguity at registration time becomes wrong tool selection later.

## Context flow

1. The host captures user intent and session context.
2. The client lists available tools and shares the relevant schemas with the model.
3. The model proposes a tool call with arguments.
4. The client validates the call against the schema before it sends anything.
5. The server runs the tool and returns a result or an error.
6. The client passes the result back with enough context for the model to reason about it.
7. The host presents the outcome and records the trace for review.

Two rules keep the flow healthy. First, context should be explicit. If a tool needs a value, that value should arrive as an argument, not as a guess. Second, results should keep their source. A summary without provenance is hard to audit and hard to trust.

## Error handling

Errors are part of the contract, not an afterthought.

1. Validate early and fail with a specific message.
2. Separate caller errors from server errors so the next step is obvious.
3. Return partial results only when the caller can tell what is missing.
4. Log the tool name, the argument shape, and the failure class. Do not log secrets or raw personal data.
5. Give the model a path to recover, such as a corrected argument or a smaller request, when recovery is safe.

A good error message reads like product copy. It says what happened, why it matters, and what to try next.

## Eval checklist for MCP tools

Run this checklist before a tool ships and after any schema or description change.

1. Golden path cases pass with realistic inputs.
2. Empty inputs and missing fields fail clearly.
3. Oversized inputs fail clearly or are bounded by design.
4. Outputs match the promised shape every time.
5. Error messages name the problem without leaking internal detail.
6. Latency stays within the budget the host can tolerate.
7. A human reviewer can read a trace and explain what the tool did.
8. At least one case covers a plausible but wrong output, and the review step catches it.

Tools that pass this checklist are not guaranteed to be right. They are guaranteed to be inspectable, and inspectable systems are the ones teams can improve with confidence.
