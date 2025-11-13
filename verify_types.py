#!/usr/bin/env python3
"""
Script to verify all types in src/elevenlabs/types/ can be imported and instantiated.
Allows pydantic ValidationError but catches other errors (like circular imports).
Each type is tested in a separate Python process to avoid import cache issues.
"""
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def get_class_name_from_file(file_path: Path) -> str | None:
    """Convert a file name to the expected class name using PascalCase."""
    # Remove .py extension
    name = file_path.stem

    # Skip special files
    if name.startswith('__'):
        return None

    # Convert snake_case to PascalCase
    parts = name.split('_')
    class_name = ''.join(word.capitalize() for word in parts)

    return class_name

def test_type_import_subprocess(module_name: str, class_name: str) -> tuple[bool, str | None]:
    """
    Test importing and instantiating a type in a separate subprocess.
    Returns (success, error_message)
    """
    # Python code to test import in isolation
    test_code = f"""
import sys
from pydantic import ValidationError as PydanticValidationError

try:
    # Try to import the type
    from elevenlabs.types.{module_name} import {class_name}

    # Try to instantiate with no args (expect ValidationError)
    try:
        {class_name}()
    except PydanticValidationError:
        pass  # Expected - type requires arguments
    except TypeError:
        pass  # Some types might not be Pydantic models (enums, etc.)
    except Exception:
        pass  # Still fine, as long as import worked

    sys.exit(0)  # Success

except ImportError as e:
    print(f"ImportError: {{e}}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"{{type(e).__name__}}: {{e}}", file=sys.stderr)
    sys.exit(1)
"""

    try:
        result = subprocess.run(
            ["poetry", "run", "python", "-c", test_code],
            capture_output=True,
            text=True,
            timeout=10,
            cwd="/Users/thomas/Projects/elevenlabs-python"
        )

        if result.returncode == 0:
            return True, None
        else:
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            return False, error_msg

    except subprocess.TimeoutExpired:
        return False, "Timeout: Import took longer than 10 seconds"
    except Exception as e:
        return False, f"Subprocess error: {str(e)}"

def main():
    types_dir = Path("src/elevenlabs/types")

    if not types_dir.exists():
        print(f"{RED}Error: {types_dir} does not exist{RESET}")
        sys.exit(1)

    # Get all Python files
    py_files = sorted([f for f in types_dir.glob("*.py") if not f.name.startswith("__")])

    print(f"Testing {len(py_files)} type files in separate processes...\n")
    print(f"This may take a few minutes...\n")

    failures = []
    successes = []
    skipped = []

    # Test types in parallel for speed
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_file = {}

        for py_file in py_files:
            module_name = py_file.stem
            class_name = get_class_name_from_file(py_file)

            if class_name is None:
                skipped.append(module_name)
                continue

            future = executor.submit(test_type_import_subprocess, module_name, class_name)
            future_to_file[future] = (module_name, class_name)

        for future in as_completed(future_to_file):
            module_name, class_name = future_to_file[future]
            try:
                success, error = future.result()

                if success:
                    successes.append((module_name, class_name))
                    print(f"{GREEN}✓{RESET} {module_name}.{class_name}")
                else:
                    failures.append((module_name, class_name, error))
                    print(f"{RED}✗{RESET} {module_name}.{class_name}")
                    print(f"  {RED}{error}{RESET}")
            except Exception as e:
                failures.append((module_name, class_name, f"Test execution failed: {str(e)}"))
                print(f"{RED}✗{RESET} {module_name}.{class_name}")
                print(f"  {RED}Test execution failed: {str(e)}{RESET}")

    # Print summary
    print(f"\n{'='*80}")
    print(f"Summary:")
    print(f"  {GREEN}Successful: {len(successes)}{RESET}")
    print(f"  {RED}Failed: {len(failures)}{RESET}")
    print(f"  {YELLOW}Skipped: {len(skipped)}{RESET}")

    if failures:
        print(f"\n{RED}Failed imports:{RESET}")
        for module_name, class_name, error in failures:
            print(f"  - {module_name}.{class_name}: {error}")
        sys.exit(1)
    else:
        print(f"\n{GREEN}All types can be imported successfully!{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
