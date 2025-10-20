#!/usr/bin/env python3
"""
CryptoSage - Cleanup Script
Xoá tất cả các file không cần thiết (Cross-platform)
"""

import os
import shutil
from pathlib import Path

# Colors
class Colors:
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    NC = '\033[0m'

def print_header():
    """Print header"""
    print(f"\n{Colors.BLUE}╔════════════════════════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}║              CryptoSage - Cleanup Script                   ║{Colors.NC}")
    print(f"{Colors.BLUE}╚════════════════════════════════════════════════════════════╝{Colors.NC}\n")

def delete_item(path, description):
    """Delete a file or directory"""
    try:
        if isinstance(path, str):
            path = Path(path)
        
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            print(f"{Colors.GREEN}✓{Colors.NC} Deleted: {description}")
            return True
    except Exception as e:
        print(f"  Warning: Could not delete {description}: {e}")
    return False

def delete_pattern(pattern, description):
    """Delete files matching pattern"""
    count = 0
    try:
        for path in Path(".").rglob(pattern):
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                count += 1
            except Exception as e:
                print(f"  Warning: Could not delete {path}: {e}")
        
        if count > 0:
            print(f"{Colors.GREEN}✓{Colors.NC} Deleted: {description} ({count} items)")
            return count
    except Exception as e:
        print(f"  Warning: Error processing {pattern}: {e}")
    
    return 0

def main():
    """Main cleanup function"""
    print_header()
    
    print(f"{Colors.YELLOW}🧹 Cleaning up project...{Colors.NC}\n")
    
    deleted = 0
    
    # Delete Python cache directories
    deleted += delete_pattern("__pycache__", "Python cache directories")
    deleted += delete_pattern(".pytest_cache", "Pytest cache directories")
    deleted += delete_pattern("*.egg-info", "Egg info directories")
    
    # Delete compiled Python files
    deleted += delete_pattern("*.pyc", "Compiled Python files")
    deleted += delete_pattern("*.pyo", "Optimized Python files")
    deleted += delete_pattern("*.pyd", "Python DLL files")
    
    # Delete log files
    deleted += delete_pattern("*.log", "Log files")
    
    # Delete temporary files
    deleted += delete_pattern("*.tmp", "Temporary files")
    deleted += delete_pattern("*.temp", "Temporary files")
    deleted += delete_pattern("*.bak", "Backup files")
    deleted += delete_pattern("*~", "Backup files")
    
    # Delete OS files
    deleted += delete_pattern(".DS_Store", "macOS system files")
    deleted += delete_pattern("Thumbs.db", "Windows thumbnail files")
    
    # Delete cache
    deleted += delete_pattern(".cache", "Cache directories")
    deleted += delete_pattern("*.cache", "Cache files")
    
    # Delete mypy cache
    deleted += delete_pattern(".mypy_cache", "Mypy cache")
    deleted += delete_pattern(".dmypy.json", "Mypy config")
    
    print(f"\n{Colors.GREEN}╔════════════════════════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.GREEN}║                  ✓ Cleanup Complete!                       ║{Colors.NC}")
    print(f"{Colors.GREEN}╚════════════════════════════════════════════════════════════╝{Colors.NC}\n")
    
    print(f"{Colors.BLUE}Summary:{Colors.NC}")
    print(f"  {Colors.GREEN}✓{Colors.NC} Total items deleted: {deleted}\n")
    
    # Calculate disk usage
    try:
        total_size = sum(f.stat().st_size for f in Path(".").rglob("*") if f.is_file())
        size_mb = total_size / (1024 * 1024)
        print(f"{Colors.BLUE}Disk Usage:{Colors.NC}")
        print(f"  Project size: {size_mb:.2f} MB\n")
    except Exception as e:
        print(f"  Warning: Could not calculate disk usage: {e}\n")
    
    print(f"{Colors.YELLOW}💡 Tips:{Colors.NC}")
    print("  • Run this script regularly to keep project clean")
    print("  • Safe to run - only deletes cache and temporary files")
    print("  • Does not delete source code or data\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Cleanup cancelled{Colors.NC}")
    except Exception as e:
        print(f"{Colors.YELLOW}Error: {e}{Colors.NC}")

