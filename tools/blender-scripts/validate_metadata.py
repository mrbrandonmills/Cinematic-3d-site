#!/usr/bin/env python3
"""
Metadata Validator
Validates asset metadata against schema
Usage: python validate_metadata.py assets/meta/station-home.json
"""

import json
import sys
from pathlib import Path
import jsonschema


def load_schema(schema_path):
    """Load the JSON schema"""
    with open(schema_path) as f:
        return json.load(f)


def load_metadata(metadata_path):
    """Load asset metadata"""
    with open(metadata_path) as f:
        return json.load(f)


def validate_metadata(metadata, schema):
    """Validate metadata against schema"""
    errors = []

    try:
        jsonschema.validate(instance=metadata, schema=schema)
        return True, []

    except jsonschema.ValidationError as e:
        errors.append(f"Validation error: {e.message}")
        return False, errors

    except jsonschema.SchemaError as e:
        errors.append(f"Schema error: {e.message}")
        return False, errors


def check_file_exists(metadata, project_root):
    """Check if referenced GLB file exists"""
    file_path = metadata.get('file', '')
    full_path = project_root / 'assets' / file_path

    if not full_path.exists():
        return False, f"GLB file not found: {full_path}"

    return True, None


def check_filesize_matches(metadata, project_root):
    """Check if metadata filesize matches actual file"""
    file_path = metadata.get('file', '')
    full_path = project_root / 'assets' / file_path

    if not full_path.exists():
        return True, None  # Already caught by file exists check

    actual_size = full_path.stat().st_size
    metadata_size = metadata.get('metadata', {}).get('fileSize', 0)

    tolerance = 1024  # 1KB tolerance
    if abs(actual_size - metadata_size) > tolerance:
        return False, f"File size mismatch: actual={actual_size}, metadata={metadata_size}"

    return True, None


def main():
    """Main execution"""
    if len(sys.argv) < 2:
        print("Usage: python validate_metadata.py <metadata-file.json>")
        print("Example: python validate_metadata.py assets/meta/station-home.json")
        sys.exit(1)

    metadata_path = Path(sys.argv[1])

    if not metadata_path.exists():
        print(f"✗ Error: File not found: {metadata_path}")
        sys.exit(1)

    # Find project root and schema
    script_dir = Path(__file__).parent.absolute()
    project_root = script_dir.parent.parent
    schema_path = project_root / "assets" / "meta" / "asset-schema.json"

    if not schema_path.exists():
        print(f"✗ Error: Schema not found: {schema_path}")
        sys.exit(1)

    print(f"\n{'='*70}")
    print(f"Validating: {metadata_path.name}")
    print(f"{'='*70}\n")

    # Load files
    try:
        schema = load_schema(schema_path)
        metadata = load_metadata(metadata_path)
    except json.JSONDecodeError as e:
        print(f"✗ JSON parse error: {e}")
        sys.exit(1)

    # Validation checks
    checks = []
    all_passed = True

    # 1. Schema validation
    valid, errors = validate_metadata(metadata, schema)
    if valid:
        checks.append(("✓", "Schema validation", "Passed"))
    else:
        checks.append(("✗", "Schema validation", f"Failed: {', '.join(errors)}"))
        all_passed = False

    # 2. GLB file exists
    exists, error = check_file_exists(metadata, project_root)
    if exists:
        checks.append(("✓", "GLB file exists", "Passed"))
    else:
        checks.append(("✗", "GLB file exists", f"Failed: {error}"))
        all_passed = False

    # 3. File size matches
    matches, error = check_filesize_matches(metadata, project_root)
    if matches:
        checks.append(("✓", "File size matches", "Passed"))
    else:
        checks.append(("✗", "File size matches", f"Failed: {error}"))
        all_passed = False

    # 4. Required fields check
    required_fields = ['id', 'category', 'file', 'section']
    missing_fields = [f for f in required_fields if f not in metadata]

    if not missing_fields:
        checks.append(("✓", "Required fields", "All present"))
    else:
        checks.append(("✗", "Required fields", f"Missing: {', '.join(missing_fields)}"))
        all_passed = False

    # Print results
    for symbol, check_name, result in checks:
        print(f"{symbol} {check_name}: {result}")

    # Print metadata summary
    print(f"\n{'='*70}")
    print("Metadata Summary")
    print(f"{'='*70}")
    print(f"ID: {metadata.get('id', 'N/A')}")
    print(f"Category: {metadata.get('category', 'N/A')}")
    print(f"Section: {metadata.get('section', 'N/A')}")
    print(f"File: {metadata.get('file', 'N/A')}")

    if 'metadata' in metadata:
        meta = metadata['metadata']
        print(f"Polycount: {meta.get('polycount', 'N/A'):,}")
        print(f"File size: {meta.get('fileSize', 0) / 1024:.1f} KB")
        print(f"Version: {meta.get('version', 'N/A')}")

    print(f"{'='*70}\n")

    if all_passed:
        print("✓ All validation checks passed!\n")
        sys.exit(0)
    else:
        print("✗ Some validation checks failed\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
