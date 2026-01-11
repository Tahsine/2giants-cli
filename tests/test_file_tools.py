"""Test file tools."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from twogiants.tools.file_tools import (
    read_file,
    write_file,
    edit_file,
    list_directory,
    delete_file,
    create_directory
)

def test_file_tools():
    """Test all file tools."""
    
    print("🧪 Testing File Tools\n")
    
    # Test 1: Create directory
    print("1️⃣ Testing create_directory...")
    result = create_directory.invoke({"path": "test_data"})
    print(result)
    print()
    
    # Test 2: Write file
    print("2️⃣ Testing write_file...")
    result = write_file.invoke({
        "filepath": "test_data/hello.txt",
        "content": "Hello from 2Giants!\nThis is a test file."
    })
    print(result)
    print()
    
    # Test 3: Read file
    print("3️⃣ Testing read_file...")
    result = read_file.invoke({"filepath": "test_data/hello.txt"})
    print(result)
    print()
    
    # Test 4: Edit file
    print("4️⃣ Testing edit_file...")
    result = edit_file.invoke({
        "filepath": "test_data/hello.txt",
        "old_text": "test file",
        "new_text": "modified test file"
    })
    print(result)
    print()
    
    # Test 5: List directory
    print("5️⃣ Testing list_directory...")
    result = list_directory.invoke({"path": "test_data"})
    print(result)
    print()
    
    # Test 6: Delete file
    print("6️⃣ Testing delete_file...")
    result = delete_file.invoke({
        "filepath": "test_data/hello.txt",
        "confirm": True
    })
    print(result)
    print()
    
    print("✅ All file tools tested!")

if __name__ == "__main__":
    test_file_tools()