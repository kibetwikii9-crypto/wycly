# AI Module Architecture

## 📁 File Location

**Recommended:** `app/services/ai.py`

**Rationale:**
- Follows existing service pattern (`telegram.py`, `processor.py`)
- Keeps all services in one directory
- Easy to import: `from app.services.ai import generate_response`
- Clear separation from business logic

**Alternative (if you prefer):**
- `app/ai/__init__.py` - Creates dedicated AI package
- `app/core/ai.py` - If you have a core module

---

## 🔧 Function Signature

```python
async def generate_response(prompt: str) -> str:
    """
    Generate a text response from a prompt.
    
    Args:
        prompt: The input prompt string
        
    Returns:
        Generated text response (never None or empty string)
    """
```

**Key Characteristics:**
- ✅ **Single responsibility:** Only generates text from prompt
- ✅ **Pure function:** No side effects, no state
- ✅ **Simple interface:** One input (prompt), one output (response)
- ✅ **Type safe:** Explicit `str` return type (not `Optional[str]`)
- ✅ **Always returns:** Guaranteed non-empty string

---

## 🎯 Why AI Must Be Abstracted Early

### 1. **Zero Business Logic in AI Module**

**Problem if AI logic is mixed:**
```python
# ❌ BAD: Business logic in AI module
async def generate_response(message, intent):
    if intent == "pricing":
        return "Our pricing is..."
    elif intent == "greeting":
        return "Hello!"
    # Business rules mixed with AI generation
```

**Solution with abstraction:**
```python
# ✅ GOOD: Pure AI function
async def generate_response(prompt: str) -> str:
    # Only generates text, no business decisions
    return llm.generate(prompt)
```

**Benefit:** Business logic stays in processor, AI module is swappable.

---

### 2. **Platform-Agnostic Design**

**Problem if platform-specific:**
```python
# ❌ BAD: Platform-specific logic
async def generate_response(telegram_message):
    # Hardcoded for Telegram
    chat_id = telegram_message.chat_id
    # ...
```

**Solution with abstraction:**
```python
# ✅ GOOD: Platform-agnostic
async def generate_response(prompt: str) -> str:
    # Works with any platform
    # Prompt is already normalized
    return llm.generate(prompt)
```

**Benefit:** Same AI module works for Telegram, WhatsApp, Instagram, etc.

---

### 3. **Easy Provider Swapping**

**Current (Placeholder):**
```python
async def generate_response(prompt: str) -> str:
    return "Placeholder response"
```

**Future (OpenAI):**
```python
async def generate_response(prompt: str) -> str:
    client = AsyncOpenAI(api_key=settings.openai_api_key)
    response = await client.chat.completions.create(...)
    return response.choices[0].message.content
```

**Future (Anthropic):**
```python
async def generate_response(prompt: str) -> str:
    client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    response = await client.messages.create(...)
    return response.content[0].text
```

**Benefit:** Swap entire AI provider by changing ONE file. Zero changes to business logic.

---

### 4. **Testing & Development**

**Easy to mock:**
```python
# In tests
async def mock_generate_response(prompt: str) -> str:
    return "Mock response"

# Replace in tests
app.services.ai.generate_response = mock_generate_response
```

**Easy to develop:**
- No API keys needed during development
- No network calls during testing
- Fast iteration on business logic

---

### 5. **Cost & Performance Control**

**Centralized control:**
```python
# Easy to add rate limiting
async def generate_response(prompt: str) -> str:
    await rate_limiter.acquire()
    return await llm.generate(prompt)

# Easy to add caching
async def generate_response(prompt: str) -> str:
    cached = cache.get(prompt)
    if cached:
        return cached
    response = await llm.generate(prompt)
    cache.set(prompt, response)
    return response
```

**Benefit:** All AI-related concerns (cost, performance, caching) in one place.

---

### 6. **Error Handling Isolation**

**Centralized error handling:**
```python
async def generate_response(prompt: str) -> str:
    try:
        return await llm.generate(prompt)
    except RateLimitError:
        return "Rate limit exceeded. Please try again later."
    except APIError:
        return "AI service temporarily unavailable."
    except Exception:
        return "An error occurred. Please try again."
```

**Benefit:** All AI errors handled in one place, business logic stays clean.

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────┐
│         Business Logic Layer            │
│  (processor.py - Intent, Prompts)       │
│                                         │
│  - Detects intent                       │
│  - Builds system prompts                │
│  - Combines prompts                    │
│  - Calls AI module                      │
└─────────────────┬───────────────────────┘
                  │
                  │ prompt: str
                  ▼
┌─────────────────────────────────────────┐
│         AI Abstraction Layer             │
│  (ai.py - Pure Function)                 │
│                                         │
│  - Takes prompt string                  │
│  - Returns text response                 │
│  - NO business logic                     │
│  - NO platform logic                     │
└─────────────────┬───────────────────────┘
                  │
                  │ Can swap implementation
                  ▼
┌─────────────────────────────────────────┐
│      AI Provider Implementation         │
│  (OpenAI / Anthropic / Local LLM)      │
│                                         │
│  - Actual LLM API calls                 │
│  - Provider-specific logic              │
│  - Error handling                       │
└─────────────────────────────────────────┘
```

---

## 🔄 Migration Path

### Current State:
```python
# processor.py
async def generate_ai_response(message, intent):
    # Business logic + AI logic mixed
    system_prompt = build_system_prompt(intent)
    user_prompt = build_user_prompt(message)
    # Placeholder response
    return "Response..."
```

### Future State:
```python
# processor.py (business logic only)
async def generate_ai_response(message, intent):
    system_prompt = build_system_prompt(intent)
    user_prompt = build_user_prompt(message)
    full_prompt = f"{system_prompt}\n\nUser: {user_prompt}"
    
    # Delegate to AI module (pure function)
    return await ai.generate_response(full_prompt)

# ai.py (pure AI function)
async def generate_response(prompt: str) -> str:
    # Actual LLM call
    return await openai_client.chat(prompt)
```

**Migration:** Simply replace placeholder in `ai.py` with real LLM call. Zero changes to processor.

---

## ✅ Benefits Summary

1. **Separation of Concerns:** Business logic ≠ AI logic
2. **Platform Agnostic:** Works with any messaging platform
3. **Provider Agnostic:** Easy to swap OpenAI → Anthropic → Local LLM
4. **Testable:** Easy to mock and test
5. **Maintainable:** AI changes don't affect business logic
6. **Scalable:** Add caching, rate limiting, retries in one place
7. **Cost Control:** Centralized AI usage tracking

---

## 🎯 Conclusion

**Early abstraction = Future flexibility**

By creating a pure AI module now, you ensure:
- ✅ Business logic stays clean
- ✅ AI provider can be swapped without refactoring
- ✅ Testing is simple
- ✅ Multi-platform support is easy
- ✅ Cost and performance control is centralized

**The AI module is a contract:** "Give me a prompt, I'll give you text."
Everything else (business rules, platform specifics, intent detection) stays in the processor.



