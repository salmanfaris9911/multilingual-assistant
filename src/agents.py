from agno_agents import AgnoAgent

# Initialize the AgnoAgent instance
agent = AgnoAgent()

def agno_agent_handle(verb: str | None, noun: str | None, translated_text: str) -> str:
    """
    Handle various intents using the AgnoAgent class.

    Args:
        verb: The action to perform (e.g., "open", "close", "scroll_up").
        noun: The object of the action (e.g., "browser", "whatsapp"), if applicable.
        translated_text: The original command for error reporting.
        
    Returns:
        A string indicating the result of the action.
    """
    # Check if verb is missing
    if verb is None:
        return f"I couldn't understand the command: '{translated_text}'"

    # Handle "open" intent
    if verb == "open":
        if noun is None:
            return "Please specify what you want to open"
        
        success = agent.open_application(noun)
        if success:
            return f"Opened {noun}"
        else:
            return f"Failed to open {noun}"

    # Handle "close" intent
    elif verb == "close":
        if noun is None:
            return "Please specify what you want to close"
        
        success = agent.close_application(noun)
        if success:
            return f"Closed {noun}"
        else:
            return f"Failed to close {noun}"

    # Handle other intents that don't require a noun
    elif verb in ["scroll_up", "scroll_down", "volume_up", "volume_down", "mute", "unmute"]:
        # Dynamically call the corresponding method on the agent
        method = getattr(agent, verb, None)
        if method:
            success = method()
            if success:
                return f"Performed {verb.replace('_', ' ')}"
            else:
                return f"Failed to perform {verb.replace('_', ' ')}"
        else:
            return f"Action '{verb}' not implemented"

    # Handle unsupported verbs
    else:
        return f"Action '{verb}' is not supported yet"