from setuptools import find_packages
from setuptools import setup

if __name__ == "__main__":
    name = "text2speech"
    version = "1.0.0"
    python_requires = ">=3.10,<3.11"
    description = "A simple text to speech app written in Python."
    packages = find_packages(include=["text2speech", "text2speech.*"])
    install_requires = ["gradio"]
    extras_require = {
        "development": ["isort", "mypy", "black", "Flake8-pyproject", "pytest", "pytest-cov"]
    }

    setup(
        name=name,
        version=version,
        description=description,
        python_requires=python_requires,
        packages=packages,
        install_requires=install_requires,
        extras_require=extras_require,
        entry_points={},  # Define here any scripts you want to run from the command line
    )
