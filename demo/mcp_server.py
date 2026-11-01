#!/usr/bin/env python3
"""A minimal MCP-style tool server for the ephe case study.

This is a teaching demo, not the full ephe platform. It speaks
JSON-RPC 2.0 over stdio using only the Python standard library:
one JSON message per line in, one JSON response per line out.

Run it with:

    python3 mcp_server.py

Then type messages such as:

    {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
    {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
     "params": {"name": "word_count",
                "arguments": {"text": "Hello tool contract."}}}
"""

import json
import re
import sys

PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "ephe-demo-server", "version": "1.0.0"}

# A sentence is a run of text that ends with ., ! or ?, plus any tail
# text that has no terminator at all.
SENTENCE_RE = re.compile(r"[^.!?]+[.!?]|[^.!?]+$")
WORD_RE = re.compile(r"\S+")


TOOLS = [
    {
        "name": "word_count",
        "description": (
            "Count the words, characters, and sentences in a piece of "
            "text. Useful as a sanity check on tool contracts because "
            "the correct answer is easy for a human to verify."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to count.",
                }
            },
            "required": ["text"],
        },
    },
    {
        "name": "summarize_text",
        "description": (
            "Return the first sentences of a text. This is an extractive "
            "stub on purpose: it does not rank or rewrite anything."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract sentences from.",
                },
                "max_sentences": {
                    "type": "integer",
                    "description": "How many sentences to return.",
                    "minimum": 1,
                    "maximum": 10,
                    "default": 2,
                },
            },
            "required": ["text"],
        },
    },
]


def split_sentences(text):
    """Split text into trimmed sentences, dropping empty fragments."""
    sentences = []
    for match in SENTENCE_RE.findall(text):
        sentence = match.strip()
        if sentence:
            sentences.append(sentence)
    return sentences


def tool_word_count(arguments):
    """Run the word_count tool and return a plain text result."""
    text = arguments.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("word_count requires a non-empty 'text' string.")
    words = WORD_RE.findall(text)
    sentences = split_sentences(text)
    result = {
        "words": len(words),
        "characters": len(text),
        "sentences": len(sentences),
    }
    return json.dumps(result, indent=2)


def tool_summarize_text(arguments):
    """Run the summarize_text tool and return extracted sentences."""
    text = arguments.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("summarize_text requires a non-empty 'text' string.")
    max_sentences = arguments.get("max_sentences", 2)
    if not isinstance(max_sentences, int) or isinstance(max_sentences, bool):
        raise ValueError("'max_sentences' must be an integer.")
    if max_sentences < 1 or max_sentences > 10:
        raise ValueError("'max_sentences' must be between 1 and 10.")
    sentences = split_sentences(text)
    if not sentences:
        raise ValueError("No sentences could be extracted from 'text'.")
    return " ".join(sentences[:max_sentences])


TOOL_HANDLERS = {
    "word_count": tool_word_count,
    "summarize_text": tool_summarize_text,
}


def make_result(request_id, result):
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def make_error(request_id, code, message):
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message},
    }


def handle_request(request):
    """Handle one decoded JSON-RPC request.

    Returns a response dict, or None for notifications, which by
    definition get no response.
    """
    if not isinstance(request, dict):
        return make_error(None, -32600, "Request must be a JSON object.")

    method = request.get("method")
    request_id = request.get("id")
    is_notification = "id" not in request

    if method == "initialize":
        result = {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": SERVER_INFO,
        }
        return make_result(request_id, result)

    if method == "ping":
        return None if is_notification else make_result(request_id, {})

    if isinstance(method, str) and method.startswith("notifications/"):
        # All other notifications are accepted and ignored.
        return None

    if method == "tools/list":
        return make_result(request_id, {"tools": TOOLS})

    if method == "tools/call":
        params = request.get("params") or {}
        name = params.get("name")
        arguments = params.get("arguments") or {}
        handler = TOOL_HANDLERS.get(name)
        if handler is None:
            return make_error(request_id, -32602, f"Unknown tool: {name!r}")
        if not isinstance(arguments, dict):
            return make_error(
                request_id, -32602, "'arguments' must be an object."
            )
        try:
            text = handler(arguments)
        except ValueError as exc:
            return make_result(
                request_id,
                {
                    "content": [{"type": "text", "text": str(exc)}],
                    "isError": True,
                },
            )
        return make_result(
            request_id,
            {"content": [{"type": "text", "text": text}], "isError": False},
        )

    if is_notification:
        return None
    return make_error(request_id, -32601, f"Method not found: {method!r}")


def main():
    """Entry point: read JSON-RPC messages from stdin, line by line."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError as exc:
            response = make_error(None, -32700, f"Parse error: {exc}")
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
            continue
        response = handle_request(request)
        if response is not None:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
