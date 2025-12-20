# Knowledge Service (RAG-Lite) Implementation

## ✅ Created `knowledge_service.py`

### File: `app/services/knowledge_service.py`

**Functions:**

1. **`load_knowledge(knowledge_file: str = "faq.json") -> bool`**
   - Loads knowledge base from JSON file
   - Validates JSON structure
   - Stores in-memory for fast access
   - Returns True if successful, False otherwise

2. **`find_answer(message_text: str) -> Optional[str]`**
   - Searches knowledge base for matching answer
   - Uses simple keyword/substring matching
   - Returns answer if match found, None otherwise

3. **`get_knowledge_count() -> int`** (bonus)
   - Returns number of knowledge entries loaded

4. **`reload_knowledge(knowledge_file: str = "faq.json") -> bool`** (bonus)
   - Reloads knowledge base (useful for updates without restart)

---

## 📄 Example `faq.json`

### Structure:
```json
[
    {
        "question": "What is your pricing?",
        "answer": "We offer flexible pricing plans...",
        "keywords": ["price", "pricing", "cost", "how much"]
    },
    ...
]
```

### Fields:
- **`question`** (required): The question text
- **`answer`** (required): The answer text
- **`keywords`** (optional): List of keywords for matching

### Example Entries:
- Pricing information
- Getting started guide
- Features list
- Customer support
- Cancellation policy
- Free trial info
- Payment methods
- Security/privacy
- Integrations
- Platform support

---

## 🔍 Matching Strategy

### Current (Simple Matching):

**Strategy 1: Keyword Matching**
```python
# Check if any keyword appears in message
for keyword in entry["keywords"]:
    if keyword.lower() in message_lower:
        return entry["answer"]
```

**Strategy 2: Question Substring Matching**
```python
# Check if question text appears in message
if question in message_lower:
    return entry["answer"]
```

**Strategy 3: Reverse Substring Matching**
```python
# Check if message appears in question
if message_lower in question:
    return entry["answer"]
```

**Example:**
```
User: "What's the price?"
→ Matches keyword "price"
→ Returns: "We offer flexible pricing plans..."
```

---

## 🧠 Integration with AI Brain

### Updated `process_message()` Flow:

**Before (No Knowledge):**
```
1. Read memory
2. Detect intent
3. Generate response
4. Update memory
```

**After (With Knowledge):**
```
1. Check knowledge base first
   → If match found: Return answer, update memory, done
   → If no match: Continue to intent-based response
2. Read memory
3. Detect intent
4. Generate response
5. Update memory
```

**Priority:**
1. ✅ Knowledge base (if match found)
2. ✅ Intent-based responses (fallback)

---

## 🚀 How This Evolves into Real RAG

### Current (RAG-Lite):

**Limitations:**
- ❌ Simple keyword matching (not semantic)
- ❌ No understanding of meaning
- ❌ Exact matches only
- ❌ No ranking/scoring
- ❌ Limited to exact keywords

**Example Problem:**
```
User: "How much does it cost?"
→ Matches keyword "cost" ✅

User: "What's the subscription fee?"
→ Matches keyword "fee" ✅

User: "Tell me about your rates"
→ No match ❌ (doesn't understand "rates" = pricing)
```

---

### Future (Real RAG with Vector Embeddings):

**Step 1: Add Vector Embeddings**

```python
# knowledge_service.py
from openai import OpenAI
import numpy as np

def generate_embeddings(text: str) -> List[float]:
    """Generate vector embedding for text."""
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def load_knowledge_with_embeddings(knowledge_file: str = "faq.json"):
    """Load knowledge and generate embeddings."""
    # Load JSON
    knowledge = json.load(open(knowledge_file))
    
    # Generate embeddings for each entry
    for entry in knowledge:
        # Embed question + answer
        text = f"{entry['question']} {entry['answer']}"
        entry['embedding'] = generate_embeddings(text)
    
    return knowledge
```

**Step 2: Semantic Search**

```python
def find_answer_semantic(message_text: str) -> Optional[str]:
    """Find answer using semantic similarity (vector search)."""
    # Generate embedding for user message
    message_embedding = generate_embeddings(message_text)
    
    # Calculate similarity with all knowledge entries
    similarities = []
    for entry in _knowledge_base:
        similarity = cosine_similarity(
            message_embedding,
            entry['embedding']
        )
        similarities.append((similarity, entry))
    
    # Return top match if similarity > threshold
    similarities.sort(reverse=True)
    if similarities[0][0] > 0.7:  # Threshold
        return similarities[0][1]['answer']
    
    return None
```

**Step 3: Vector Database (Optional)**

```python
# Use Pinecone, Weaviate, or Qdrant
import pinecone

pinecone.init(api_key=settings.pinecone_api_key)
index = pinecone.Index("knowledge-base")

def find_answer_vector_db(message_text: str) -> Optional[str]:
    """Find answer using vector database."""
    # Generate embedding
    message_embedding = generate_embeddings(message_text)
    
    # Search vector database
    results = index.query(
        vector=message_embedding,
        top_k=1,
        include_metadata=True
    )
    
    if results.matches and results.matches[0].score > 0.7:
        return results.matches[0].metadata['answer']
    
    return None
```

---

## 📊 Comparison: RAG-Lite vs Real RAG

### RAG-Lite (Current):
```
User: "What's the price?"
    ↓
Keyword matching: "price" in keywords ✅
    ↓
Return answer
```

**Pros:**
- ✅ Fast (no API calls)
- ✅ Simple (easy to understand)
- ✅ No costs
- ✅ Works offline

**Cons:**
- ❌ Limited matching (exact keywords only)
- ❌ No semantic understanding
- ❌ Misses synonyms ("rates" vs "price")
- ❌ No ranking/scoring

---

### Real RAG (Future):
```
User: "What's the price?"
    ↓
Generate embedding for message
    ↓
Vector similarity search
    ↓
Find most similar knowledge entry
    ↓
Return answer (with confidence score)
```

**Pros:**
- ✅ Semantic understanding
- ✅ Handles synonyms ("rates", "cost", "price" all match)
- ✅ Better accuracy
- ✅ Can rank multiple results
- ✅ Confidence scores

**Cons:**
- ❌ Requires API calls (OpenAI embeddings)
- ❌ More complex
- ❌ Costs money
- ❌ Slower (API latency)

---

## 🔄 Migration Path

### Step 1: Current (RAG-Lite)
```python
# Simple keyword matching
answer = find_answer(message_text)  # Uses keywords
```

### Step 2: Add Embeddings (Hybrid)
```python
# Try semantic first, fallback to keywords
answer = find_answer_semantic(message_text)
if not answer:
    answer = find_answer(message_text)  # Fallback to keywords
```

### Step 3: Full RAG (Vector DB)
```python
# Use vector database
answer = find_answer_vector_db(message_text)
```

### Step 4: Advanced RAG (Context + Retrieval)
```python
# RAG with conversation context
context = get_conversation_context(user_id)
answer = find_answer_with_context(message_text, context)
```

---

## 🎯 Key Design Principles

### 1. **Same Interface**
- ✅ `find_answer(message_text)` - Same signature
- ✅ Returns `Optional[str]` - Same return type
- ✅ No changes needed in `ai_brain.py`

### 2. **Simple and Readable**
- ✅ Clear matching logic
- ✅ Easy to understand
- ✅ Easy to debug
- ✅ Easy to extend

### 3. **Easy to Upgrade**
- ✅ Abstracted behind function
- ✅ Can swap implementation
- ✅ No changes to callers
- ✅ Gradual migration possible

### 4. **Production Ready**
- ✅ Handles missing files gracefully
- ✅ Validates JSON structure
- ✅ Logs errors appropriately
- ✅ Fast in-memory access

---

## 📝 Example Usage

### Loading Knowledge:
```python
# On app startup
load_knowledge("faq.json")
```

### Finding Answers:
```python
# In ai_brain.py
answer = find_answer("What's the price?")
if answer:
    return answer  # Use knowledge answer
else:
    return generate_intent_response()  # Fallback
```

### Example Conversations:

**User:** "What's the price?"
- ✅ Matches keyword "price"
- ✅ Returns: "We offer flexible pricing plans..."

**User:** "How do I get started?"
- ✅ Matches keyword "start"
- ✅ Returns: "Getting started is easy! Simply sign up..."

**User:** "Tell me about rates"
- ❌ No keyword match (RAG-lite limitation)
- ✅ Falls back to intent-based response

**Future (with RAG):**
- ✅ "rates" → semantic match → pricing answer

---

## ✅ Benefits Summary

1. **Immediate Value:**
   - ✅ Answers common questions
   - ✅ Reduces need for intent-based responses
   - ✅ More accurate answers

2. **Simple Implementation:**
   - ✅ JSON file (easy to edit)
   - ✅ No external dependencies
   - ✅ Fast keyword matching

3. **Future-Proof:**
   - ✅ Easy to upgrade to vector embeddings
   - ✅ Same interface
   - ✅ Can add vector DB later

4. **Production Ready:**
   - ✅ Handles errors gracefully
   - ✅ Fast in-memory access
   - ✅ Easy to maintain

---

## 🎯 Conclusion

**RAG-lite system is:**
- ✅ Implemented and working
- ✅ Simple keyword matching
- ✅ Easy to understand and maintain
- ✅ Ready to upgrade to real RAG
- ✅ Production-ready for MVP

**Real RAG upgrade will:**
- ✅ Use vector embeddings
- ✅ Semantic understanding
- ✅ Better accuracy
- ✅ Same interface (easy migration)

The knowledge service provides immediate value with simple matching while maintaining a clear path to full RAG with vector embeddings and semantic search.



