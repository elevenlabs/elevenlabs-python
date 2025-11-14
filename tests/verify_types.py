#!/usr/bin/env python3
"""
Script to verify all types in src/elevenlabs/types/ can be imported and instantiated.
Allows pydantic ValidationError but catches other errors (like circular imports).
Each type is tested in a separate Python process to avoid import cache issues.
"""
import subprocess
import sys
from pathlib import Path
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_class_name_from_file(file_path: Path) -> Optional[str]:
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


def verify_type_import_in_subprocess(module_name: str, class_name: str) -> Optional[str]:
    """
    Test importing and instantiating a type in a separate subprocess.
    Returns error_message if failed, None if successful.
    """
    # Get project root (parent of tests directory)
    project_root = Path(__file__).parent.parent

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
            cwd=str(project_root)
        )

        if result.returncode == 0:
            return None
        else:
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            return error_msg

    except subprocess.TimeoutExpired:
        return "Timeout: Import took longer than 10 seconds"
    except Exception as e:
        return f"Subprocess error: {str(e)}"


def main():
    # Get project root (parent of tests directory)
    project_root = Path(__file__).parent.parent
    types_dir = project_root / "src/elevenlabs/types"

    if not types_dir.exists():
        print(f"Error: {types_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    # Get all Python files
    py_files = sorted([f for f in types_dir.glob("*.py") if not f.name.startswith("__")])

    print(f"Testing {len(py_files)} type files in parallel...\n")

    failures = []
    successes = []

    # Test types in parallel for speed
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_file = {}

        for py_file in py_files:
            module_name = py_file.stem
            class_name = get_class_name_from_file(py_file)

            if class_name is None:
                continue  # Skip special files

            future = executor.submit(verify_type_import_in_subprocess, module_name, class_name)
            future_to_file[future] = (module_name, class_name)

        for future in as_completed(future_to_file):
            module_name, class_name = future_to_file[future]
            try:
                error = future.result()

                if error is None:
                    successes.append((module_name, class_name))
                    print(f"✓ {module_name}.{class_name}")
                else:
                    failures.append((module_name, class_name, error))
                    print(f"✗ {module_name}.{class_name}")

            except Exception as e:
                failures.append((module_name, class_name, f"Test execution failed: {str(e)}"))
                print(f"✗ {module_name}.{class_name}")

    # Print summary
    print(f"\n{'='*80}")
    print(f"Summary: {len(successes)} passed, {len(failures)} failed")
    print(f"{'='*80}")

    if failures:
        print("\nFailed imports:")
        for module_name, class_name, error in failures:
            print(f"\n{module_name}.{class_name}:")
            # Indent error messages
            for line in error.split('\n'):
                print(f"  {line}")
        sys.exit(1)
    else:
        print("\nAll types can be imported successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
