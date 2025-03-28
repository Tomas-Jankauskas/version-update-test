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
    Update changelog file with a new entry AFTER the highest version
    
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
        version_pattern = re.compile(r"^(\d+\.\d+\.\d+) \(\d{4}-\d{2}-\d{2}\)")
        versions = []  # List to store all version entries [(line_number, version), ...]
        
        # First pass: Find the header
        for i, line in enumerate(lines):
            # Only check if we have at least 2 lines
            if i < len(lines) - 1:
                two_line_content = lines[i] + lines[i+1]
                if re.search(header_pattern, two_line_content):
                    header_found = True
                    header_line_index = i+1  # Set to the line after "========="
                    print(f"Header found at lines {i} and {i+1}")
                    break
                
        if not header_found:
            print(f"Could not find header pattern in {file_path}")
            return False
        
        # Second pass: Find all version entries
        print(f"Looking for all version entries after line {header_line_index}")
        for i in range(header_line_index + 1, len(lines)):
            match = version_pattern.match(lines[i])
            if match:
                version = match.group(1)
                versions.append((i, version))
                print(f"Found version entry at line {i}: {version}")
        
        if not versions:
            # No version entries found, insert right after the header
            insertion_index = header_line_index + 1
            # Skip empty lines
            while insertion_index < len(lines) and not lines[insertion_index].strip():
                insertion_index += 1
            print(f"No version entries found, inserting after header at line {insertion_index}")
        else:
            # Find the highest version - first sort by version number (semver)
            from helpers import parse_version
            
            # Sort versions by their numeric value (descending)
            sorted_versions = sorted(versions, key=lambda x: parse_version(x[1]), reverse=True)
            highest_version_line, highest_version = sorted_versions[0]
            print(f"Highest version found: {highest_version} at line {highest_version_line}")
            
            # Find where this version's entry ends (look for next version or EOF)
            # Start searching from the line after the version line
            end_of_entry = highest_version_line + 1
            while end_of_entry < len(lines):
                # If we hit another version entry, we've found the end
                if version_pattern.match(lines[end_of_entry]):
                    break
                # If we're at the end of the file, we've found the end
                end_of_entry += 1
            
            # Insert after the highest version's entry
            insertion_index = end_of_entry
            print(f"Inserting new version {new_version} after version {highest_version} at line {insertion_index}")
        
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