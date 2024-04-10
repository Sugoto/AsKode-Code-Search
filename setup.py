from setuptools import setup, find_packages

setup(
    name="askode",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "askode=kode_search.app:cli",
        ],
    },
    install_requires=["whoosh", "colorama", "art", "click"],
    python_requires=">=3.6",
)
