TOOL_DESCRIPTIONS = {
    "Note Maker Tool": "Use when the user wants to summarize, structure, or take notes on a specific topic.",
    "Flashcard Generator Tool": "Use when the user wants practice questions or flashcards to test their knowledge on a topic.",
    "Concept Explainer Tool": "Use when the user is asking for an explanation, definition, or a deeper understanding of a specific concept."
}

TOOL_SCHEMAS = {
    "Note Maker Tool": {
        "description": "A tool to create structured notes from a conversation.",
        "input_schema": {
            "user_info": "object (user profile information)",
            "chat_history": "array (recent conversation history)",
            "topic": "string (the main topic for note generation)",
            "subject": "string (academic subject area)",
            "note_taking_style": "string (enum: 'outline', 'bullet_points', 'narrative', 'structured')"
        }
    },
    "Flashcard Generator Tool": {
        "description": "A tool to generate flashcards for studying.",
        "input_schema": {
            "user_info": "object (user profile information)",
            "topic": "string (the topic for flashcard generation)",
            "count": "integer (number of flashcards to generate, 1-20)",
            "difficulty": "string (enum: 'easy', 'medium', 'hard')",
            "subject": "string (academic subject area)"
        }
    },
    "Concept Explainer Tool": {
        "description": "A tool to explain concepts in detail.",
        "input_schema": {
            "user_info": "object (user profile information)",
            "chat_history": "array (recent conversation history)",
            "concept_to_explain": "string (the specific concept to explain)",
            "current_topic": "string (broader topic context)",
            "desired_depth": "string (enum: 'basic', 'intermediate', 'advanced', 'comprehensive')"
        }
    }
}
