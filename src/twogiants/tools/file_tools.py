"""File operation tools - Read, write, edit, list, delete files and directories."""

from langchain.tools import tool
import os
from pathlib import Path
from typing import Optional


@tool
def read_file(filepath: str) -> str:
    """Read the contents of a file.
    
    Args:
        filepath: Path to the file (relative or absolute)
    
    Returns:
        File contents as string, or error message
    
    Examples:
        read_file("README.md")
        read_file("src/main.py")
        read_file("/absolute/path/to/file.txt")
    """
    try:
        # Expand user home directory if present (~)
        filepath = os.path.expanduser(filepath)
        
        # Check if file exists
        if not os.path.exists(filepath):
            return f"❌ Error: File not found: {filepath}"
        
        # Check if it's actually a file (not a directory)
        if not os.path.isfile(filepath):
            return f"❌ Error: {filepath} is not a file"
        
        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get file size info
        size = os.path.getsize(filepath)
        lines = len(content.splitlines())
        
        return f"""✓ File: {filepath}
Size: {size} bytes | Lines: {lines}

{content}"""
    
    except PermissionError:
        return f"❌ Error: Permission denied to read {filepath}"
    
    except UnicodeDecodeError:
        return f"❌ Error: {filepath} is not a text file (binary content)"
    
    except Exception as e:
        return f"❌ Error reading {filepath}: {e}"


@tool
def write_file(filepath: str, content: str, overwrite: bool = False) -> str:
    """Write content to a new file.
    
    Args:
        filepath: Path where to create the file
        content: Content to write
        overwrite: If True, overwrite existing file. If False, fail if exists.
    
    Returns:
        Success message or error
    
    Examples:
        write_file("test.txt", "Hello world!")
        write_file("src/new_file.py", "print('hello')", overwrite=True)
    """
    try:
        filepath = os.path.expanduser(filepath)
        
        # Check if file exists and overwrite is False
        if os.path.exists(filepath) and not overwrite:
            return f"❌ Error: File already exists: {filepath}\nUse overwrite=True to replace it, or use edit_file to modify it."
        
        # Create parent directories if they don't exist
        parent_dir = os.path.dirname(filepath)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        size = os.path.getsize(filepath)
        lines = len(content.splitlines())
        
        return f"✓ Created {filepath}\nSize: {size} bytes | Lines: {lines}"
    
    except PermissionError:
        return f"❌ Error: Permission denied to write {filepath}"
    
    except Exception as e:
        return f"❌ Error writing {filepath}: {e}"


@tool
def edit_file(filepath: str, old_text: str, new_text: str) -> str:
    """Edit a file by replacing old_text with new_text.
    
    Args:
        filepath: Path to the file to edit
        old_text: Text to find and replace
        new_text: Replacement text
    
    Returns:
        Success message with number of replacements, or error
    
    Examples:
        edit_file("config.py", "DEBUG = False", "DEBUG = True")
        edit_file("README.md", "version 1.0", "version 1.1")
    
    Note:
        - Replaces ALL occurrences of old_text
        - Case-sensitive matching
        - Creates backup before editing (filename.bak)
    """
    try:
        filepath = os.path.expanduser(filepath)
        
        # Check if file exists
        if not os.path.exists(filepath):
            return f"❌ Error: File not found: {filepath}"
        
        if not os.path.isfile(filepath):
            return f"❌ Error: {filepath} is not a file"
        
        # Read current content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if old_text exists
        if old_text not in content:
            return f"❌ Error: Text not found in {filepath}\nSearched for: {old_text[:100]}..."
        
        # Create backup
        backup_path = filepath + '.bak'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Replace text
        new_content = content.replace(old_text, new_text)
        occurrences = content.count(old_text)
        
        # Write modified content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return f"""✓ Edited {filepath}
Replaced {occurrences} occurrence(s)
Backup saved: {backup_path}

Changes:
  - Old: {old_text[:50]}...
  + New: {new_text[:50]}..."""
    
    except PermissionError:
        return f"❌ Error: Permission denied to edit {filepath}"
    
    except UnicodeDecodeError:
        return f"❌ Error: {filepath} is not a text file"
    
    except Exception as e:
        return f"❌ Error editing {filepath}: {e}"


@tool
def list_directory(path: str = ".", recursive: bool = False, show_hidden: bool = False) -> str:
    """List contents of a directory.
    
    Args:
        path: Directory path (default: current directory)
        recursive: If True, list subdirectories recursively
        show_hidden: If True, show hidden files (starting with .)
    
    Returns:
        Formatted directory listing
    
    Examples:
        list_directory()
        list_directory("src")
        list_directory(".", recursive=True)
    """
    try:
        path = os.path.expanduser(path)
        
        # Check if directory exists
        if not os.path.exists(path):
            return f"❌ Error: Directory not found: {path}"
        
        if not os.path.isdir(path):
            return f"❌ Error: {path} is not a directory"
        
        output = [f"📁 Contents of: {os.path.abspath(path)}\n"]
        
        if recursive:
            # Recursive listing
            items = []
            for root, dirs, files in os.walk(path):
                # Filter hidden if needed
                if not show_hidden:
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    files = [f for f in files if not f.startswith('.')]
                
                level = root.replace(path, '').count(os.sep)
                indent = '  ' * level
                
                items.append(f"{indent}📁 {os.path.basename(root)}/")
                
                for file in sorted(files):
                    file_path = os.path.join(root, file)
                    size = os.path.getsize(file_path)
                    items.append(f"{indent}  📄 {file} ({size} bytes)")
            
            output.extend(items)
        
        else:
            # Non-recursive listing
            items = os.listdir(path)
            
            # Filter hidden if needed
            if not show_hidden:
                items = [item for item in items if not item.startswith('.')]
            
            items.sort()
            
            # Separate directories and files
            dirs = []
            files = []
            
            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    dirs.append(f"📁 {item}/")
                else:
                    size = os.path.getsize(full_path)
                    files.append(f"📄 {item} ({size} bytes)")
            
            # Display directories first, then files
            output.extend(dirs)
            output.extend(files)
            
            total = len(dirs) + len(files)
            output.append(f"\nTotal: {len(dirs)} directories, {len(files)} files")
        
        return '\n'.join(output)
    
    except PermissionError:
        return f"❌ Error: Permission denied to access {path}"
    
    except Exception as e:
        return f"❌ Error listing directory {path}: {e}"


@tool
def delete_file(filepath: str, confirm: bool = False) -> str:
    """Delete a file.
    
    ⚠️ WARNING: This operation cannot be undone!
    
    Args:
        filepath: Path to the file to delete
        confirm: Must be True to actually delete (safety check)
    
    Returns:
        Success message or error
    
    Examples:
        delete_file("temp.txt", confirm=True)
    
    Note:
        Requires confirm=True to prevent accidental deletions
    """
    try:
        if not confirm:
            return """⚠️ Deletion requires explicit confirmation.
Use: delete_file(filepath, confirm=True)

WARNING: This operation cannot be undone!"""
        
        filepath = os.path.expanduser(filepath)
        
        # Check if file exists
        if not os.path.exists(filepath):
            return f"❌ Error: File not found: {filepath}"
        
        if not os.path.isfile(filepath):
            return f"❌ Error: {filepath} is not a file (use a different method for directories)"
        
        # Get file info before deletion
        size = os.path.getsize(filepath)
        
        # Delete file
        os.remove(filepath)
        
        return f"✓ Deleted {filepath} ({size} bytes)"
    
    except PermissionError:
        return f"❌ Error: Permission denied to delete {filepath}"
    
    except Exception as e:
        return f"❌ Error deleting {filepath}: {e}"


@tool
def create_directory(path: str, parents: bool = True) -> str:
    """Create a new directory.
    
    Args:
        path: Directory path to create
        parents: If True, create parent directories as needed
    
    Returns:
        Success message or error
    
    Examples:
        create_directory("new_folder")
        create_directory("src/utils/helpers", parents=True)
    """
    try:
        path = os.path.expanduser(path)
        
        # Check if already exists
        if os.path.exists(path):
            if os.path.isdir(path):
                return f"ℹ️ Directory already exists: {path}"
            else:
                return f"❌ Error: {path} exists but is not a directory"
        
        # Create directory
        if parents:
            os.makedirs(path, exist_ok=True)
        else:
            os.mkdir(path)
        
        return f"✓ Created directory: {path}"
    
    except PermissionError:
        return f"❌ Error: Permission denied to create {path}"
    
    except Exception as e:
        return f"❌ Error creating directory {path}: {e}"