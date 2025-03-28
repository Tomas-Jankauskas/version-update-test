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
        with open(file_path, "r") as f:
            content = f.read()
        
        # Get current date
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Create new entry
        new_entry = f"{new_version} ({today})\n{changelog_entry}\n\n"
        
        # First, make sure we find the header
        match = re.search(header_pattern, content)
        if not match:
            print(f"Could not find header pattern in {file_path}")
            return False
        
        # Find all version entries in the changelog
        version_pattern = r"(\d+\.\d+\.\d+) \(\d{4}-\d{2}-\d{2}\)"
        versions = re.findall(version_pattern, content)
        
        if not versions:
            # If no versions found, insert after header
            insert_position = match.end()
            updated_content = content[:insert_position] + "\n" + new_entry + content[insert_position:]
        else:
            # Find the first occurrence of the latest version
            latest_version = versions[0]
            latest_version_pattern = f"{latest_version} \\(\\d{{4}}-\\d{{2}}-\\d{{2}}\\)"
            latest_version_match = re.search(latest_version_pattern, content)
            
            if latest_version_match:
                # Insert the new entry before the latest version
                insert_position = latest_version_match.start()
                updated_content = content[:insert_position] + new_entry + content[insert_position:]
                print(f"Inserting new entry before existing version {latest_version}")
            else:
                # Fallback to inserting after header
                insert_position = match.end()
                updated_content = content[:insert_position] + "\n" + new_entry + content[insert_position:]
                print(f"Could not find latest version pattern, inserting after header")
        
        with open(file_path, "w") as f:
            f.write(updated_content)
            
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