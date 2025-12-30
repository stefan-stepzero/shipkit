# OpenAI Integration Patterns

Common security pitfalls and best practices for OpenAI integrations.

---


### Common Mistakes:

1. **Exposing API keys client-side**
   - API keys are SECRET
   - Never include in frontend code
   - Always proxy through your backend

2. **Not handling rate limits**
   - OpenAI has RPM/TPM limits
   - MUST implement retry logic with exponential backoff
   - Handle 429 status codes

3. **Missing input validation**
   - User input goes to LLM
   - MUST validate/sanitize prompts
   - Prevent prompt injection attacks

4. **Not streaming long responses**
   - Large completions can timeout
   - Use streaming for better UX
   - Handle partial responses

### Security Checklist:

- [ ] API key stored in environment variables (not code)
- [ ] API calls made server-side only (not client)
- [ ] User input validated/sanitized before sending to OpenAI
- [ ] Rate limit handling implemented (retry with backoff)
- [ ] Costs monitored (set usage limits in OpenAI dashboard)
- [ ] Error handling for API failures
- [ ] Streaming used for long completions (optional)

### Code Pattern - Server-Side Proxy:

```javascript
// ✅ CORRECT - Server-side API route
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY, // Server-side only
});

app.post('/api/chat', async (req, res) => {
  const { message } = req.body;

  // CRITICAL: Validate input
  if (!message || message.length > 1000) {
    return res.status(400).json({ error: 'Invalid message' });
  }

  try {
    const completion = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [{ role: 'user', content: message }],
    });

    res.json({ response: completion.choices[0].message.content });
  } catch (error) {
    // Handle rate limits
    if (error.status === 429) {
      return res.status(429).json({ error: 'Rate limit exceeded, try again' });
    }
    res.status(500).json({ error: 'OpenAI error' });
  }
});
```

```javascript
// ❌ WRONG - Client-side API call
const openai = new OpenAI({
  apiKey: 'sk-proj-...' // EXPOSED - security breach!
});

const completion = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [{ role: 'user', content: userInput }],
});
```

### Code Pattern - Streaming:

```javascript
// ✅ CORRECT - Stream long responses
app.post('/api/chat-stream', async (req, res) => {
  const { message } = req.body;

  const stream = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [{ role: 'user', content: message }],
    stream: true,
  });

  res.setHeader('Content-Type', 'text/event-stream');

  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content || '';
    res.write(`data: ${JSON.stringify({ content })}\n\n`);
  }

  res.end();
});
```

### References:
- https://platform.openai.com/docs/guides/production-best-practices
- https://platform.openai.com/docs/guides/rate-limits
- https://platform.openai.com/docs/api-reference/streaming
```

---

**S3/STORAGE INTEGRATION PATTERNS**

```markdown