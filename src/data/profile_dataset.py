import numpy as np
import pandas as pd

from load_dataset import (
    REQUIRED_COLUMNS,
    discover_release_files,
    load_full_dataset,
)


FEATURE_COLUMNS = [
    column
    for column in REQUIRED_COLUMNS
    if column != "isDefective"
]

TARGET_COLUMN = "isDefective"


FEATURE_SUITES = {
    "LOC": [
        "LOC",
    ],
    "CK": [
        "WMC",
        "DIT",
        "NOC",
        "RFC",
        "LCOM5",
        "CBO",
    ],
    "OTHER": [
        "NPA",
        "NPM",
        "NLE",
        "CBOI",
        "CD",
    ],
    "CK_OTHER": [
        "WMC",
        "DIT",
        "NOC",
        "RFC",
        "LCOM5",
        "CBO",
        "NPA",
        "NPM",
        "NLE",
        "CBOI",
        "CD",
    ],
}


def calculate_class_distribution(dataframe):
    """Calculate target-class counts and percentages."""

    counts = (
        dataframe[TARGET_COLUMN]
        .value_counts()
        .sort_index()
    )

    percentages = (
        dataframe[TARGET_COLUMN]
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
    )

    return counts, percentages


def calculate_missing_values(dataframe):
    """Calculate missing values for reproduction columns."""

    return dataframe[REQUIRED_COLUMNS].isna().sum()


def calculate_infinite_values(dataframe):
    """Calculate infinite values for numerical features."""

    return pd.Series(
        {
            column: np.isinf(dataframe[column]).sum()
            for column in FEATURE_COLUMNS
        }
    )


def calculate_project_statistics(dataframe, release_files):
    """Calculate observations, defects, and releases per project."""

    project_statistics = (
        dataframe
        .groupby("project")
        .agg(
            observations=(TARGET_COLUMN, "size"),
            defective=(TARGET_COLUMN, "sum"),
        )
    )

    project_statistics["non_defective"] = (
        project_statistics["observations"]
        - project_statistics["defective"]
    )

    project_statistics["defect_percentage"] = (
        project_statistics["defective"]
        / project_statistics["observations"]
        * 100
    )

    project_statistics["releases"] = pd.Series(
        {
            project_name: len(csv_files)
            for project_name, csv_files in release_files.items()
        }
    )

    return project_statistics.sort_index()


def calculate_duplicate_statistics(dataframe):
    """
    Calculate duplicate counts under multiple plausible definitions.

    The original paper states that duplicate observations were removed
    but does not fully specify the duplicate-removal scope.
    """

    feature_and_target_columns = FEATURE_COLUMNS + [TARGET_COLUMN]

    full_row_duplicates = dataframe.duplicated(
        subset=feature_and_target_columns
    ).sum()

    feature_only_duplicates = dataframe.duplicated(
        subset=FEATURE_COLUMNS
    ).sum()

    within_project_duplicates = dataframe.duplicated(
        subset=["project"] + feature_and_target_columns
    ).sum()

    within_release_duplicates = dataframe.duplicated(
        subset=[
            "project",
            "release",
        ] + feature_and_target_columns
    ).sum()

    return {
        "global_features_and_target": int(full_row_duplicates),
        "global_features_only": int(feature_only_duplicates),
        "within_project_features_and_target": int(
            within_project_duplicates
        ),
        "within_release_features_and_target": int(
            within_release_duplicates
        ),
    }


def calculate_feature_suite_duplicates(dataframe):
    """
    Calculate duplicate counts for each RQ1 feature configuration.

    Duplicates are measured using the selected feature suite together
    with the target variable.
    """

    duplicate_statistics = {}

    for suite_name, feature_columns in FEATURE_SUITES.items():
        subset_columns = feature_columns + [TARGET_COLUMN]

        global_duplicates = dataframe.duplicated(
            subset=subset_columns
        ).sum()

        within_project_duplicates = dataframe.duplicated(
            subset=["project"] + subset_columns
        ).sum()

        within_release_duplicates = dataframe.duplicated(
            subset=[
                "project",
                "release",
            ] + subset_columns
        ).sum()

        duplicate_statistics[suite_name] = {
            "global": int(global_duplicates),
            "within_project": int(within_project_duplicates),
            "within_release": int(within_release_duplicates),
        }

    return duplicate_statistics


def profile_dataset():
    """Run a complete profile of the raw research dataset."""

    print("=" * 70)
    print("SOFTWARE DEFECT PREDICTION DATASET PROFILE")
    print("=" * 70)

    print("\nLoading dataset...")

    dataframe = load_full_dataset()
    release_files = discover_release_files()

    print("Dataset loaded successfully.")

    print(f"\nTotal observations: {len(dataframe):,}")
    print(f"Projects:           {dataframe['project'].nunique()}")
    print(f"Releases:           {dataframe['release'].nunique()}")

    counts, percentages = calculate_class_distribution(dataframe)

    print("\nCLASS DISTRIBUTION")
    print("-" * 70)

    for target_value in counts.index:
        label = (
            "Non-Defective"
            if target_value == 0
            else "Defective"
        )

        print(
            f"{label:<15} "
            f"{counts[target_value]:>10,} "
            f"({percentages[target_value]:.2f}%)"
        )

    missing_values = calculate_missing_values(dataframe)
    infinite_values = calculate_infinite_values(dataframe)

    print("\nDATA QUALITY")
    print("-" * 70)

    print(
        f"Missing values:  "
        f"{int(missing_values.sum()):,}"
    )

    print(
        f"Infinite values: "
        f"{int(infinite_values.sum()):,}"
    )

    duplicate_statistics = calculate_duplicate_statistics(dataframe)

    print("\nDUPLICATE ANALYSIS")
    print("-" * 70)

    for definition, count in duplicate_statistics.items():
        print(f"{definition:<45} {count:>10,}")

    feature_suite_duplicates = calculate_feature_suite_duplicates(
        dataframe
    )

    print("\nFEATURE-SUITE DUPLICATE ANALYSIS")
    print("-" * 70)

    for suite_name, statistics in feature_suite_duplicates.items():
        print(f"\n{suite_name}")

        for scope, count in statistics.items():
            remaining = len(dataframe) - count

            print(
                f"  {scope:<20} "
                f"duplicates={count:>10,} "
                f"remaining={remaining:>10,}"
            )

    project_statistics = calculate_project_statistics(
        dataframe,
        release_files,
    )

    print("\nPROJECT STATISTICS")
    print("-" * 70)

    print(
        project_statistics.to_string(
            formatters={
                "defect_percentage": "{:.2f}%".format,
            }
        )
    )

    print("\n" + "=" * 70)

    return {
        "dataframe": dataframe,
        "class_counts": counts,
        "class_percentages": percentages,
        "missing_values": missing_values,
        "infinite_values": infinite_values,
        "duplicate_statistics": duplicate_statistics,
        "feature_suite_duplicates": feature_suite_duplicates,
        "project_statistics": project_statistics,
    }


if __name__ == "__main__":
    profile_dataset()