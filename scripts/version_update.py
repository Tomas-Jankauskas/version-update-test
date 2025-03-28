#!/usr/bin/env python3
"""
Version Update Script

This script updates version numbers in PHP files and adds changelog entries
based on PR information.
"""

import os
import re
import sys
import yaml
import datetime
from helpers import get_current_version, increment_version

def load_config(config_path="version-update-config.yml"):
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to the config file
        
    Returns:
        Dict with configuration
    """
    try:
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        sys.exit(1)

def update_version_in_file(file_path, patterns, new_version):
    """
    Update version in a file using the provided patterns
    
    Args:
        file_path: Path to the file to update
        patterns: List of search/replace patterns
        new_version: New version string to use in replacements
    """
    try:
        with open(file_path, "r") as f:
            content = f.read()
            
        for pattern in patterns:
            search = pattern.get("search")
            replace_template = pattern.get("replace")
            
            if search and replace_template:
                replace = replace_template.replace("{{new_version}}", new_version)
                content = re.sub(search, replace, content)
        
        with open(file_path, "w") as f:
            f.write(content)
            
        print(f"Updated version in {file_path} to {new_version}")
    except Exception as e:
        print(f"Error updating version in {file_path}: {str(e)}")
        return False
    
    return True

def update_changelog(file_path, header_pattern, changelog_entry, new_version):
    """
    Update changelog file with a new entry
    
    Args:
        file_path: Path to the changelog file
        header_pattern: Regular expression to find where to insert the new entry
        changelog_entry: The new changelog entry text
        new_version: New version string
    """
    try:
        # Read file contents as lines
        with open(file_path, "r") as f:
            lines = f.readlines()
        
        # Get current date
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Create new entry
        new_entry_lines = [f"{new_version} ({today})\n"]
        for line in changelog_entry.strip().split('\n'):
            new_entry_lines.append(f"{line}\n")
        new_entry_lines.append("\n")  # Add extra newline for spacing
        
        # Process the file
        header_found = False
        header_line_index = -1
        first_version_line_index = -1
        version_pattern = re.compile(r"^(\d+\.\d+\.\d+) \(\d{4}-\d{2}-\d{2}\)")
        
        # First pass: Find the header
        for i, line in enumerate(lines):
            # Check for header pattern across 2 lines
            if i < len(lines) - 1 and re.search(header_pattern, line + lines[i+1]):
                header_found = True
                header_line_index = i+1  # Set to the line after "========="
                print(f"Header found at line {i} and {i+1}")
                break
                
        if not header_found:
            print(f"Could not find header pattern in {file_path}")
            return False
                
        # Second pass: Find the first version entry after the header
        for i in range(header_line_index + 1, len(lines)):
            if version_pattern.match(lines[i]):
                first_version_line_index = i
                print(f"Found first version entry at line {i}: {lines[i].strip()}")
                break
        
        # Decide where to insert the new entry
        if first_version_line_index != -1:
            # Insert before the first version entry
            insertion_index = first_version_line_index
            print(f"Inserting new version {new_version} before line {insertion_index}")
        else:
            # No version entries found, insert right after the header
            # Usually there should be at least one empty line after the header
            # Look for the first non-empty line after the header
            insertion_index = header_line_index + 1
            while insertion_index < len(lines) and not lines[insertion_index].strip():
                insertion_index += 1
            print(f"No version entries found, inserting after header at line {insertion_index}")
        
        # Insert the new entry
        updated_lines = lines[:insertion_index] + new_entry_lines + lines[insertion_index:]
        
        # Write the updated content back to the file
        with open(file_path, "w") as f:
            f.writelines(updated_lines)
        
        print(f"Updated changelog in {file_path}")
        return True
    
    except Exception as e:
        print(f"Error updating changelog in {file_path}: {str(e)}")
        return False

def main():
    # Load configuration
    config = load_config()
    if not config:
        print("Could not load configuration")
        sys.exit(1)
    
    # Check if this is a release PR - case-insensitive check
    pr_title = os.environ.get("PR_TITLE", "")
    if not re.search(r'^\[release\]', pr_title, re.IGNORECASE):
        print(f"Not a release PR ('{pr_title}'), skipping version update")
        sys.exit(0)
    
    # Get PR information
    pr_description = ""
    pr_changes = ""
    
    if os.path.exists("pr_description.txt"):
        with open("pr_description.txt", "r") as f:
            pr_description = f.read()
            
    if os.path.exists("pr_changes.txt"):
        with open("pr_changes.txt", "r") as f:
            pr_changes = f.read()
            print(f"Found checklist items/changes: {pr_changes}")
    
    # Find main PHP file to get current version
    main_php_file = None
    for file_config in config.get("files", []):
        if file_config.get("type") == "php":
            main_php_file = file_config.get("path")
            break
    
    if not main_php_file:
        print("No PHP file specified in config")
        sys.exit(1)
    
    # Get current version and calculate new version
    try:
        current_version = get_current_version(main_php_file)
        new_version = increment_version(current_version)
        print(f"Current version: {current_version}")
        print(f"New version: {new_version}")
    except Exception as e:
        print(f"Error getting version: {str(e)}")
        sys.exit(1)
    
    # Generate changelog entry - use checklist items if available, otherwise use PR title
    if pr_changes and pr_changes.strip():
        print("Using extracted checklist items for changelog")
        changelog_entry = pr_changes
    else:
        print("No checklist items found, using PR title")
        clean_title = re.sub(r'\[release\]', '', pr_title, flags=re.IGNORECASE).strip()
        changelog_entry = f"- {clean_title}"
    
    # Update version in files
    for file_config in config.get("files", []):
        file_path = file_config.get("path")
        file_type = file_config.get("type")
        needs_description = file_config.get("needs_description", True)  # Default to True for backwards compatibility
        
        if file_type == "php":
            patterns = file_config.get("patterns", [])
            update_version_in_file(file_path, patterns, new_version)
        elif file_type == "changelog" and needs_description:
            header_pattern = file_config.get("header_pattern", "")
            update_changelog(file_path, header_pattern, changelog_entry, new_version)
        elif file_type == "changelog" and not needs_description:
            print(f"Skipping changelog update for {file_path} as needs_description is set to false")
    
    print("Version update completed successfully")

if __name__ == "__main__":
    main()