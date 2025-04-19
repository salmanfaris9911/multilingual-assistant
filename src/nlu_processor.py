from config import INTENT_MAP, OBJECT_MAP

def analyze_intent(text: str) -> tuple[str | None, str | None]:
    """
    Analyze text to extract intent (verb) and object (noun).
    
    This function has been improved to handle:
    - Multi-word intents and objects
    - Better matching by checking if words are contained within phrases
    - Handling of compound commands
    
    Args:
        text: The text to analyze (usually translated from speech)
        
    Returns:
        tuple: (verb, noun) where each can be None if not found
    """
    if not text:
        return None, None
        
    text = text.lower().strip()
    words = text.split()
    verb, noun = None, None
    
    # Check for multi-word matches first
    for intent, synonyms in INTENT_MAP.items():
        for synonym in synonyms:
            if synonym in text:
                verb = intent
                break
        if verb:
            break
    
    for obj, synonyms in OBJECT_MAP.items():
        for synonym in synonyms:
            if synonym in text:
                noun = obj
                break
        if noun:
            break
    
    # If multi-word matching didn't work, try individual words
    if not verb:
        for word in words:
            for intent, synonyms in INTENT_MAP.items():
                if any(word == syn or word in syn.split() for syn in synonyms):
                    verb = intent
                    break
            if verb:
                break
    
    if not noun:
        for word in words:
            for obj, synonyms in OBJECT_MAP.items():
                if any(word == syn or word in syn.split() for syn in synonyms):
                    noun = obj
                    break
            if noun:
                break
    
    return verb, noun