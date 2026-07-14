# Reproduction Blueprint

## Base Study

**Title:** Source Code Metrics for Software Defects Prediction

This project independently reproduces and extends the experiments reported in the base study.

The reproduction aims to:

1. Reconstruct the original experimental methodology.
2. Reproduce the reported machine learning experiments.
3. Compare reproduced findings with the published results.
4. Document methodological ambiguities and reproducibility challenges.
5. Extend the study through explainability and feature explanation analysis.

---

## Dataset

The official research dataset contains:

- 39 open-source Java projects.
- 275 software releases.
- 702,023 class-level observations.
- 12 source-code metrics.
- Binary target variable: `isDefective`.

### Target Variable

`isDefective`

- `0` = Non-defective
- `1` = Defective

### Raw Class Distribution

| Class | Observations | Percentage |
|---|---:|---:|
| Non-defective | 677,607 | 96.52% |
| Defective | 24,416 | 3.48% |

The raw dataset is therefore highly class-imbalanced.

---

## Dataset Validation

The implemented dataset validation pipeline confirmed:

- 39 project directories.
- 275 release CSV files.
- All required source-code metrics are present.
- The target variable is present in every release.
- No missing values exist in the reproduction features.
- No infinite values exist in the reproduction features.

---

## Feature Configurations

### LOC

- LOC

### CK

- WMC
- DIT
- NOC
- RFC
- LCOM5
- CBO

### OTHER

- NPA
- NPM
- NLE
- CBOI
- CD

### CK + OTHER

- WMC
- DIT
- NOC
- RFC
- LCOM5
- CBO
- NPA
- NPM
- NLE
- CBOI
- CD

LOC is treated as a separate baseline configuration and is not included in CK + OTHER.

---

## Original Classifiers

The original study evaluates:

- Naive Bayes
- Decision Tree
- Random Forest

The exact implementation-level hyperparameters are not fully specified in the paper.

---

## Dataset Hierarchy

The dataset has three conceptual levels:

```text
39 Projects
    ↓
275 Releases
    ↓
702,023 Class-Level Observations
The same or similar source-code entities may occur across multiple releases.

This hierarchical structure must be considered when interpreting duplicate removal and experimental validation.

Duplicate Removal

The original study states that duplicate observations were removed as a limited approach to reducing class imbalance.

However, the exact duplicate-removal procedure is not sufficiently specified.

The following methodological decisions remain ambiguous:

Whether duplicates were identified globally or separately per project.
Whether duplicates were removed separately within each release.
Whether duplicate detection used all source-code metrics or only the active feature configuration.
Whether the target variable was included when identifying duplicate observations.
Initial Duplicate Analysis

Duplicate observations were measured under multiple plausible definitions using all 12 source-code metrics.

Duplicate Definition Duplicate Observations
Global features + target 488,101
Global features only 495,207
Within project + features + target 480,551
Within release + features + target 185,228

The results demonstrate that duplicate-removal scope substantially affects the resulting experimental dataset.

Feature-Suite-Specific Duplicate Analysis

Because the original RQ1 experiment evaluates separate feature configurations, duplicate counts were additionally measured separately for each feature suite.

LOC
Scope Duplicates Remaining
Global 698,641 3,382
Within project 676,218 25,805
Within release 616,041 85,982
CK
Scope Duplicates Remaining
Global 608,699 93,324
Within project 573,585 128,438
Within release 338,683 363,340
OTHER
Scope Duplicates Remaining
Global 573,195 128,828
Within project 550,735 151,288
Within release 356,525 345,498
CK + OTHER
Scope Duplicates Remaining
Global 508,013 194,010
Within project 497,968 204,055
Within release 226,130 475,893

These results demonstrate that duplicate removal is highly sensitive to both the feature configuration and the scope at which duplicates are identified.

Quantitative Duplicate-Removal Investigation

A dedicated duplicate-removal investigation was performed for every project and feature configuration.

Two plausible project-oriented strategies were evaluated.

Project-Level Deduplication

Duplicate feature and target combinations are removed across all releases belonging to the same project.

Within-Release Deduplication

Duplicate feature and target combinations are removed separately within each release.

Aggregate Results
Feature Suite Scope Processed Rows Rows Removed Percentage Removed Defective Rows Remaining Processed Defect Percentage
CK Project 128,438 573,585 81.70% 17,200 13.39%
CK Within Release 363,340 338,683 48.24% 21,792 6.00%
CK + OTHER Project 204,055 497,968 70.93% 19,280 9.45%
CK + OTHER Within Release 475,893 226,130 32.21% 22,838 4.80%
LOC Project 25,805 676,218 96.32% 8,367 32.42%
LOC Within Release 85,982 616,041 87.75% 15,287 17.78%
OTHER Project 151,288 550,735 78.45% 17,504 11.57%
OTHER Within Release 345,498 356,525 50.79% 21,417 6.20%
Duplicate-Removal Findings

The quantitative investigation demonstrates that duplicate removal is not a minor preprocessing decision.

Depending on the feature configuration and duplicate-removal scope:

Between 32.21% and 96.32% of observations may be removed.
The defective-class percentage can change substantially.
LOC is particularly sensitive to duplicate removal.
Duplicate observations disproportionately belong to the non-defective majority class.
Duplicate removal therefore significantly alters the class distribution.

For example:

Project-level LOC deduplication reduces the dataset from 702,023 observations to 25,805 observations and increases the defective percentage from 3.48% to 32.42%.
Within-release LOC deduplication leaves 85,982 observations with a defective percentage of 17.78%.
Project-level CK + OTHER deduplication leaves 204,055 observations with a defective percentage of 9.45%.
Within-release CK + OTHER deduplication leaves 475,893 observations with a defective percentage of 4.80%.

Therefore, the reproduction does not silently assume a duplicate-removal procedure.

The primary reproduction strategy and any sensitivity analyses must explicitly document the selected duplicate-removal scope.

Validation Strategy

The original study uses:

Stratified 10-fold cross-validation.

The paper describes randomly splitting observations into 10 stratified folds.

Remaining Ambiguities

The following implementation details are not fully specified:

Exact cross-validation scope.
Exact random seed.
Whether identical or highly similar observations from different releases may occur across folds.

These decisions will be explicitly documented before model implementation.

Evaluation Metrics

The original study evaluates classifier performance using:

F-measure for the defective minority class.
Weighted AUC-ROC.
F-Measure

The defective class is treated as the positive class.

AUC-ROC

The paper reports weighted AUC-ROC, but the exact implementation-level calculation requires reconstruction.

Statistical Analysis

The original study uses:

Mann-Whitney U test.
Kruskal-Wallis test.

These statistical tests will be reproduced after the primary model evaluation pipeline has been implemented.

RQ2 Feature Importance Experiment

The original study investigates individual source-code metric importance using:

Variance Inflation Factor analysis.
10-fold cross-validated permutation feature importance.
Project-level feature ranking.
Aggregated feature-ranking analysis.
Multicollinearity Analysis

The original study uses Variance Inflation Factor analysis.

The methodology identifies:

RFC
WMC

as problematic for the feature-importance experiment.

These features are removed from the RQ2 feature-importance analysis.

They remain part of the relevant RQ1 feature configurations.

RQ2 Features

After removing RFC and WMC, the RQ2 experiment analyzes:

LCOM5
NLE
CBO
CBOI
CD
DIT
NOC
NPA
NPM
Artifact Forensics

The official result artifact was inspected.

It contains:

39 project-specific feature-importance plots.
One aggregate importance_ALL plot.

The artifact provides strong evidence that RQ2 feature-importance analysis was performed separately for each project before aggregate analysis.

The artifact does not provide sufficient evidence to determine:

The exact RQ1 experimental scope.
The exact duplicate-removal procedure.
The random seed.
The exact implementation of weighted AUC-ROC.
Identified Reproducibility Ambiguities

The reproduction investigation has identified the following major ambiguities:

Exact duplicate-removal procedure.
Whether duplicate removal occurs before or after feature-suite selection.
Exact duplicate-removal scope.
Exact RQ1 cross-validation scope.
Random seed not reported.
Exact weighted AUC-ROC implementation.
Exact classifier hyperparameters and implementation defaults.
Exact VIF-based project or observation exclusion procedure.
Reproduction Principles

The following principles guide the implementation:

No methodological ambiguity will be silently resolved in source code.
Decisions introduced by the reproduction will be documented.
Original-paper methodology will be separated from reproduction assumptions.
Sensitivity analysis will be used where unresolved methodological decisions could materially affect results.
Reproduction experiments will be completed before implementing the explainability extension.
Raw research data will remain unmodified.
Generated and processed data will remain separate from the original research artifact.
Current Reproduction Status
 Base paper selected.
 Official dataset obtained.
 Dataset structure validated.
 39 projects confirmed.
 275 releases confirmed.
 Dataset profiling completed.
 Class distribution measured.
 Missing and infinite values checked.
 Duplicate definitions investigated.
 Feature-suite-specific duplicates investigated.
 Project-level and release-level deduplication compared.
 Result artifact inspected.
 RQ2 project-level structure confirmed.
 Primary reproduction protocol finalized.
 Reproduction preprocessing implemented.
 Original classifiers implemented.
 RQ1 experiments reproduced.
 Statistical analysis reproduced.
 RQ2 feature-importance experiment reproduced.
 Published and reproduced results compared.
 Explainability extension implemented.
 Final technical report completed.
