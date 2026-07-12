from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

REQUIRED_COLUMNS = [
    "LOC",
    "LCOM5",
    "NLE",
    "CBO",
    "CBOI",
    "CD",
    "DIT",
    "NOC",
    "NPA",
    "NPM",
    "RFC",
    "WMC",
    "isDefective",
]


def discover_project_directories(raw_data_dir=RAW_DATA_DIR):
    """Return all project directories in the raw dataset."""

    if not raw_data_dir.exists():
        raise FileNotFoundError(
            f"Raw dataset directory does not exist: {raw_data_dir}"
        )

    project_directories = sorted(
        path for path in raw_data_dir.iterdir() if path.is_dir()
    )

    return project_directories


def discover_release_files(raw_data_dir=RAW_DATA_DIR):
    """Return all CSV release files grouped by project."""

    project_directories = discover_project_directories(raw_data_dir)

    release_files = {}

    for project_directory in project_directories:
        csv_files = sorted(project_directory.glob("*.csv"))
        release_files[project_directory.name] = csv_files

    return release_files


def validate_release_columns(csv_path):
    """Check whether a release contains all required columns."""

    columns = pd.read_csv(csv_path, nrows=0).columns

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in columns
    ]

    return missing_columns


def load_release(csv_path):
    """Load the required columns from one release CSV."""

    missing_columns = validate_release_columns(csv_path)

    if missing_columns:
        raise ValueError(
            f"{csv_path} is missing required columns: {missing_columns}"
        )

    dataframe = pd.read_csv(
        csv_path,
        usecols=REQUIRED_COLUMNS,
    )

    return dataframe
def load_project(project_name, release_files=None):
    """Load and combine all releases belonging to one project."""

    if release_files is None:
        release_files = discover_release_files()

    if project_name not in release_files:
        raise ValueError(f"Unknown project: {project_name}")

    project_frames = []

    for csv_path in release_files[project_name]:
        dataframe = load_release(csv_path)

        dataframe["project"] = project_name
        dataframe["release"] = csv_path.stem

        project_frames.append(dataframe)

    if not project_frames:
        raise ValueError(f"No release CSV files found for: {project_name}")

    return pd.concat(project_frames, ignore_index=True)


def load_full_dataset():
    """Load and combine all projects and releases."""

    release_files = discover_release_files()
    dataset_frames = []

    for project_name in release_files:
        project_dataframe = load_project(
            project_name,
            release_files=release_files,
        )

        dataset_frames.append(project_dataframe)

    if not dataset_frames:
        raise ValueError("No dataset files were loaded.")

    return pd.concat(dataset_frames, ignore_index=True)