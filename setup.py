from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    author='Dustin Ingram',
    author_email='di@di.codes',
    description='The official unofficial pip API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='pip-api',
    packages=['pip_api'],
    url='http://github.com/di/pip-api',
    version='0.0.1',
)
