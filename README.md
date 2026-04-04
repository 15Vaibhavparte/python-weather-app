# 🚀 Python Project Build & Package: A Learning Trial

> **Disclaimer**
> This project was created **entirely for trial and educational purposes**. It is a hands-on exercise designed to explore the complete Python development and packaging lifecycle from scratch. It is not intended to be a production-ready repository.

## 🎯 The Purpose

The core objective of this repository is to step out of the theory and gain practical, end-to-end experience with Python project architecture. Specifically, this trial aims to:

* **Structure:** Learn how to organize a Python project according to modern best practices.
* **Configure:** Understand the intricate setup required for robust packaging using modern standards (`pyproject.toml`).
* **Tooling:** Explore industry-standard build tools (`build`, `twine`).
* **Workflow:** Gain muscle memory for the complete packaging and deployment workflow.

## 🛤️ How It Was Built: Step-by-Step Guide

This project was built methodically through six distinct phases. Below is a descriptive breakdown of how the final package was achieved, including the exact configurations used.

### 🛠️ 1. Project Initialization & Environment

The first step was establishing a clean workspace and isolating dependencies to avoid conflicts with the global Python installation.

```bash
# 1. Create and enter the project directory
mkdir python-packaging-trial
cd python-packaging-trial

# 2. Initialize Git
git init

# 3. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
💻 2. Core Development Structure
Modern Python packages place source code inside a src/ directory to prevent accidental imports during testing. Here is the structure we created:

plaintext
python-packaging-trial/ 
├── src/
│   └── weather_fetcher/
│       ├── __init__.py
│       └── core.py
├── tests/
│   └── test_core.py
├── pyproject.toml
└── README.md
Example Application Code (src/weather_fetcher/core.py):

python
import requests

def get_temperature(city: str) -> str:
    """Fetches the current temperature for a given city."""
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    if response.status_code == 200:
        data = response.json()
        return f"The temperature in {city} is {data['current_condition'][0]['temp_C']}°C"
    return "City not found."
📦 3 & 4. Dependency Management and Packaging Setup
Instead of the legacy setup.py, this project utilizes the modern PEP 518 standard via pyproject.toml. This file acts as the single source of truth for metadata and build instructions.

Configuration (pyproject.toml):

toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "weather-fetcher-trial"
version = "0.1.0"
authors = [
  { name="Your Name", email="your.email@example.com" },
]
description = "A trial project to learn Python packaging."
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "requests>=2.31.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0.0"]
🧪 5. Testing & Validation
Before packaging, we must ensure the code works. We install the package locally in "editable" mode (-e) along with our testing dependencies.

bash
# Install the package and development dependencies
pip install -e .[dev]

# Run pytest
pytest tests/
Example Test (tests/test_core.py):

python
from weather_fetcher.core import get_temperature

def test_get_temperature():
    # A basic test to ensure the function returns a string
    result = get_temperature("London")
    assert isinstance(result, str)
    assert "temperature" in result or "not found" in result
🚀 6. Build & Distribution
Once the code was tested, we converted the raw files into distributable formats: a Source Distribution (.tar.gz) and a Wheel (.whl).

bash
# 1. Install the build tool
python3 -m pip install --upgrade build

# 2. Build the package
python3 -m build
This command generates a dist/ directory containing the .whl and .tar.gz artifacts.

Finally, to simulate sharing this package with the world (or an internal company repository like Nexus), we used twine:

bash
# Install twine for uploading
python3 -m pip install --upgrade twine

# Upload to TestPyPI (or standard PyPI/Nexus)
twine upload --repository testpypi dist/*
🧠 Key Takeaways
Through building this trial project, several core DevOps and Python packaging concepts were mastered:

Concept	Practical Application
Project Architecture	Organizing raw code into scalable src/ modules.
Environment Isolation	Utilizing venv to prevent dependency conflicts.
Configuration Specs	Transitioning from setup.py to the modern pyproject.toml.
Artifact Generation	Compiling raw code into distributable formats (Wheel/sdist).
Validation	Ensuring the final compiled package is fully operational post-installation.
🏁 Conclusion
This exercise successfully demystified the end-to-end process of packaging a Python application. By building this from scratch, the theoretical concepts of dependency management, build tooling, and distribution have been translated into practical, repeatable workflows.
