from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    author="Dustin Ingram",
    author_email="di@di.codes",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="An unofficial, importable pip API",
    install_requires=["pip"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="pip-api",
    packages=["pip_api"],
    python_requires=">=2.7,!=3.0,!=3.1,!=3.2,!=3.3",
    url="http://github.com/di/pip-api",
    summary="An unofficial, importable pip API",
    version="0.0.9",
)
