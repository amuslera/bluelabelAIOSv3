#!/usr/bin/env python3
"""
Script to fix Python 3.10+ union type syntax to Python 3.9 compatible syntax.
Converts 'Optional[type]' to 'Optional[type]' and 'Dict[str, type]' to 'Dict[str, type]' etc.
"""

import re
import sys
from pathlib import Path


def fix_union_types_in_file(file_path: Path) -> bool:
    """Fix union types in a single file. Returns True if changes were made."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix typing imports first
        if 'from typing import' in content:
            # Add missing imports
            import_line = re.search(r'from typing import Dict, List, Optional, Tuple, content, n
            if import_line:
                imports = import_line.group(1)
                needed_imports = set()
                
                # Check what imports we need
                if 'Dict[' in content.lower() or 'Dict[' in content:
                    needed_imports.add('Dict')
                if 'List[' in content.lower() or 'List[' in content:
                    needed_imports.add('List')
                if '| None' in content or 'Optional[' in content:
                    needed_imports.add('Optional')
                if 'Tuple[' in content.lower() or 'Tuple[' in content:
                    needed_imports.add('Tuple')
                
                # Add missing imports
                current_imports = set(re.findall(r'\b\w+\b', imports))
                missing_imports = needed_imports - current_imports
                
                if missing_imports:
                    all_imports = sorted(current_imports | missing_imports)
                    new_import_line = f"from typing import Dict, List, Optional, Tuple, content, n
                    content = re.sub(
                        r'from typing import Dict, List, Optional, Tuple, content, n
                        new_import_line,
                        content
                    )
        
        # Fix union types: Optional[type] -> Optional[type]
        # Match patterns like: Optional[str], Optional[datetime], etc.
        union_pattern = r'\b([A-Za-z_][A-Za-z0-9_]*(?:\[[^\]]+\])?)\s*\|\s*None\b'
        content = re.sub(union_pattern, r'Optional[\1]', content)
        
        # Fix Dict[key, value] -> Dict[key, value]
        content = re.sub(r'\bdict\[', 'Dict[', content)
        
        # Fix List[type] -> List[type]
        content = re.sub(r'\blist\[', 'List[', content)
        
        # Fix Tuple[type] -> Tuple[type]
        content = re.sub(r'\btuple\[', 'Tuple[', content)
        
        # Fix Set[type] -> Set[type] (if any)
        content = re.sub(r'\bset\[', 'Set[', content)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Fix union types in all Python files in the project."""
    project_root = Path(__file__).parent
    
    # Find all Python files
    python_files = list(project_root.rglob("*.py"))
    
    # Exclude venv and other directories
    excluded_dirs = {'venv', '__pycache__', '.git', 'node_modules'}
    python_files = [
        f for f in python_files 
        if not any(excluded in f.parts for excluded in excluded_dirs)
    ]
    
    fixed_count = 0
    
    for py_file in python_files:
        if fix_union_types_in_file(py_file):
            fixed_count += 1
    
    print(f"\nProcessed {len(python_files)} Python files")
    print(f"Fixed {fixed_count} files")


if __name__ == "__main__":
    main()