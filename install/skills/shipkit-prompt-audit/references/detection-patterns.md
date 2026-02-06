# Detection Patterns for LLM Integrations

Grep and Glob patterns used by `shipkit-prompt-audit` to discover LLM integration points.

---

## API Client Detection

### OpenAI

```
Grep: pattern="new OpenAI\(" glob="**/*.{ts,tsx,js,jsx,py}"
Grep: pattern="openai\.chat\.completions" glob="**/*.{ts,tsx,js,jsx,py}"
Grep: pattern="openai\.completions" glob="**/*.{ts,tsx,js,jsx,py}"
Grep: pattern="openai\.embeddings" glob="**/*.{ts,tsx,js,jsx,py}"
Grep: pattern="from openai import" glob="**/*.py"
Grep: pattern="import OpenAI" glob="**/*.{ts,tsx,js,jsx}"
```

### Anthropic

```
Grep: pattern="new Anthropic\(" glob="**/*.{ts,tsx,js,jsx,py}"
Grep: pattern="anthropic\.messages\.create" glob="**/*.{ts,tsx,js,jsx,py}"
Grep: pattern="from anthropic import" glob="**/*.py"
Grep: pattern="import Anthropic" glob="**/*.{ts,tsx,js,jsx}"
```

### Google Gemini

```
Grep: pattern="GoogleGenerativeAI\|GenerativeModel" glob="**/*.{ts,tsx,js,jsx,py}"
Grep: pattern="model\.generateContent" glob="**/*.{ts,tsx,js,jsx,py}"
Grep: pattern="google\.generativeai" glob="**/*.py"
```

### LangChain

```
Grep: pattern="ChatOpenAI\|ChatAnthropic\|ChatGoogleGenerativeAI" glob="**/*.{ts,tsx,js,jsx,py}"
Grep: pattern="LLMChain\|RunnableSequence\|RunnableParallel" glob="**/*.{ts,tsx,js,jsx,py}"
Grep: pattern="PromptTemplate\|ChatPromptTemplate" glob="**/*.{ts,tsx,js,jsx,py}"
Grep: pattern="from langchain" glob="**/*.{ts,tsx,js,jsx,py}"
```

### Vercel AI SDK

```
Grep: pattern="generateText\|streamText\|generateObject\|streamObject" glob="**/*.{ts,tsx,js,jsx}"
Grep: pattern="from ['\"]ai['\"]" glob="**/*.{ts,tsx,js,jsx}"
Grep: pattern="from ['\"]@ai-sdk/" glob="**/*.{ts,tsx,js,jsx}"
Grep: pattern="useChat\|useCompletion\|useObject" glob="**/*.{ts,tsx,js,jsx}"
```

### Other Providers

```
Grep: pattern="Groq\|Mistral\|Cohere\|Replicate" glob="**/*.{ts,tsx,js,jsx,py}"
Grep: pattern="ollama\|localhost:11434" glob="**/*.{ts,tsx,js,jsx,py}"
```

---

## Prompt Template Detection

### Structured Message Arrays

```
Grep: pattern="role.*system.*content\|role.*user.*content\|role.*assistant" glob="**/*.{ts,tsx,js,jsx,py}"
Grep: pattern="\{.*role:.*system" glob="**/*.{ts,tsx,js,jsx}"
```

### Prompt Files

```
Glob: pattern="**/*.prompt"
Glob: pattern="**/*.prompt.md"
Glob: pattern="**/*.prompt.txt"
Glob: pattern="**/prompts/**/*.{md,txt,yaml,yml}"
Glob: pattern="**/prompt-templates/**"
```

### Template Literals with AI Instructions

```
Grep: pattern="You are a\|As an AI\|You are an" glob="**/*.{ts,tsx,js,jsx,py}"
Grep: pattern="system.*prompt\|systemPrompt\|SYSTEM_PROMPT" glob="**/*.{ts,tsx,js,jsx,py}"
```

---

## Schema & Validation Detection

### Zod Schemas Near AI Calls

```
Grep: pattern="z\.object\(.*\)" glob="**/*.{ts,tsx,js,jsx}"
```

Cross-reference with AI call files to find schemas used for output validation.

### JSON Parsing of AI Output

```
Grep: pattern="JSON\.parse\(" glob="**/*.{ts,tsx,js,jsx}"
```

Check if these are parsing LLM responses (read surrounding context).

### Structured Output Modes

```
Grep: pattern="response_format.*json\|response_format.*json_schema" glob="**/*.{ts,tsx,js,jsx,py}"
Grep: pattern="generateObject\|streamObject" glob="**/*.{ts,tsx,js,jsx}"
Grep: pattern="tool_choice\|function_call" glob="**/*.{ts,tsx,js,jsx,py}"
```

---

## Pipeline Pattern Detection

### Sequential Chains

```
Grep: pattern="await.*await" multiline=true glob="**/*.{ts,tsx,js,jsx}"
```

Look for multiple sequential await calls to AI APIs in the same function.

### Parallel Execution

```
Grep: pattern="Promise\.all\|Promise\.allSettled" glob="**/*.{ts,tsx,js,jsx}"
```

Check if any AI calls are parallelized.

### Pipeline Orchestration

```
Grep: pattern="pipe\(|\.pipe\(|RunnableSequence|RunnableParallel" glob="**/*.{ts,tsx,js,jsx,py}"
Grep: pattern="chain\.|\.chain\(" glob="**/*.{ts,tsx,js,jsx,py}"
```

---

## Fallback Pattern Detection

### Retry Logic

```
Grep: pattern="retry\|maxRetries\|retryCount\|backoff" glob="**/*.{ts,tsx,js,jsx,py}"
```

### Error Handling on AI Calls

```
Grep: pattern="catch.*openai\|catch.*anthropic\|catch.*generate" glob="**/*.{ts,tsx,js,jsx,py}"
```

### Model Fallback

```
Grep: pattern="fallback.*model\|model.*fallback\|backup.*model" glob="**/*.{ts,tsx,js,jsx,py}"
```

### Rate Limit Handling

```
Grep: pattern="rate.limit\|429\|too.many.requests\|RateLimitError" glob="**/*.{ts,tsx,js,jsx,py}"
```

---

## Dependency Detection (package.json / requirements.txt)

### Node.js / TypeScript

```
Grep: pattern="openai\|@anthropic-ai/sdk\|@google/generative-ai\|langchain\|\"ai\"" path="package.json"
Grep: pattern="@ai-sdk/" path="package.json"
```

### Python

```
Grep: pattern="openai\|anthropic\|google-generativeai\|langchain" path="requirements.txt"
Grep: pattern="openai\|anthropic\|google-generativeai\|langchain" path="pyproject.toml"
```

---

## Usage Notes

1. **Start with dependency detection** — check package.json/requirements.txt first to know which SDKs to look for
2. **Then scan for API calls** — use provider-specific patterns
3. **Then find prompt templates** — may be separate from API call sites
4. **Cross-reference** — match prompts to the calls that use them
5. **Exclude test files** if scope is production code only (add `--glob '!**/*.test.*'`)
