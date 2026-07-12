from load_dataset import (
    REQUIRED_COLUMNS,
    discover_project_directories,
    discover_release_files,
    validate_release_columns,
)


EXPECTED_PROJECT_COUNT = 39
EXPECTED_RELEASE_COUNT = 275


def audit_dataset():
    """Audit the raw dataset structure and required schema."""

    project_directories = discover_project_directories()
    release_files = discover_release_files()

    project_count = len(project_directories)

    release_count = sum(
        len(files) for files in release_files.values()
    )

    releases_with_missing_columns = []

    for project_name, csv_files in release_files.items():
        for csv_path in csv_files:
            missing_columns = validate_release_columns(csv_path)

            if missing_columns:
                releases_with_missing_columns.append(
                    {
                        "project": project_name,
                        "release": csv_path.name,
                        "missing_columns": missing_columns,
                    }
                )

    print("=" * 60)
    print("SOFTWARE DEFECT PREDICTION DATASET AUDIT")
    print("=" * 60)

    print(f"\nRaw dataset directory:")
    print(project_directories[0].parent if project_directories else "N/A")

    print(f"\nProjects discovered: {project_count}")
    print(f"Expected projects:   {EXPECTED_PROJECT_COUNT}")

    print(f"\nReleases discovered: {release_count}")
    print(f"Expected releases:   {EXPECTED_RELEASE_COUNT}")

    print(f"\nRequired columns:")
    for column in REQUIRED_COLUMNS:
        print(f"  - {column}")

    print(
        "\nReleases missing required columns: "
        f"{len(releases_with_missing_columns)}"
    )

    print("\nValidation Results")

    projects_valid = project_count == EXPECTED_PROJECT_COUNT
    releases_valid = release_count == EXPECTED_RELEASE_COUNT
    schema_valid = len(releases_with_missing_columns) == 0

    print(
        f"Project count: {'PASS' if projects_valid else 'FAIL'}"
    )

    print(
        f"Release count: {'PASS' if releases_valid else 'FAIL'}"
    )

    print(
        f"Required schema: {'PASS' if schema_valid else 'FAIL'}"
    )

    if releases_with_missing_columns:
        print("\nSchema Problems:")

        for problem in releases_with_missing_columns:
            print(
                f"{problem['project']} / "
                f"{problem['release']} -> "
                f"{problem['missing_columns']}"
            )

    print("\n" + "=" * 60)

    return {
        "project_count": project_count,
        "release_count": release_count,
        "schema_problems": releases_with_missing_columns,
        "projects_valid": projects_valid,
        "releases_valid": releases_valid,
        "schema_valid": schema_valid,
    }


if __name__ == "__main__":
    audit_dataset()