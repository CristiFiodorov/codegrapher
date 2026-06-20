from setuptools import setup, find_packages

setup(
    name="codegrapher",
    version="0.1.0",
    description="Parse source code into AST, DFG or combined graphs",
    author="Cristian FIODOROV",
    license="MIT",
    license_files=["LICENSE"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "tree-sitter>=0.24",
        "tree-sitter-language-pack>=0.7",
        "networkx",
    ],
    entry_points={
        "console_scripts": [
            "codegrapher=main:main",
        ],
    },
)
