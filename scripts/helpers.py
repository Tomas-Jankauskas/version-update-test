#!/usr/bin/env python3
"""
Helper functions for version updating
"""

import re
import os
import anthropic
from typing import Optional, Tuple

def get_current_version(php_file_path: str) -> str:
    """
    Extract the current version from a PHP file.
    
    Args:
        php_file_path: Path to the PHP file
        
    Returns:
        The current version string (e.g., "1.0.2")
        
    Raises:
        ValueError: If the version cannot be extracted
    """
    with open(php_file_path, "r") as f:
        content = f.read()
    
    # Look for version in header comment
    version_match = re.search(r"Version:\s+([0-9]+\.[0-9]+\.[0-9]+)", content)
    if version_match:
        return version_match.group(1)
    
    # Alternatively, look for version in define statement
    define_match = re.search(r"define\(\s*'[\w_]+VERSION',\s*'([0-9]+\.[0-9]+\.[0-9]+)'\s*\)", content)
    if define_match:
        return define_match.group(1)
    
    raise ValueError(f"Could not extract version from {php_file_path}")

def increment_version(version: str) -> str:
    """
    Increment the patch version by 1.
    
    Args:
        version: Current version string (e.g., "1.0.2")
        
    Returns:
        New version string with patch version incremented (e.g., "1.0.3")
    """
    major, minor, patch = map(int, version.split("."))
    return f"{major}.{minor}.{patch + 1}"

def parse_version(version: str) -> Tuple[int, int, int]:
    """
    Parse a version string into its components.
    
    Args:
        version: Version string (e.g., "1.0.2")
        
    Returns:
        Tuple of (major, minor, patch) as integers
    """
    parts = version.split(".")
    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {version}")
    
    return tuple(map(int, parts))

def generate_changelog_with_claude(
    pr_title: str, 
    pr_description: str, 
    pr_changes: str, 
    pr_diff: str
) -> Optional[str]:
    """
    Generate a changelog entry using Claude AI.
    
    Args:
        pr_title: PR title
        pr_description: PR description
        pr_changes: List of changed files
        pr_diff: Detailed diff of changes
        
    Returns:
        Formatted changelog entry or None if API call fails
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Warning: ANTHROPIC_API_KEY not set, using PR title as changelog")
        clean_title = re.sub(r'\[release\]', '', pr_title, flags=re.IGNORECASE).strip()
        return f"- {clean_title}"
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Limit diff size to avoid exceeding context limits
        if len(pr_diff) > 10000:
            pr_diff = pr_diff[:10000] + "... [truncated]"
        
        system_prompt = """
        You are an expert at writing clear, concise changelog entries. 
        Based on the PR description, title, and code changes, write a well-formatted changelog entry.
        Keep your response focused only on the changelog entry text.
        Format as bullet points, starting each point with "- ".
        """

        message = f"""
        PR Title: {pr_title}
        PR Description: {pr_description}

        Files changed:
        {pr_changes}

        Code changes:
        {pr_diff}

        Please write a concise changelog entry describing these changes. Format as bullet points.
        """

        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": message}
            ]
        )

        return response.content[0].text.strip()
    
    except Exception as e:
        print(f"Error generating changelog with Claude: {str(e)}")
        clean_title = re.sub(r'\[release\]', '', pr_title, flags=re.IGNORECASE).strip()
        return f"- {clean_title}" 
