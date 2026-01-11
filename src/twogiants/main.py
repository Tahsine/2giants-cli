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
        
        # Initialize Router Agent
        from twogiants.agents.router import RouterAgent
        self.router = RouterAgent(api_key=self.api_key, debug=debug)
        
        # Initialize base LLM (for simple responses)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            temperature=0.7,
            api_key=self.api_key
        )
        
        if self.debug:
            console.print("[dim]🔧 Debug mode enabled[/dim]")
            console.print(f"[dim]🔑 API Key: {self.api_key[:10]}...[/dim]")
            console.print("[dim]🧭 Router Agent initialized[/dim]")
    
    def execute(self, prompt: str, session: Optional[str] = None) -> str:
        """Execute a user command.
        
        Args:
            prompt: User's natural language command
            session: Optional session ID for context
        
        Returns:
            Response string to display to user
        """
        
        if self.debug:
            console.print(f"[dim]📥 Received: {prompt}[/dim]")
        
        try:
            # Route the command
            route = self.router.route(prompt)
            
            # Show routing info
            route_desc = self.router.get_route_description(route)
            console.print(f"[dim]{route_desc}[/dim]")
            console.print()
            
            # Handle based on route
            if route == "conversation":
                return self._handle_conversation(prompt)
            
            elif route == "executor":
                return self._handle_executor(prompt)
            
            elif route == "research":
                return self._handle_research(prompt)
            
            else:
                # Fallback (should not happen)
                return self._handle_conversation(prompt)
        
        except Exception as e:
            console.print(f"[red]❌ Error:[/red] {e}")
            
            if self.debug:
                import traceback
                console.print(traceback.format_exc())
            
            return f"Sorry, I encountered an error: {e}"
    
    def _handle_conversation(self, prompt: str) -> str:
        """Handle conversation requests.
        
        TODO: Implement dedicated Conversation Agent
        For now, uses basic Gemini.
        """
        
        system_prompt = """You are 2Giants, a friendly and helpful AI assistant.
You answer questions, explain concepts, and have casual conversations.
Be concise but thorough. Be friendly but professional.
If the user wants to execute something, suggest they rephrase as a command."""
        
        messages = [
            ("system", system_prompt),
            ("user", prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.text
    
    def _handle_executor(self, prompt: str) -> str:
        """Handle execution requests.
        
        TODO: Implement Executor Agent with approval system
        For now, just acknowledges the request.
        """
        
        return f"""🚧 Executor Agent (Coming Soon)

I understand you want to execute: "{prompt}"

The Executor Agent will:
1. Plan the execution steps
2. Assess risks for each step
3. Show you the plan
4. Wait for your approval
5. Execute approved commands

This feature is being implemented. For now, you can ask me questions about what this command would do!"""
    
    def _handle_research(self, prompt: str) -> str:
        """Handle research requests.
        
        TODO: Implement Research Agent with RAG + web search
        For now, uses Gemini knowledge.
        """
        
        system_prompt = """You are 2Giants Research Agent.
Answer the query using your knowledge. Be factual and cite when possible.
Note: Web search and documentation indexing will be added soon for current information."""
        
        messages = [
            ("system", system_prompt),
            ("user", prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        return f"""🔍 Research Mode (Basic - Web search coming soon)

{response.text}

💡 Note: Full research capabilities with web search and documentation indexing are being implemented."""