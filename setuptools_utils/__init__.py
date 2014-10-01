from setuptools import Command

class minify(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            import jsmin
        except:
            pass
        djanalytics_js_in = open('djanalytics/templates/djanalytics.js')
        djanalytics_js_out = open('djanalytics/templates/djanalytics.js.min', 'w')
        try:
            jsmin.JavascriptMinify(djanalytics_js_in, djanalytics_js_out).minify()
        finally:
            djanalytics_js_in.close()
            djanalytics_js_out.close()
