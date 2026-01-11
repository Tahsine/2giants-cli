"""Router Agent - Classifies user intent and routes to specialized agents."""

from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Literal
import os

RouteType = Literal["conversation", "executor", "research"]


class RouterAgent:
    """Routes user commands to the appropriate specialized agent."""
    
    def __init__(self, api_key: str, debug: bool = False):
        """Initialize Router Agent.
        
        Args:
            api_key: Google API key for Gemini
            debug: Enable debug logging
        """
        self.debug = debug
        
        # Use Gemini Flash for fast routing
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.1,  # Low temperature for consistent classification
            api_key=api_key
        )
    
    def route(self, user_input: str) -> RouteType:
        """Classify user input and route to appropriate agent.
        
        Args:
            user_input: User's command or question
        
        Returns:
            Route type: "conversation", "executor", or "research"
        """
        
        prompt = self._build_classification_prompt(user_input)
        
        try:
            response = self.llm.invoke(prompt)
            route = response.content.strip().lower()
            
            # Validate response
            if route in ["conversation", "executor", "research"]:
                if self.debug:
                    print(f"[Router] '{user_input}' → {route}")
                return route
            else:
                # Invalid response, default to conversation
                if self.debug:
                    print(f"[Router] Invalid response '{route}', defaulting to conversation")
                return "conversation"
        
        except Exception as e:
            if self.debug:
                print(f"[Router] Error: {e}, defaulting to conversation")
            # On error, default to conversation (safest)
            return "conversation"
    
    def _build_classification_prompt(self, user_input: str) -> str:
        """Build the classification prompt for Gemini.
        
        Args:
            user_input: User's input to classify
        
        Returns:
            Formatted prompt for classification
        """
        
        return f"""Classify this user input into ONE category.

Input: "{user_input}"

Categories:
- "conversation" : greetings, questions, explanations, casual chat, how-to questions
- "executor" : commands to execute, file operations, deployments, code changes, actions
- "research" : needs web search, documentation lookup, latest information, "what's new"

Rules:
- Return ONLY the category name, nothing else
- If unsure, choose "conversation" (safest)
- "executor" only if there's a clear ACTION verb (run, deploy, create, delete, etc.)
- "research" only if needs current/external information

Examples:
"hello" → conversation
"how are you?" → conversation
"explain git rebase" → conversation
"what is Docker?" → conversation

"deploy to production" → executor
"run tests" → executor
"create a new file" → executor
"commit my changes" → executor
"delete old logs" → executor

"what's new in Python 3.13?" → research
"find React documentation" → research
"what's the latest Next.js version?" → research
"search for async/await best practices" → research

Now classify: "{user_input}"

Answer (one word only):"""
    
    def get_route_description(self, route: RouteType) -> str:
        """Get human-readable description of a route.
        
        Args:
            route: The route type
        
        Returns:
            Description string
        """
        descriptions = {
            "conversation": "💬 Conversation - I'll chat and explain",
            "executor": "⚡ Executor - I'll plan and execute with your approval",
            "research": "🔍 Research - I'll search for information"
        }
        return descriptions.get(route, "Unknown route")