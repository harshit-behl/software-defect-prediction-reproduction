# Reproduction Blueprint

## Base Study

**Title:** Source Code Metrics for Software Defects Prediction

## Dataset

- 39 open-source Java projects
- 275 software releases
- Class-level source-code observations
- Binary target variable: `isDefective`

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

All CK and OTHER metrics.

## Original Classifiers

- Naive Bayes
- Decision Tree
- Random Forest

## Preprocessing

The original study removes duplicate observations as a limited approach to class-imbalance reduction.

The exact duplicate-removal scope requires further investigation.

## Validation

- Stratified 10-fold cross-validation

### Ambiguity

The exact scope of cross-validation and the random seed are not fully specified.

## Evaluation

- F-measure for the defective minority class
- Weighted AUC-ROC

## Statistical Analysis

- Mann-Whitney U test
- Kruskal-Wallis test

## Feature Importance Experiment

- Variance Inflation Factor analysis
- RFC and WMC removed from the feature-importance experiment
- 10-fold cross-validated permutation feature importance
- Feature rankings aggregated across suitable projects

## Identified Reproducibility Ambiguities

1. Exact duplicate-removal procedure.
2. Exact cross-validation scope.
3. Random seed not reported.
4. Exact weighted AUC-ROC implementation.
5. Exact project-exclusion procedure during VIF analysis.

## Reproduction Decisions

All decisions introduced because of missing methodological details will be documented here before implementation.

No methodological ambiguity should be silently resolved in the source code.
