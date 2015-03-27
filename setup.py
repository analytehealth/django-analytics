import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
from setuptools_utils import minify

version = '1.0.1'

setup(
    name='dj-analytics',
    version=version,
    author='Analyte Health',
    author_email='tech@analytehealth.com',
    url='https://github.com/analytehealth/django-analytics',
    zip_safe=False,
    download_url='https://github.com/analytehealth/django-analytics/archive/%s.tar.gz' % version,
    packages=find_packages(exclude=('*.tests',)),
    package_data={
        'djanalytics': [
            'templates/djanalytics/*.html',
            'templates/djanalytics/charts/*',
            'templates/djanalytics/reports/*',
            'templates/*png',
            'templates/*js',
            'templates/*min',
            'static/css/*',
            'static/fonts/*',
            'static/img/*',
            'static/js/*',
        ],
    },
    description='Django app to capture, track and display site analytics',
    long_description=open('README.md').read(),
    install_requires=[
        'ipaddress',
        'python-dateutil',
        'django-graphos==0.0.2a0',
        'pytz',
        'user-agents>=0.3.0',
        'jsmin>=2.0.6',
    ],
    cmdclass={'minify': minify},
)
