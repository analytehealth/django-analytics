from distutils.core import setup
from setuptools import find_packages

setup(
    name='dj-analytics',
    version=0.1,
    author='Analyte Health',
    author_email='tech@analytehealth.com',
    url='https://github.com/analytehealth/django-analytics',
    download_url='https://github.com/analytehealth/django-analytics/archive/0.1.tar.gz',
    packages=find_packages(exclude=('*.tests',)),
    package_data={
        'djanalytics': [
            'templates/charts/*',
            'templates/*png'
        ],
    },
    description='Django app to capture, track and display site analytics',
    long_description=open('README.md').read(),
    install_requires=[
        ln for ln in open('requirements.txt').read().split('\n')
    ],
)
