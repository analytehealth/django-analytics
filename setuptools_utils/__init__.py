import jsmin

from distutils.command.build import build

class minify(build):

    def run(self):
        djanalytics_js_in = open('djanalytics/templates/djanalytics.js')
        djanalytics_js_out = open('djanalytics/templates/djanalytics.js.min', 'w')
        try:
            jsmin.JavascriptMinify(djanalytics_js_in, djanalytics_js_out).minify()
        finally:
            djanalytics_js_in.close()
            djanalytics_js_out.close()
        build.run(self)
