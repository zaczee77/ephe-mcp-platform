# ephe demo server

This demo is a small MCP style tool server written in Python with only the standard library. It speaks JSON RPC over stdio, which means it reads one JSON message per line on standard input and writes one JSON response per line on standard output. It frames the patterns from the ephe case study in code a reader can run in a minute.

## What it demonstrates

1. A server that answers an initialize request with its name and protocol version.
2. A tools list response that describes each tool and its input schema.
3. A word counter tool that returns counts for words, characters, and sentences.
4. A summarizer stub that returns the first sentences of a longer text.
5. Clear error responses for unknown methods and bad arguments.

## How to run it

1. Open a terminal in this demo folder.
2. Start the server with the command in the code block below.
3. Type one JSON RPC message per line and read one JSON response per line.
4. Send the tools list message to see both tools.
5. Send a tools call message to run a tool.
6. Stop the server with Control C.

```
python3 mcp_server.py
```

## Sample messages

The block below shows a short session. The first line is the initialize request. The second line is the initialized notification, which gets no response. The third line asks for the tool list. The last two lines call each tool once.

```
{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "manual test", "version": "0.1.0"}}}
{"jsonrpc": "2.0", "method": "notifications/initialized"}
{"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "word_count", "arguments": {"text": "Agents need clear tools. Clear tools need clear schemas."}}}
{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "summarize_text", "arguments": {"text": "First point here. Second point follows. Third point adds detail.", "max_sentences": 2}}}
```

## Notes and limits

The summarizer is a stub on purpose. It extracts sentences. It does not understand meaning, rank importance, or rewrite text. That honesty is the point of the demo. A reference implementation should make the contract visible without pretending to be the full platform.

The server keeps no state between calls, stores nothing on disk, and opens no network ports. It is a teaching tool for the protocol shape, the tool contract, and the error style described in the case study.
