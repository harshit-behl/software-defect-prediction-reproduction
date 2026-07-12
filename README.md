# Reproducing and Extending Source-Code Metric-Based Software Defect Prediction

This repository contains an independent reproduction and extension study of the paper **"Source Code Metrics for Software Defects Prediction"**.

## Project Objectives

The project aims to:

1. Reproduce the machine learning experiments reported in the original study.
2. Compare reproduced results with the published findings.
3. Document methodological ambiguities and reproducibility challenges.
4. Extend the original study through explainable AI and feature explanation analysis.
5. Investigate the consistency of source-code metric explanations across machine learning models.

## Base Study

**Paper:** Source Code Metrics for Software Defects Prediction

The original study evaluates the effectiveness of source-code metrics for predicting defective Java classes using 39 open-source Java projects and 275 software releases.

The original experiment compares:

- Naive Bayes
- Decision Tree
- Random Forest

across four feature configurations:

- LOC
- CK metrics
- OTHER metrics
- CK + OTHER metrics

## Research Questions

### Reproduction

**RQ1:** To what extent can the predictive results of the original source-code metric-based software defect prediction study be reproduced?

### Extension

**RQ2:** How do additional machine learning models compare with the original classifiers under consistent experimental conditions?

**RQ3:** Which source-code metrics contribute most strongly to defect predictions?

**RQ4:** How consistent are feature explanations across different machine learning models?

## Repository Structure

```text
data/               Dataset storage
docs/               Research and reproducibility documentation
notebooks/          Exploratory data analysis
results/            Experimental outputs
src/                Source code
tests/              Automated tests
