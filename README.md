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

Capture using HTML
------------------

    var url = 'http://dja_server.example.com/capture/?dja_id=[client uuid]';
    document.write('<span style="display: none"><img src="' +
        url+'&pth='+window.location.pathname+
        '&qs='+
        escape(window.location.search.substr(window.location.search.indexOf('?')+1))+
        '"></img></span>');
