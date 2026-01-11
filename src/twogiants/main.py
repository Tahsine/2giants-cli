"""2Giants Main Class - Core orchestration."""

from dotenv import load_dotenv
import os
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from rich.console import Console

# Load environment variables
load_dotenv()

console = Console()


class TwoGiants:
    """Main class for 2Giants CLI - orchestrates all agents and workflows."""
    
    def __init__(self, safe_mode: bool = True, debug: bool = False):
        """Initialize 2Giants.
        
        Args:
            safe_mode: Enable safety checks and human approval
            debug: Enable debug logging
        """
        self.safe_mode = safe_mode
        self.debug = debug
        
        # Load API key
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GOOGLE_API_KEY not found in environment. "
                "Please create a .env file with your API key."
            )
        
        # Initialize Gemini (using Flash for quick responses)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            temperature=0.7,
            api_key=self.api_key
        )
        
        if self.debug:
            console.print("[dim]🔧 Debug mode enabled[/dim]")
            console.print(f"[dim]🔑 API Key: {self.api_key[:10]}...[/dim]")
    
    def execute(self, prompt: str, session: Optional[str] = None) -> str:
        """Execute a user command.
        
        This is the main entry point. For now, it just calls Gemini directly.
        Later, this will route to specialized agents.
        
        Args:
            prompt: User's natural language command
            session: Optional session ID for context
        
        Returns:
            Response string to display to user
        """
        
        if self.debug:
            console.print(f"[dim]📥 Received: {prompt}[/dim]")
            console.print(f"[dim]🔒 Safe mode: {self.safe_mode}[/dim]")
        
        try:
            # For now, simple Gemini call
            # TODO: Later, route to specialized agents (router, executor, research)
            
            response = self.llm.invoke(prompt)
            
            if self.debug:
                console.print(f"[dim]📤 Response length: {len(response.text)} chars[/dim]")
            
            return response.text
        
        except Exception as e:
            console.print(f"[red]❌ Error calling Gemini API:[/red] {e}")
            
            if self.debug:
                import traceback
                console.print(traceback.format_exc())
            
            return f"Sorry, I encountered an error: {e}"
    
    # Placeholder methods for future implementation
    
    def route_command(self, prompt: str) -> str:
        """Route command to appropriate agent.
        
        TODO: Implement router agent logic
        Returns: "conversation" | "executor" | "research"
        """
        # Will be implemented with router agent
        pass
    
    def execute_with_approval(self, prompt: str) -> str:
        """Execute command with human-in-the-loop approval.
        
        TODO: Implement executor workflow with approval system
        """
        # Will be implemented with executor agent + approval
        pass
    
    def research(self, query: str) -> str:
        """Research using web search and RAG.
        
        TODO: Implement research agent
        """
        # Will be implemented with research agent + RAG
        pass