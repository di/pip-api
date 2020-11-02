from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    author="Dustin Ingram",
    author_email="di@python.org",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="An unofficial, importable pip API",
    install_requires=["pip"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="pip-api",
    packages=find_packages(),
    python_requires=">=2.7,!=3.0,!=3.1,!=3.2,!=3.3",
    url="http://github.com/di/pip-api",
    summary="An unofficial, importable pip API",
    version="0.0.17",
)
