from distutils.core import setup
from setuptools import find_packages

# this is a hack until I figure out how to properly do this with setup
try:
    import jsmin

    djanalytics_js_in = open('djanalytics/templates/djanalytics.js')
    djanalytics_js_out = open('djanalytics/templates/djanalytics.js.min', 'w')
    try:
        jsmin.JavascriptMinify(djanalytics_js_in, djanalytics_js_out).minify()
    finally:
        djanalytics_js_in.close()
        djanalytics_js_out.close()
except:
    pass
#endhack

version = '0.11'

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
            'templates/charts/*',
            'templates/*png',
            'templates/*js',
            'templates/*min',
        ],
    },
    description='Django app to capture, track and display site analytics',
    long_description=open('README.md').read(),
    install_requires=[
        ln for ln in open('requirements.txt').read().split('\n')
    ],
)
