import pandas as pd

from load_dataset import (
    discover_release_files,
    load_project,
)

from profile_dataset import (
    FEATURE_SUITES,
    TARGET_COLUMN,
)


DEDUPLICATION_SCOPES = [
    "global_project",
    "within_release",
]


def calculate_class_statistics(dataframe):
    """Return row count and class-distribution statistics."""

    total_rows = len(dataframe)

    defective_rows = int(
        (dataframe[TARGET_COLUMN] == 1).sum()
    )

    non_defective_rows = int(
        (dataframe[TARGET_COLUMN] == 0).sum()
    )

    defect_percentage = (
        defective_rows / total_rows * 100
        if total_rows > 0
        else 0.0
    )

    return {
        "rows": total_rows,
        "defective": defective_rows,
        "non_defective": non_defective_rows,
        "defect_percentage": defect_percentage,
    }


def deduplicate_project(
    dataframe,
    feature_columns,
    scope,
):
    """
    Deduplicate one project dataset using a specified scope.

    global_project:
        Remove duplicate feature + target combinations across
        all releases belonging to the project.

    within_release:
        Remove duplicate feature + target combinations only
        within the same release.
    """

    subset_columns = feature_columns + [TARGET_COLUMN]

    if scope == "global_project":
        return dataframe.drop_duplicates(
            subset=subset_columns
        ).copy()

    if scope == "within_release":
        return dataframe.drop_duplicates(
            subset=["release"] + subset_columns
        ).copy()

    raise ValueError(
        f"Unknown deduplication scope: {scope}"
    )


def investigate_duplicates():
    """
    Compare deduplication effects across projects,
    feature suites, and plausible scopes.
    """

    release_files = discover_release_files()

    result_rows = []

    print("=" * 80)
    print("DUPLICATE REMOVAL INVESTIGATION")
    print("=" * 80)

    for project_index, project_name in enumerate(
        release_files,
        start=1,
    ):
        print(
            f"[{project_index:>2}/{len(release_files)}] "
            f"Processing {project_name}"
        )

        project_dataframe = load_project(
            project_name,
            release_files=release_files,
        )

        original_statistics = calculate_class_statistics(
            project_dataframe
        )

        for suite_name, feature_columns in FEATURE_SUITES.items():
            for scope in DEDUPLICATION_SCOPES:
                deduplicated_dataframe = deduplicate_project(
                    project_dataframe,
                    feature_columns,
                    scope,
                )

                processed_statistics = calculate_class_statistics(
                    deduplicated_dataframe
                )

                rows_removed = (
                    original_statistics["rows"]
                    - processed_statistics["rows"]
                )

                percentage_removed = (
                    rows_removed
                    / original_statistics["rows"]
                    * 100
                    if original_statistics["rows"] > 0
                    else 0.0
                )

                result_rows.append(
                    {
                        "project": project_name,
                        "feature_suite": suite_name,
                        "scope": scope,
                        "original_rows": (
                            original_statistics["rows"]
                        ),
                        "processed_rows": (
                            processed_statistics["rows"]
                        ),
                        "rows_removed": rows_removed,
                        "percentage_removed": percentage_removed,
                        "original_defective": (
                            original_statistics["defective"]
                        ),
                        "processed_defective": (
                            processed_statistics["defective"]
                        ),
                        "original_defect_percentage": (
                            original_statistics[
                                "defect_percentage"
                            ]
                        ),
                        "processed_defect_percentage": (
                            processed_statistics[
                                "defect_percentage"
                            ]
                        ),
                    }
                )

    results = pd.DataFrame(result_rows)

    print("\n" + "=" * 80)
    print("AGGREGATE RESULTS")
    print("=" * 80)

    aggregate_results = (
        results
        .groupby(
            [
                "feature_suite",
                "scope",
            ]
        )
        .agg(
            original_rows=("original_rows", "sum"),
            processed_rows=("processed_rows", "sum"),
            rows_removed=("rows_removed", "sum"),
            original_defective=("original_defective", "sum"),
            processed_defective=("processed_defective", "sum"),
        )
        .reset_index()
    )

    aggregate_results["percentage_removed"] = (
        aggregate_results["rows_removed"]
        / aggregate_results["original_rows"]
        * 100
    )

    aggregate_results["processed_defect_percentage"] = (
        aggregate_results["processed_defective"]
        / aggregate_results["processed_rows"]
        * 100
    )

    print(
        aggregate_results.to_string(
            index=False,
            formatters={
                "percentage_removed": "{:.2f}%".format,
                "processed_defect_percentage": "{:.2f}%".format,
            },
        )
    )

    return results, aggregate_results


if __name__ == "__main__":
    investigate_duplicates()