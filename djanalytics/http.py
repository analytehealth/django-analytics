from django.http.response import HttpResponse

from djanalytics.encoders import jsonencoder


class JsonHttpResponse(HttpResponse):
    """HttpResponse which JSON-encodes its content and sets mimetype to
    "application/json".

    """
    def __init__(self, content='', mimetype='application/json', status=None,
                 content_type=None):
        super(JsonHttpResponse, self).__init__(
            jsonencoder.encode(content), mimetype, status, content_type)
