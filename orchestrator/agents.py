import os
import json
import time
from typing import List, Dict, Any

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import BaseModel, Field

from .tools import TOOL_DESCRIPTIONS

load_dotenv()

TOOL_DESCRIPTIONS["Sign Language Tutor"] = "Use when the user wants to learn or translate words or phrases into sign language."

USER_INFO_EXAMPLE = {
    "user_id": "student123", "name": "Alex", "grade_level": "10",
    "learning_style_summary": "Prefers visual examples and structured notes.",
    "emotional_state_summary": "Focused and motivated",
    "mastery_level_summary": "Level 6: Good understanding, ready for application"
}

def router_agent(user_message: str) -> List[str]:
    """Analyzes the user's message to determine which tool(s) are needed."""
    print("\n--- 1. ROUTING AGENT ---")
    formatted_descriptions = "\n".join(
        [f"- {name}: {desc}" for name, desc in TOOL_DESCRIPTIONS.items()]
    )
    system_prompt = f"""
You are a high-accuracy tool router. Your sole purpose is to read a user's request and select the correct tool(s) from the provided list.

Here are the available tools:
{formatted_descriptions}

You MUST follow these rules:
1. Your response MUST be a comma-separated list of the exact tool names.
2. DO NOT attempt to answer the user's question or have a conversation.
3. DO NOT include any explanations or extra text.

Reply with only the tool names.
"""
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{user_message}")])
    llm = ChatGoogleGenerativeAI(model="gemini-pro-latest", temperature=0)
    chain = prompt | llm | StrOutputParser()
    print(f"Routing message: '{user_message}'")
    response = chain.invoke({"user_message": user_message})
    print(f"LLM Raw Response: '{response}'")
    tool_names = [tool.strip() for tool in response.split(',') if tool.strip()]
    print(f"Router decided: {tool_names}")
    return tool_names

# --- Pydantic Models for all tools ---
class FlashcardParams(BaseModel):
    topic: str = Field(description="The topic for the flashcards.")
    count: int = Field(description="The number of flashcards to create (1-20).")
    difficulty: str = Field(description="Difficulty level: 'easy', 'medium', or 'hard'.")
    subject: str = Field(description="The academic subject area.")

class ConceptExplainerParams(BaseModel):
    concept_to_explain: str = Field(description="The specific concept the user wants explained.")
    current_topic: str = Field(description="The broader subject or topic context for the explanation.")
    desired_depth: str = Field(description="The level of detail: 'basic', 'intermediate', 'advanced', or 'comprehensive'.")

class NoteMakerParams(BaseModel):
    topic: str = Field(description="The main topic for the notes.")
    subject: str = Field(description="The academic subject area.")
    note_taking_style: str = Field(description="The desired format: 'outline', 'bullet_points', 'narrative', or 'structured'.")

class SignLanguageParams(BaseModel):
    phrase_to_translate: str = Field(description="The specific word or phrase the user wants to see in sign language.")
    language: str = Field(description="The sign language to use, e.g., ASL (American Sign Language). Default to ASL if not specified.")
    output_format: str = Field(description="The desired output format, e.g., 'animated_gif' or 'video_clip'.")

def parameter_extractor_agent(user_message: str, tool_name: str) -> Dict[str, Any]:
    """Extracts the specific JSON parameters required for a given tool."""
    print(f"\n--- 2. PARAMETER EXTRACTOR AGENT for: {tool_name} ---")

    if tool_name == "Flashcard Generator Tool": pydantic_object = FlashcardParams
    elif tool_name == "Concept Explainer Tool": pydantic_object = ConceptExplainerParams
    elif tool_name == "Note Maker Tool": pydantic_object = NoteMakerParams
    elif tool_name == "Sign Language Tutor": pydantic_object = SignLanguageParams
    else:
        print(f"Parameter extractor for '{tool_name}' is not yet implemented.")
        return {"tool_name": tool_name, "status": "not_implemented"}

    output_parser = JsonOutputParser(pydantic_object=pydantic_object)
    system_prompt = """
    You are a highly intelligent parameter extraction agent... [rest of prompt is unchanged]
    """
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{user_message}")]).partial(format_instructions=output_parser.get_format_instructions())
    llm = ChatGoogleGenerativeAI(model="gemini-pro-latest", temperature=0)
    chain = prompt | llm.bind(response_mime_type="application/json") | output_parser
    print(f"Extracting parameters from: '{user_message}'")
    try:
        extracted_params = chain.invoke({"user_message": user_message, "tool_name": tool_name})
        if tool_name in ["Note Maker Tool", "Concept Explainer Tool"]:
             extracted_params["chat_history"] = [{"role": "user", "content": user_message}]
        final_payload = {"user_info": USER_INFO_EXAMPLE, **extracted_params}
        print("Extraction complete. Final Payload:", json.dumps(final_payload, indent=2))
        return final_payload
    except Exception as e:
        print(f"Error during parameter extraction: {e}")
        return {}

# --- TESTING BLOCK ---
if __name__ == '__main__':
    print("--- Testing Agent Workflow ---")
    
    print("\n--- Running Sign Language Tutor Test ---")
    message = "How do I sign the phrase 'thank you' in ASL? I'd like to see it as a video clip."
    chosen_tools = router_agent(message)
    if chosen_tools and chosen_tools[0] == "Sign Language Tutor":
        parameter_extractor_agent(message, chosen_tools[0])
    print("-" * 20)