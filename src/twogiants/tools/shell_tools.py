"""Shell and system operation tools - Execute commands, navigate directories, system info."""

from langchain.tools import tool
import os
import subprocess
import platform
import sys
from typing import Optional


@tool
def execute_shell_command(command: str, timeout: int = 60, shell: bool = True) -> str:
    """Execute a shell command and return the output.
    
    ⚠️ WARNING: Use with caution! Commands are executed directly on the system.
    
    Args:
        command: Shell command to execute
        timeout: Maximum execution time in seconds (default: 60)
        shell: Execute through shell (default: True)
    
    Returns:
        Command output (stdout and stderr combined), or error message
    
    Examples:
        execute_shell_command("ls -la")
        execute_shell_command("git status")
        execute_shell_command("npm test", timeout=120)
    
    Note:
        - Both stdout and stderr are captured
        - Non-zero exit codes are reported but not treated as errors
        - Timeout prevents hanging commands
    """
    try:
        # Execute command
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # Build output
        output = []
        
        # Add stdout if present
        if result.stdout:
            output.append("📤 Output:")
            output.append(result.stdout.strip())
        
        # Add stderr if present
        if result.stderr:
            output.append("\n⚠️ Errors/Warnings:")
            output.append(result.stderr.strip())
        
        # Add exit code
        if result.returncode != 0:
            output.append(f"\n❌ Exit code: {result.returncode}")
        else:
            output.append(f"\n✓ Exit code: 0 (success)")
        
        return '\n'.join(output) if output else "✓ Command executed (no output)"
    
    except subprocess.TimeoutExpired:
        return f"❌ Error: Command timed out after {timeout} seconds\nCommand: {command}"
    
    except FileNotFoundError:
        return f"❌ Error: Command not found: {command.split()[0]}"
    
    except Exception as e:
        return f"❌ Error executing command: {e}\nCommand: {command}"


@tool
def get_current_directory() -> str:
    """Get the current working directory.
    
    Returns:
        Absolute path of current working directory
    
    Example:
        get_current_directory()
        # Returns: /home/user/projects/2giants-cli
    """
    try:
        cwd = os.getcwd()
        
        # Get some additional context
        try:
            # Try to get git repo info if in a git repository
            result = subprocess.run(
                "git rev-parse --show-toplevel",
                shell=True,
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode == 0:
                repo_root = result.stdout.strip()
                repo_name = os.path.basename(repo_root)
                
                return f"""📂 Current Directory: {cwd}

🔧 Git Repository: {repo_name}
📁 Repo Root: {repo_root}"""
        except:
            pass
        
        # Not a git repo or git not available
        return f"📂 Current Directory: {cwd}"
    
    except Exception as e:
        return f"❌ Error getting current directory: {e}"


@tool
def change_directory(path: str) -> str:
    """Change the current working directory.
    
    Args:
        path: Directory path to change to (relative or absolute)
    
    Returns:
        Success message with new directory, or error
    
    Examples:
        change_directory("src")
        change_directory("..")
        change_directory("/home/user/projects")
    
    Note:
        This affects the working directory for all subsequent commands
    """
    try:
        # Expand user home directory if present
        path = os.path.expanduser(path)
        
        # Check if directory exists
        if not os.path.exists(path):
            return f"❌ Error: Directory not found: {path}"
        
        if not os.path.isdir(path):
            return f"❌ Error: Not a directory: {path}"
        
        # Get old directory for reference
        old_dir = os.getcwd()
        
        # Change directory
        os.chdir(path)
        
        # Get new directory
        new_dir = os.getcwd()
        
        return f"""✓ Changed directory

From: {old_dir}
To:   {new_dir}"""
    
    except PermissionError:
        return f"❌ Error: Permission denied to access {path}"
    
    except Exception as e:
        return f"❌ Error changing directory: {e}"


@tool
def get_environment_variables(filter_pattern: Optional[str] = None) -> str:
    """Get environment variables.
    
    Args:
        filter_pattern: Optional pattern to filter variables (case-insensitive)
                       If provided, only shows variables containing this pattern
    
    Returns:
        Formatted list of environment variables
    
    Examples:
        get_environment_variables()  # All variables
        get_environment_variables("PATH")  # Only PATH-related
        get_environment_variables("PYTHON")  # Python-related
    
    Note:
        Shows first 50 variables if no filter provided
    """
    try:
        env_vars = dict(os.environ)
        
        # Filter if pattern provided
        if filter_pattern:
            pattern_lower = filter_pattern.lower()
            filtered = {
                k: v for k, v in env_vars.items()
                if pattern_lower in k.lower() or pattern_lower in v.lower()
            }
            
            if not filtered:
                return f"ℹ️ No environment variables found matching: {filter_pattern}"
            
            output = [f"🔍 Environment Variables (filtered by '{filter_pattern}'):\n"]
            
            for key in sorted(filtered.keys()):
                value = filtered[key]
                # Truncate long values
                if len(value) > 100:
                    value = value[:100] + "..."
                output.append(f"{key}={value}")
            
            output.append(f"\nTotal: {len(filtered)} variables")
        
        else:
            # Show first 50 variables
            output = ["📋 Environment Variables (showing first 50):\n"]
            
            for key in sorted(list(env_vars.keys())[:50]):
                value = env_vars[key]
                # Truncate long values
                if len(value) > 100:
                    value = value[:100] + "..."
                output.append(f"{key}={value}")
            
            output.append(f"\nShowing 50 of {len(env_vars)} total variables")
            output.append("💡 Use filter_pattern to search specific variables")
        
        return '\n'.join(output)
    
    except Exception as e:
        return f"❌ Error getting environment variables: {e}"


@tool
def get_system_info() -> str:
    """Get detailed system information.
    
    Returns:
        Formatted system information including OS, Python, CPU, memory, disk
    
    Example:
        get_system_info()
    
    Note:
        Requires psutil for memory/disk info. If not available, shows basic info.
    """
    try:
        info = []
        
        # OS Information
        info.append("💻 System Information\n")
        info.append("=" * 50)
        
        info.append(f"\n🖥️  Operating System:")
        info.append(f"   OS: {platform.system()} {platform.release()}")
        info.append(f"   Version: {platform.version()}")
        info.append(f"   Machine: {platform.machine()}")
        info.append(f"   Processor: {platform.processor()}")
        
        # Python Information
        info.append(f"\n🐍 Python:")
        info.append(f"   Version: {sys.version.split()[0]}")
        info.append(f"   Executable: {sys.executable}")
        info.append(f"   Platform: {sys.platform}")
        
        # Try to get CPU and Memory info (requires psutil)
        try:
            import psutil
            
            # CPU
            info.append(f"\n⚡ CPU:")
            info.append(f"   Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical")
            info.append(f"   Usage: {psutil.cpu_percent(interval=1)}%")
            
            # Memory
            memory = psutil.virtual_memory()
            info.append(f"\n💾 Memory:")
            info.append(f"   Total: {memory.total / (1024**3):.1f} GB")
            info.append(f"   Available: {memory.available / (1024**3):.1f} GB")
            info.append(f"   Used: {memory.used / (1024**3):.1f} GB ({memory.percent}%)")
            
            # Disk
            disk = psutil.disk_usage('/')
            info.append(f"\n💿 Disk (/):")
            info.append(f"   Total: {disk.total / (1024**3):.1f} GB")
            info.append(f"   Used: {disk.used / (1024**3):.1f} GB ({disk.percent}%)")
            info.append(f"   Free: {disk.free / (1024**3):.1f} GB")
        
        except ImportError:
            info.append("\n💡 Install psutil for detailed CPU/Memory/Disk info:")
            info.append("   pip install psutil")
        
        # Current Directory
        info.append(f"\n📂 Current Directory:")
        info.append(f"   {os.getcwd()}")
        
        info.append("\n" + "=" * 50)
        
        return '\n'.join(info)
    
    except Exception as e:
        return f"❌ Error getting system info: {e}"