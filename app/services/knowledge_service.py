"""Knowledge service for retrieving answers from FAQ/knowledge base.

This module provides a simple RAG-lite system that:
- Loads knowledge from JSON file
- Performs simple keyword/substring matching
- Returns relevant answers based on user queries

Currently uses simple text matching but can be upgraded to
vector embeddings and semantic search (real RAG) later.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

log = logging.getLogger(__name__)

# In-memory knowledge store
_knowledge_base: List[Dict[str, str]] = []
_knowledge_loaded: bool = False


def load_knowledge(knowledge_file: str = "faq.json") -> bool:
    """
    Load knowledge base from JSON file.

    Expected JSON structure:
    [
        {
            "question": "What is your pricing?",
            "answer": "We offer flexible pricing plans...",
            "keywords": ["price", "cost", "pricing", "how much"]
        },
        ...
    ]

    Args:
        knowledge_file: Path to JSON knowledge file (default: "faq.json")

    Returns:
        True if knowledge loaded successfully, False otherwise
    """
    global _knowledge_base, _knowledge_loaded

    try:
        # Try to find the file in the project root
        project_root = Path(__file__).parent.parent.parent
        knowledge_path = project_root / knowledge_file

        # If not found in root, try current directory
        if not knowledge_path.exists():
            knowledge_path = Path(knowledge_file)

        if not knowledge_path.exists():
            log.warning(f"Knowledge file not found: {knowledge_file}")
            return False

        # Load JSON file
        with open(knowledge_path, "r", encoding="utf-8") as f:
            _knowledge_base = json.load(f)

        # Validate structure
        if not isinstance(_knowledge_base, list):
            log.error("Knowledge file must contain a JSON array")
            return False

        # Validate each entry has required fields
        for entry in _knowledge_base:
            if not isinstance(entry, dict):
                log.error("Each knowledge entry must be a dictionary")
                return False
            if "question" not in entry or "answer" not in entry:
                log.error("Each knowledge entry must have 'question' and 'answer' fields")
                return False

        _knowledge_loaded = True
        log.info(f"Loaded {len(_knowledge_base)} knowledge entries from {knowledge_file}")
        return True

    except json.JSONDecodeError as e:
        log.error(f"Invalid JSON in knowledge file: {e}")
        return False
    except Exception as e:
        log.error(f"Error loading knowledge file: {e}")
        return False


def find_answer(message_text: str) -> Optional[str]:
    """
    Find an answer from knowledge base using simple keyword/substring matching.

    Matching strategy:
    1. Check if message contains any keywords from knowledge entries
    2. Check if message contains question text (substring match)
    3. Return the first matching answer

    Args:
        message_text: User's message text to search for

    Returns:
        Answer string if match found, None otherwise
        Never raises exceptions - returns None on any error

    Error Handling:
        - Handles None or empty message_text
        - Handles non-string message_text
        - Handles corrupted knowledge base entries
        - Handles missing or invalid entry fields
        - Always returns None on errors (never crashes)
    """
    try:
        # Validate knowledge base is loaded
        if not _knowledge_loaded:
            return None  # Silent return - not an error condition

        if not _knowledge_base or not isinstance(_knowledge_base, list):
            return None

        # Validate input
        if not message_text:
            return None

        if not isinstance(message_text, str):
            try:
                message_text = str(message_text)
            except Exception:
                log.warning(f"Could not convert message_text to string: {type(message_text)}")
                return None

        message_lower = message_text.lower().strip()
        if not message_lower:
            return None

        # Strategy 1: Check keywords (if provided)
        try:
            for entry in _knowledge_base:
                if not isinstance(entry, dict):
                    continue  # Skip invalid entries
                
                keywords = entry.get("keywords", [])
                if not isinstance(keywords, list):
                    continue
                
                if keywords:
                    # Check if any keyword appears in message
                    for keyword in keywords:
                        try:
                            if isinstance(keyword, str) and keyword.lower() in message_lower:
                                answer = entry.get("answer")
                                if answer and isinstance(answer, str) and answer.strip():
                                    log.debug(f"knowledge_keyword_match keyword={keyword}")
                                    return answer.strip()
                        except Exception as e:
                            log.debug(f"Error checking keyword '{keyword}': {e}")
                            continue
        except Exception as e:
            log.warning(f"Error in keyword matching strategy: {e}")

        # Strategy 2: Check if question text appears in message (substring match)
        try:
            for entry in _knowledge_base:
                if not isinstance(entry, dict):
                    continue
                
                question = entry.get("question", "")
                if not isinstance(question, str):
                    continue
                
                question_lower = question.lower()
                if question_lower and question_lower in message_lower:
                    answer = entry.get("answer")
                    if answer and isinstance(answer, str) and answer.strip():
                        log.debug(f"knowledge_question_match question_length={len(question)}")
                        return answer.strip()
        except Exception as e:
            log.warning(f"Error in question substring matching: {e}")

        # Strategy 3: Check if message appears in question (reverse substring)
        try:
            for entry in _knowledge_base:
                if not isinstance(entry, dict):
                    continue
                
                question = entry.get("question", "")
                if not isinstance(question, str):
                    continue
                
                question_lower = question.lower()
                if question_lower and message_lower in question_lower:
                    answer = entry.get("answer")
                    if answer and isinstance(answer, str) and answer.strip():
                        log.debug(f"knowledge_reverse_match")
                        return answer.strip()
        except Exception as e:
            log.warning(f"Error in reverse substring matching: {e}")

        # No match found
        return None

    except Exception as e:
        # Catch-all for any unexpected errors
        log.error(f"Unexpected error in find_answer: {e}", exc_info=True)
        return None


def get_knowledge_count() -> int:
    """
    Get the number of knowledge entries loaded.

    Returns:
        Number of knowledge entries, or 0 if not loaded
    """
    return len(_knowledge_base) if _knowledge_loaded else 0


def reload_knowledge(knowledge_file: str = "faq.json") -> bool:
    """
    Reload knowledge base from file.

    Useful for updating knowledge without restarting the server.

    Args:
        knowledge_file: Path to JSON knowledge file

    Returns:
        True if reloaded successfully, False otherwise
    """
    global _knowledge_loaded
    _knowledge_loaded = False
    return load_knowledge(knowledge_file)

