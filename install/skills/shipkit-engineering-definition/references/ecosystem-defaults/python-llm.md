# Ecosystem Defaults — Python LLM / AI Pipelines

> **LLM-generated reference.** Authored 2026-06-27 with then-current best practice.
> **Refresh:** ecosystems move — regenerate this file when it feels stale or after a major SDK/library release. Re-run `/shipkit-engineering-definition` is not enough; ask Claude to "regenerate references/ecosystem-defaults/python-llm.md with current best practice" (and for the Anthropic SDK section, ground it against the `claude-api` skill / its reference so the SDK patterns stay correct).

## When to use

Python projects whose core is an LLM chain, agent, or AI pipeline — prompt orchestration, structured extraction, RAG, multi-step generation, tool-using agents. If the project is a general backend API that happens to call an LLM, read `python-api.md` too and treat this file as the AI-specific overlay.

## Non-negotiable defaults

- **Pydantic (v2) for every data model and I/O boundary.** Step inputs/outputs, tool arguments, API payloads, and config are all Pydantic models. This is the single biggest "don't reinvent it" win in Python AI code.
- **Structured outputs over string parsing.** Never regex/`json.loads` a free-text completion and hope. Use the provider's native structured-output / tool-use schema enforcement, validated into a Pydantic model.
- **Async by default for I/O-bound LLM calls.** LLM and HTTP calls are I/O-bound; use the async client and `asyncio` so concurrent calls (fan-out, batching) don't serialize.
- **Stream long generations.** Anything with large output or high token limits should stream to avoid request timeouts and to surface progress.
- **Typed config from the environment, not `os.getenv` scattered everywhere.** One settings object, validated at startup.

## Recommended libraries by concern

| Concern | Default | Notes |
|---|---|---|
| Data modeling / validation | **Pydantic v2** | Models for all step I/O, tool args, and results |
| App config / secrets | **pydantic-settings** | One `Settings` model reading env vars; fails fast on missing config |
| LLM SDK (Anthropic) | **Official `anthropic` SDK** | See the Anthropic SDK section below — do not hand-roll HTTP |
| LLM SDK (OpenAI) | Official `openai` SDK | Same principle: official SDK, structured outputs, async client |
| Chain orchestration | **Direct SDK calls first**; LangGraph / LlamaIndex only when the graph is genuinely complex | Reach for a framework when you have real branching/state, not for a linear 2–3 step chain |
| Structured extraction helper | `instructor` (wraps the SDK to return Pydantic models) | Optional convenience over native structured outputs when you want Pydantic-first ergonomics |
| HTTP (outbound) | **httpx** (async) | Not `requests` — you want async + timeouts |
| Retry / backoff | **tenacity** | Exponential backoff on rate limits / transient errors |
| Logging | **structlog** or **loguru** | Structured logs, never bare `print()` |
| CLI | **Typer** | Pydantic-friendly; not raw `argparse` |
| Tokenization / counting | Provider's token-counting endpoint | Don't estimate cross-provider with `tiktoken` for non-OpenAI models |
| Tests | **pytest** + fixtures; `respx`/recorded responses to stub LLM calls | Don't hit live APIs in unit tests |

## Anthropic SDK specifics (current best practice)

Ground anything here against the `claude-api` skill before writing real code — the SDK surface evolves. As of this file's authoring:

- **Use the official `anthropic` SDK**, `client.messages.create(...)` / `client.messages.stream(...)`. Never the legacy text-completions API, never raw `requests`/`httpx` against the REST endpoint when the SDK exists.
- **Async:** use `AsyncAnthropic()` for I/O-bound pipelines and concurrent calls.
- **Structured output:** prefer `client.messages.parse(...)` with `output_config={"format": {...}}` (a JSON schema, e.g. generated from a Pydantic model), or **strict tool use** (`strict: true` on the tool, schema with `additionalProperties: false` + `required`). Validate the result into your Pydantic model. This replaces brittle string parsing and assistant-prefill tricks.
- **Streaming:** for long or high-`max_tokens` generations use `with client.messages.stream(...) as stream:` and `stream.get_final_message()`; stream individual deltas only when you render progress.
- **Thinking:** on current models use adaptive thinking (`thinking={"type": "adaptive"}`) and control depth with `output_config={"effort": ...}` rather than a fixed token budget.
- **Prompt caching:** mark stable prefixes (system prompt, fixed few-shot context, deterministic tool list) with `cache_control={"type": "ephemeral"}`; keep volatile content (timestamps, per-request IDs) after the last cache breakpoint so the prefix stays byte-stable.
- **Model selection:** pin to a current model family generically in config (a `pydantic-settings` field), not a hardcoded literal scattered through the code, so model upgrades are a one-line change. Confirm exact model IDs against the `claude-api` reference at build time.
- **Errors:** catch the SDK's typed exceptions (rate-limit, connection, status) most-specific-first; let the SDK's built-in retry handle transient 429/5xx.

## Anti-patterns to avoid

- Parsing free-text LLM output with regex / string slicing instead of schema-enforced structured output.
- `requests` in an otherwise-async pipeline (blocks the event loop).
- Hand-rolled HTTP to the LLM REST endpoint when an official SDK exists.
- The legacy completions API (use the messages/chat API).
- `os.getenv("API_KEY")` sprinkled across modules instead of one validated settings object.
- `print()` debugging left in as the logging strategy.
- Hardcoded model-ID string literals duplicated across files.
- A heavyweight orchestration framework (LangChain etc.) wrapped around a trivial linear chain "because everyone uses it."
- Hitting the live LLM API inside unit tests.
