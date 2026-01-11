# Router Agent Configuration

## Role
Quick classification of user intent to route to specialized agents.

## Objective
- Fast classification (< 1 second)
- High accuracy (> 90%)
- Safe defaults (when unsure → conversation)

## Categories

### Conversation
**When to use:**
- Greetings and casual chat
- Questions about concepts
- Explanations and how-to queries
- General knowledge questions

**Examples:**
- "hello", "hi", "hey"
- "what is X?", "how does Y work?"
- "explain Z to me"
- "tell me about..."

**Agent:** Conversation Agent (simple Q&A)

---

### Executor
**When to use:**
- Commands with action verbs
- File operations
- Code changes
- Deployments
- Git operations
- System commands

**Examples:**
- "deploy to production"
- "run tests"
- "create a new file"
- "delete logs"
- "commit changes"

**Agent:** Executor Agent (with human-in-the-loop approval)

**⚠️ Important:** Always requires human approval for medium/high risk actions

---

### Research
**When to use:**
- Queries about current/latest information
- Documentation lookup
- Web search needed
- Version/release queries

**Examples:**
- "what's new in Python?"
- "latest React version"
- "find documentation for X"
- "search for best practices"

**Agent:** Research Agent (with RAG + web search)

---

## Routing Logic

### Decision Tree
```
Is it a greeting or general question?
  └─ YES → conversation

Does it have an action verb (run, create, deploy, etc.)?
  └─ YES → executor

Does it need current/external information?
  └─ YES → research

Still unsure?
  └─ DEFAULT → conversation (safest)
```

### Confidence Threshold
- High confidence (> 0.8): Route to classified agent
- Medium confidence (0.5-0.8): Consider context, lean toward conversation
- Low confidence (< 0.5): Default to conversation

---

## Special Cases

### Ambiguous Inputs
- "check the status" → Could be executor (git status) or conversation (explain status)
- **Solution:** Default to conversation, let user clarify

### Multi-intent Inputs
- "search for React docs and deploy" → Multiple intents
- **Solution:** Route to primary intent (executor in this case)

### Empty or Invalid Inputs
- Empty string, gibberish, etc.
- **Solution:** Conversation agent handles gracefully

---

## Performance Targets

- **Speed:** < 500ms per classification
- **Accuracy:** > 90% correct routing
- **Reliability:** 99.9% uptime (no crashes on invalid input)

---

## Future Improvements

- [ ] Add confidence scoring
- [ ] Support multi-intent routing
- [ ] Learn from user corrections
- [ ] Add more specialized routes (code review, documentation generation, etc.)