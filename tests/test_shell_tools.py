"""Test shell tools."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from twogiants.tools.shell_tools import (
    execute_shell_command,
    get_current_directory,
    change_directory,
    get_environment_variables,
    get_system_info
)

def test_shell_tools():
    """Test all shell tools."""
    
    print("🧪 Testing Shell & System Tools\n")
    
    # Test 1: Get current directory
    print("1️⃣ Testing get_current_directory...")
    result = get_current_directory.invoke({})
    print(result)
    print()
    
    # Test 2: Execute shell command
    print("2️⃣ Testing execute_shell_command...")
    result = execute_shell_command.invoke({"command": "echo 'Hello from shell!'"})
    print(result)
    print()
    
    # Test 3: Get system info
    print("3️⃣ Testing get_system_info...")
    result = get_system_info.invoke({})
    print(result)
    print()
    
    # Test 4: Get environment variables (filtered)
    print("4️⃣ Testing get_environment_variables (filtered)...")
    result = get_environment_variables.invoke({"filter_pattern": "PATH"})
    print(result[:500] + "..." if len(result) > 500 else result)
    print()
    
    # Test 5: Change directory (test and revert)
    print("5️⃣ Testing change_directory...")
    original_dir = get_current_directory.invoke({})
    result = change_directory.invoke({"path": ".."})
    print(result)
    # Go back
    change_directory.invoke({"path": original_dir.split(": ")[1].split("\n")[0]})
    print()
    
    print("✅ All shell tools tested!")

if __name__ == "__main__":
    test_shell_tools()