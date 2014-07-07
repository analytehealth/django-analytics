[![Travis CI Build Status](https://travis-ci.org/analytehealth/django-analytics.svg?branch=development)](https://travis-ci.org/analytehealth/django-analytics)

django-analytics
================

Django app to capture, track and display site analytics

Install
-------
pip install dj-analytics

Add to django configuration
---------------------------
* Add `djanalytics` to `INSTALLED_APPS` in settings.py file.
* Run `manage.py migrate djanalytics` to create database tables.
* Create and configure at least one Client and Domain.
* In urls.py, include djanalytics urls. For example:

    urlpatterns += patterns(
        '',
        (r'', include('djanalytics.urls'))
    )

Use middleware
--------------

In settings.py, add 'djanalytics.middleware.AnalyticsMiddleware' to the MIDDLEWARE_CLASSES setting
for your django project.

Capture using HTML
------------------

    var img_html = '<img src="http://dja_server.example.com/capture/' +
        '?dja_id=[client uuid]' +
        '&pth=' + escape(window.location.pathname) +
        '&qs=' + escape(window.location.search.substr(window.location.search.indexOf('?')+1)) +
        '&rf=' + escape(document.referrer) +
        '" style="position:absolute; left: -999px"></img>";
    document.write(img_html);

License
-------
[Read it here](https://raw.githubusercontent.com/analytehealth/django-analytics/master/LICENSE)

Change Log
----------
- 0.6
  - Added Location model object. This will allow geocoding of IP addresses on a periodic basis,
    since IP addresses change over time.
 
- 0.5
  - Fix for issue #1 - capture view raises TypeError
  - Fix for issue #2 - allow for use of HTTP_X_FORWARDED_FOR header

- 0.4
  - Switched version of django-graphos to fix install issue
  - Added in files for Travis CI

- 0.3
  - Added 'referrer' to RequestEvent model
  - Added more indexes to RequestEvent model
  - Added middleware documentation to README

- 0.2
  - Switched default for RequestEvent created field to 'now()' instead of 'today()'

- 0.1
  - Initial version

