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
from helpers import get_current_version, increment_version, generate_changelog_with_claude

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
        with open(file_path, "r") as f:
            content = f.read()
        
        # Get current date
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Create new entry
        new_entry = f"{new_version} ({today})\n{changelog_entry}\n\n"
        
        # Find where to insert the new entry
        match = re.search(header_pattern, content)
        if match:
            insert_position = match.end()
            updated_content = content[:insert_position] + "\n" + new_entry + content[insert_position:]
            
            with open(file_path, "w") as f:
                f.write(updated_content)
                
            print(f"Updated changelog in {file_path}")
            return True
        else:
            print(f"Could not find header pattern in {file_path}")
            return False
            
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
    pr_diff = ""
    
    if os.path.exists("pr_description.txt"):
        with open("pr_description.txt", "r") as f:
            pr_description = f.read()
            
    if os.path.exists("pr_changes.txt"):
        with open("pr_changes.txt", "r") as f:
            pr_changes = f.read()
            print(f"Found checklist items/changes: {pr_changes}")
            
    if os.path.exists("pr_diff.txt"):
        with open("pr_diff.txt", "r") as f:
            pr_diff = f.read()
    
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
    
    # Use the extracted checklist items from the PR if available
    if pr_changes and pr_changes.strip():
        print("Using extracted checklist items for changelog")
        changelog_entry = pr_changes
    else:
        # Fall back to generating changelog with Claude
        print("No checklist items found, generating changelog with Claude")
        changelog_entry = generate_changelog_with_claude(
            pr_title, pr_description, pr_changes, pr_diff
        )
        
        if not changelog_entry:
            print("Failed to generate changelog entry, using PR title as fallback")
            clean_title = re.sub(r'\[release\]', '', pr_title, flags=re.IGNORECASE).strip()
            changelog_entry = f"- {clean_title}"
    
    # Update version in files
    for file_config in config.get("files", []):
        file_path = file_config.get("path")
        file_type = file_config.get("type")
        
        if file_type == "php":
            patterns = file_config.get("patterns", [])
            update_version_in_file(file_path, patterns, new_version)
        elif file_type == "changelog":
            header_pattern = file_config.get("header_pattern", "")
            update_changelog(file_path, header_pattern, changelog_entry, new_version)
    
    print("Version update completed successfully")

if __name__ == "__main__":
    main()