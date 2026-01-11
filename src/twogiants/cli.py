"""2Giants CLI - Main entry point."""

import typer
from rich.console import Console
from rich.panel import Panel
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from typing import Optional
import os
from pathlib import Path

# Créer l'app avec invoke_without_command=True
app = typer.Typer(
    name="2g",
    help="2Giants CLI - Where human wisdom meets AI power",
    add_completion=False,
    invoke_without_command=True
)

console = Console()

# Créer le dossier config si n'existe pas
CONFIG_DIR = Path.home() / ".2giants"
CONFIG_DIR.mkdir(exist_ok=True)


@app.callback()
def main(
    ctx: typer.Context,
    prompt: Optional[str] = typer.Argument(None, help="Natural language command"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show plan without executing"),
    safe_mode: bool = typer.Option(True, "--safe/--unsafe", help="Enable safety checks"),
    session: Optional[str] = typer.Option(None, "--session", "-s", help="Session ID"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode")
):
    """2Giants CLI - Execute commands or start interactive mode.
    
    Usage:
        2g                       # Interactive mode
        2g "your command"        # One-shot mode
        2g version               # Show version
        2g history               # View history
    """
    
    # Si une sous-commande est invoquée, ne rien faire ici
    if ctx.invoked_subcommand is not None:
        return
    
    # Si pas de prompt → Mode interactif
    if prompt is None:
        start_interactive_mode(safe_mode=safe_mode, session=session, debug=debug)
        return
    
    # Mode one-shot
    execute_command(
        prompt=prompt,
        dry_run=dry_run,
        safe_mode=safe_mode,
        session=session,
        debug=debug
    )


def start_interactive_mode(
    safe_mode: bool = True,
    session: Optional[str] = None,
    debug: bool = False
):
    """Start the interactive loop mode."""
    
    # ASCII Art Banner
    banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   ██████╗  ██████╗ ██╗ █████╗ ███╗   ██╗████████╗███████╗║
║   ╚════██╗██╔════╝ ██║██╔══██╗████╗  ██║╚══██╔══╝██╔════╝║
║    █████╔╝██║  ███╗██║███████║██╔██╗ ██║   ██║   ███████╗║
║   ██╔═══╝ ██║   ██║██║██╔══██║██║╚██╗██║   ██║   ╚════██║║
║   ███████╗╚██████╔╝██║██║  ██║██║ ╚████║   ██║   ███████║║
║   ╚══════╝ ╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝║
║                                                          ║
║         Where human wisdom meets AI power                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
    
    console.print(banner, style="bold cyan")
    console.print()
    
    # Info
    console.print("💡 [cyan]Type your commands naturally, like talking to a human[/cyan]")
    console.print("📝 [dim]Type 'help' for commands, 'exit' or 'quit' to leave[/dim]")
    console.print()
    
    if safe_mode:
        console.print("🛡️  [green]Safe mode: ON[/green] (dangerous commands require approval)")
    else:
        console.print("⚠️  [yellow]Safe mode: OFF[/yellow] (use with caution!)")
    
    console.print()
    console.print("─" * 60)
    console.print()
    
    # Setup prompt with history
    history_file = CONFIG_DIR / "history"
    prompt_session = PromptSession(
        history=FileHistory(str(history_file))
    )
    
    # Interactive loop
    while True:
        try:
            # Get user input
            user_input = prompt_session.prompt("2g> ")
            
            # Strip whitespace
            user_input = user_input.strip()
            
            # Skip empty input
            if not user_input:
                continue
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'q', 'bye']:
                console.print("\n[yellow]👋 Goodbye! Thanks for using 2Giants![/yellow]\n")
                break
            
            # Check for help
            if user_input.lower() in ['help', '?']:
                show_help()
                continue
            
            # Check for clear
            if user_input.lower() in ['clear', 'cls']:
                console.clear()
                continue
            
            # Execute command
            console.print()  # Blank line
            execute_command(
                prompt=user_input,
                dry_run=False,
                safe_mode=safe_mode,
                session=session,
                debug=debug
            )
            console.print()  # Blank line
        
        except KeyboardInterrupt:
            # Ctrl+C pressed
            console.print("\n[yellow]⚠️  Interrupted. Type 'exit' to quit.[/yellow]")
            continue
        
        except EOFError:
            # Ctrl+D pressed
            console.print("\n[yellow]👋 Goodbye![/yellow]\n")
            break
        
        except Exception as e:
            console.print(f"\n[red]❌ Error: {e}[/red]\n")
            if debug:
                import traceback
                console.print(traceback.format_exc())


def execute_command(
    prompt: str,
    dry_run: bool = False,
    safe_mode: bool = True,
    session: Optional[str] = None,
    debug: bool = False
):
    """Execute a single command (called by both modes)."""
    
    try:
        # Import here to avoid circular imports
        from twogiants.main import TwoGiants
        
        # Show what we're processing
        console.print(f"[cyan]💬 You:[/cyan] {prompt}")
        console.print()
        
        if dry_run:
            console.print("[yellow]🔍 DRY RUN MODE - No execution[/yellow]")
            return
        
        # Create TwoGiants instance
        cli = TwoGiants(safe_mode=safe_mode, debug=debug)
        
        # Execute
        console.print("[dim]🤖 2Giants is thinking...[/dim]")
        response = cli.execute(prompt, session=session)
        
        # Display response
        console.print(f"[green]🤖 2Giants:[/green] {response}")
    
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        if debug:
            import traceback
            console.print(traceback.format_exc())

def show_help():
    """Show help message in interactive mode."""
    
    help_text = """
[cyan bold]Available Commands:[/cyan bold]

[yellow]Natural Language Commands:[/yellow]
  Just type what you want naturally!
  Examples:
    • deploy to production
    • create a new React component
    • what's the latest Python version?
    • run tests
    
[yellow]Special Commands:[/yellow]
  [cyan]help, ?[/cyan]      Show this help message
  [cyan]clear, cls[/cyan]   Clear the screen
  [cyan]exit, quit[/cyan]   Exit interactive mode
  
[yellow]Tips:[/yellow]
  • Use ↑↓ arrows to navigate command history
  • Press Ctrl+C to cancel current input
  • Press Ctrl+D or type 'exit' to quit
"""
    
    console.print(Panel(help_text, title="2Giants Help", border_style="cyan"))


@app.command()
def version():
    """Show version information."""
    console.print("[cyan bold]2Giants CLI v1.0.0[/cyan bold]")
    console.print("Powered by Gemini 3 and LangGraph")
    console.print()
    console.print("[dim]https://github.com/yourusername/2giants-cli[/dim]")


@app.command()
def history(
    date: str = typer.Option(None, "--date", help="Date (YYYY-MM-DD)"),
    last: int = typer.Option(10, "--last", "-n", help="Show last N entries"),
    stats: bool = typer.Option(False, "--stats", help="Show statistics")
):
    """View execution history."""
    console.print("[yellow]📜 History feature coming soon...[/yellow]")


@app.command()
def chat(
    safe_mode: bool = typer.Option(True, "--safe/--unsafe"),
    session: Optional[str] = typer.Option(None, "--session", "-s"),
    debug: bool = typer.Option(False, "--debug")
):
    """Start interactive chat mode (same as running '2g' with no args)."""
    start_interactive_mode(safe_mode=safe_mode, session=session, debug=debug)


if __name__ == "__main__":
    app()