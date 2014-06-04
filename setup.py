from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-analytics',
    version='dev',
    author='Analyte Health',
    packages=find_packages(exclude=('*.tests',)),
    package_data={
        'djanalytics': [
            'templates/charts/*'
            'templates/djanalytics/*',
            'templates/*png'
        ],
    },
    description='Django app to capture, track and display site analytics',
    long_description=open('README.md').read(),
    install_requires=[
        ln for ln in open('requirements.txt').read().split('\n')
    ],
)
