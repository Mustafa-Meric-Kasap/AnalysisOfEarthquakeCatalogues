# Analysis of Earthquake Catalogues

## Rules

All rules in this guide must be followed or might get replaced without warning.

### Branch Naming Conventions

Branch names must follow this naming convention:

1. **fix/...**: Branches dedicated to fixing specific issues or bugs in the codebase.
2. **feat/...**: Branches focused on implementing new features or functionalities.
3. **wip/...**: Branches indicating work-in-progress, often for incomplete features or experimental changes.
4. **refactor/...**: Branches for refactoring existing code to improve its structure, readability, or performance.
5. **hotfix/...**: Branches for addressing critical issues or bugs that require immediate action.
6. **test/...**: Branches for testing purposes, such as writing or updating unit tests.
7. **data/...**: Branches focused on data-related tasks, such as cleaning, augmentation, or transformation scripts.
8. **exp/...**: Branches for experimental features or models that may not be finalized.
9. **doc/...**: Branches for updating documentation, such as README, notebooks, or code comments.

## Project Structure

The project is organized as follows:

- **data/**
  - **cleaned/**: Cleaned datasets.
  - **processed/**: Processed datasets ready for modeling.
  - **raw/**: Raw datasets before any processing.
  
- **docs/**: Documentation related to the project, including this README.
  
- **environment/**: Environment-related files, such as `requirements.txt` for dependencies.
  
- **experiments/**: Directory for storing experimental results or configurations.
  
- **models/**: Directory for saving trained models and related scripts.
  
- **notebooks/**
  - **exploration/**: Jupyter notebooks for exploratory data analysis.
  - **final/**: Final versions of notebooks ready for presentation.
  - **modeling/**: Notebooks focused on model development.
  - **visualization/**: Notebooks dedicated to data visualization and result interpretation.
  
- **papers/**: Directory for storing papers, reports, or references used in the project.
  
- **scripts/**: Utility scripts used across the project.
  
- **src/**
  - **data/**
    - **preprocess.py**: Script for data preprocessing.
    - **transform.py**: Script for data transformation.
  - **models/**
    - **__init__.py**: Initialization file for model-related modules.
  - **util/**: Utility functions or helper scripts.
  - **visualization/**
    - **__init__.py**: Initialization file for visualization-related modules.
  
- **tests/**: Unit tests and validation scripts.
