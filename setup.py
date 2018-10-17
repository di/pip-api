from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    author='Dustin Ingram',
    author_email='di@di.codes',
    description='The official unofficial pip API',
    install_requires=['packaging'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='pip-api',
    packages=['pip_api'],
    python_requires='>=2.7,!=3.0,!=3.1,!=3.2,!=3.3',
    url='http://github.com/di/pip-api',
    summary='The official unofficial pip API',
    version='0.0.2',
)
