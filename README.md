[![Travis CI Build Status](https://travis-ci.org/analytehealth/django-analytics.svg)](https://travis-ci.org/analytehealth/django-analytics)

django-analytics
================

Django app to capture, track and display site analytics

Install
-------
pip install dj-analytics

Add to django configuration (before 1.7)
---------------------------
* Add `djanalytics` to `INSTALLED_APPS` in settings.py file.
* Run `manage.py migrate djanalytics` to create database tables.

Add to django configuration (1.7+)
---------------------------
* Add `djanalytics` to `INSTALLED_APPS` in settings.py file.
* Point at correct migration module:

    MIGRATION_MODULES = {
        'djanalytics': 'djanalytics.django_migrations'
    }

* Run `manage.py migrate djanalytics` to create database tables.

Configure
---------
* Create and configure at least one Client and Domain.
* If you're capturing using HTML, in your urls.py, include djanalytics urls. For example:

    urlpatterns += patterns(
        '',
        (r'', include('djanalytics.urls'))
    )

* For charts, include the charts urls:

    urlpatterns += patterns('', (r'^analytics/', include='djanalytics.charts.urls'))

* For reports, include the reports urls:

    urlpatterns += patterns('', (r'^analytics/', include='djanalytics.reports.urls'))

Capture using middleware
--------------

* In settings.py, add 'djanalytics.middleware.AnalyticsMiddleware' to the MIDDLEWARE_CLASSES setting
for your django project.
* In settings.py, add DJA_CLIENT_ID='[uuid of Client created above]'

Capture using HTML
------------------

    <script>
    var img_html = '<img src="http://dja_server.example.com/capture/' +
        '?dja_id=[client uuid]' +
        '&pth=' + escape(window.location.pathname) +
        '&qs=' + escape(window.location.search.substr(window.location.search.indexOf('?')+1)) +
        '&rf=' + escape(document.referrer) +
        '&sw=' + screen.width +
        '&sh=' + screen.height +
        '" style="position:absolute; left: -999px"></img>";
    document.getElementsByTagName('body')[0].innerHTML += img_html;
    </script>

Capture Cross-Domain
--------------------
If you're hosting your djanalytics instance in a different domain than the site you're capturing,
you will need to use a slightly different mechanism. Set up djanalytics on your server, and ensure
it's got a url for the djanalytics_js view (included in the urls.py file). Then put the following
HTML in your templates:

    <div id="dja_tag"></div>
    <script defer="defer">
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://dja_server.example.com/djanalytics.js' +
                 '?dja_id=[client uuid]';
    document.getElementsByTagName('body')[0].appendChild(script);
    </script>

If you want to maintain tracking ids across domains, you'll need to add them to links between sites.
If the site you're linking to is a django site with djanalytics installed, you can use the
cross-domain middleware by adding 'djanalytics.middleware.CrossDomainMiddleware' to your
MIDDLEWARE_CLASSES setting and then pass the client ID, user ID and tracking ID (dja_id, dja_uuid,
and dja_tracking_id respectively) in your link as parameters. This will then handle setting the
appropriate cookies.

Filtering IP addresses
----------------------

If you're using the django admin app, djanalytics will automatically register its models. To filter
by IP address, add a new IPFilter for your client. The IPFilter uses netmasks to filter addresses. You
can also specify whether to include or exclude the given netmask. If you choose include, only IP
addresses that match the netmask will be allowed in.

Filtering Paths
---------------

The PathFilter model allows you to include or exclude path patterns. PathFilters use regex to determine
a match on the path.

Reporting
---------

### Generating report data

A management command, _collect_reporting_stats_, will generate report data. This command should
most likely be run on a schedule (cron). It takes a few arguments:

* -s, --start - Date of earliest RequestEvent to process. This is optional. If omitted, the command will
not set a beginning time when searching for RequestEvents.
* -e, --end - Date of latest RequestEvent to process. This is optional. If omitted, the command will
not set an end time when searching for RequestEvents.
* -a, --max-age - This is used when calculation visit durations as well as visit durations,
conversions and exit pages. This argument defaults to 30 days.

### Conversion Tracking

In order to track conversions, you'll need to define page patterns for the FUNNEL and CONVERSION
page types. Conversions are defined by a page visit to at least one FUNNEL page followed by
a page visit to a CONVERSION page.

License
-------
[Read it here](https://raw.githubusercontent.com/analytehealth/django-analytics/master/LICENSE)

Change Log
----------
- 1.0.1
  - Fix for issue #27 - User-agents with non-ascii characters cause collect_reporting_stats command to fail
- 1.0
  - Modeling for analytics reporting (#25)
  - Adding a number of reports:
    - #19 - Audience Overview Report
    - #20 - Device Overview Report
    - #21 - Browser and OS Detail Report
    - #22 - Page Overview Report
    - #23 - Ecommerce Overview Report
    - #24 - Device Detail Report
  - Added management command to collect data into reporting model (#26)

- 0.11.3
  - Fix for issue #17 - ensure djanalytics.js is served regardless of where request comes from

- 0.11.2
  - Fix for issue #16 - try to make sure all browsers work with djanalytics.js (IE8 had some issues)

- 0.11.1
  - Fix for issue #15 - djanalytics.js is breaking events

- 0.11
  - Added issue #13 - Cross-domain capabilities

- 0.10.1
  - Fix for issue #11 - Max key length exceeded with referrer field

- 0.10
  - Added screen width and height to RequestEvent model (issue #10)
  - Added 'sw' and 'sh' parameters to Capture view to support screen width and height

- 0.9
  - Fixed issue #6 - Referrer length > 200 characters causes 500 error
  - Added chart for top pages (issue #8)
  - Now capturing domain in middleware
  - Added chart for exit pages (issue #9)
  - Added chart for external referrers (issue #7)
  - Made base template for charts to better allow for overrides
  - Broke chart views.py file up into individual modules

- 0.8
  - Corrected name of user chart.
  - Added try / except block around middleware to avoid 500 error when
    client doesn't exist or can't be found.

- 0.7.1
  - Fix for issue #5 - Created date on RequestEvent is storing the wrong date

- 0.7
  - Fix for issue #3 - logic for determining valid domain in capture view is wrong.

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

