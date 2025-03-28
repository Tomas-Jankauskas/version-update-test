#!/usr/bin/env python3
"""
Helper functions for version updating
"""

import re
from typing import Tuple

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
