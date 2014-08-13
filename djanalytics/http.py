from django.http.response import HttpResponse

from djanalytics.encoders import jsonencoder


class JsonHttpResponse(HttpResponse):
    """HttpResponse which JSON-encodes its content and sets mimetype to
    "application/json".

    """
    def __init__(self, content='', content_type='application/json', status=None):
        super(JsonHttpResponse, self).__init__(
            jsonencoder.encode(content),
            content_type=content_type,
            status=status
        )
