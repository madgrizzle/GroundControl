#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from kivy.app                                import App
from kivy.uix.popup                          import Popup
from kivy.uix.screenmanager                  import Screen
from kivy.uix.floatlayout                    import FloatLayout
from UIElements.frontPage                    import FrontPage
import urlparse
import json
from OpticalCalibration.opticalCalibrationCanvas    import OpticalCalibrationCanvas
#This class will handles any incoming request from
#the browser
class webHandler(BaseHTTPRequestHandler):
    widget = None
    widgetTitle = ""

    def do_GET(self):
        print self.path
        if self.path.endswith(".css"):
            print "at css"
            f = open("WebService/"+self.path)
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return
        if self.path.endswith(".js"):
            print "at js"
            f = open("WebService/"+self.path)
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return
        content = self.getContentForActiveWidget()
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(content)
        return

    def do_PUT(self):
        print "at PUT"
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        #print self.data_string
        fields = json.loads(self.data_string)
        if 'action' in fields:
            self.executeAction(fields['action'],fields['widget'])
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write("OK")

    def executeAction(self, _field, _widget):
        self.app = App.get_running_app()
        activeWidget = self.app.activeWidget
        print _widget+"->"+_field
        if (_widget=="Optical Calibration"):
            functions = {'Exit':activeWidget.do_Exit,
                         'CalibrateSledRotation':activeWidget.on_CenterOnSquare,
                         'CalibrateDimensions':activeWidget.on_CenterOnSquare,
                         'ReturnToCenter':activeWidget.on_ReturnToCenter}
            arguments = { 'CalibrateSledRotation':{'findCenter':True},
                          'CalibrateDimensions':{'doCalibrate':True}}
        elif (_widget=="FrontPage"):
            functions = {'Home':activeWidget.home }
            arguments = { }

        if _field in functions and _field in arguments:
            functions[_field](**arguments[_field])
            return
        elif _field in functions:
            print "calling without arguments"
            functions[_field]()
            return

    def getContentForActiveWidget(self):
        self.app = App.get_running_app()
        _widget = self.app.activeWidget
        if type(_widget) is OpticalCalibrationCanvas:
            fileName = "OpticalCalibration.html"
        elif type(_widget) is FrontPage:
            fileName = "FrontPage.html"
        else:
            fileName = "NotFound.html"
        f = open("WebService/"+fileName)
        content = f.read()

        content+="<script>disableBtn()</script><html>"
        return content
