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

