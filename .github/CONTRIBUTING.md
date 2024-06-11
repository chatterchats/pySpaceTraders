# Contributing to pySpaceStrader

Thank you for your interest in contributing to pySpaceTrader! We welcome all types of contributions: bug reports, feature suggestions, documentation improvements, and code contributions.

Please take a moment to review this document to make the contribution process easy and effective for everyone involved.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Code of Conduct](#code-of-conduct)
3. [How to Contribute](#how-to-contribute)
    - [Reporting Bugs](#reporting-bugs)
    - [Suggesting Enhancements](#suggesting-enhancements)
    - [Submitting Changes](#submitting-changes)
4. [Style Guide](#style-guide)
5. [Running Tests](#running-tests)
6. [Additional Resources](#additional-resources)

## Getting Started

To get started with contributing:

1. Fork the repository.
2. Clone your fork: `git clone https://github.com/your-username/your-repo-name.git`
3. Create a new branch: `git checkout -b feature-branch`
4. Create Virtual Environment `python -m venv venv
5. Activate Virtual Environment | Windows: `venv\Scripts\activate` or Linux/Mac: `source venv/bin/acvtivate`
6. Install development requirements `pip install -r requirements-dev.txt`

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a positive experience for all contributors.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with the following details:
- A clear and descriptive title.
- Steps to reproduce the issue.
- Expected and actual behavior.
- Screenshots or code snippets, if applicable.
- Any other relevant information.

### Suggesting Enhancements

If you have an idea for an improvement, please open an issue on GitHub with:
- A clear and descriptive title.
- A detailed description of the proposed enhancement.
- Any relevant examples or use cases.

### Submitting Changes

1. Ensure your changes pass all tests and adhere to the project’s style guide.
2. Commit your changes with a descriptive message: `git commit -m 'Add new feature'`.
3. Push to your branch: `git push origin feature-branch`.
4. Open a pull request on GitHub with a detailed description of your changes and why they are necessary.

## Style Guide

We use [Black](https://github.com/psf/black) to maintain code style consistency. Please format your code before submitting changes.

1. Run Black on your code: `black .`

## Running Tests

Ensure that all tests pass before submitting your changes. To run the tests:

1. Run the tests: `pytest`

## Additional Resources

- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Black Formatter](https://black.readthedocs.io/en/stable/)
- [pytest Documentation](https://docs.pytest.org/en/stable/)

Thank you for contributing!
