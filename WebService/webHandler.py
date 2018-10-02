#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from kivy.app                                import App
from kivy.uix.popup                          import Popup
import urlparse
from OpticalCalibration.opticalCalibrationCanvas    import OpticalCalibrationCanvas
#This class will handles any incoming request from
#the browser
class webHandler(BaseHTTPRequestHandler):
    widget = None
    widgetTitle = ""

    def do_GET(self):
        print "at get"
        fields = urlparse.parse_qs(urlparse.urlparse(self.path).query)
        #print fields
        print fields
        if 'action' in fields:
            self.executeAction(fields['action'][0],fields['widget'][0])
        #print fields['action'][0]
        #print fields['widget']
        self.app = App.get_running_app()
        for widget in self.app.root_window.children:
            if isinstance(widget,Popup):
                if widget.title == "Maslow Optical Calibration":
                    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.end_headers()
                    # Send the html message
                    self.wfile.write("<html><head><title>"+widget.title+"</title></head>")
                    self.wfile.write("<body><form method='get'>")
                    self.wfile.write("<input type='hidden' id='widget' name='widget' value='"+widget.title+"'>")
                    self.wfile.write("<button type='submit' name='action' value='Calibrate'>Calibrate</button>")
                    self.wfile.write("<button type='submit' name='action' value='do_Exit'>Exit</button>")
                    self.wfile.write("</form></body><html>")
                    return
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write("No Screen Detected !")
        return

    def executeAction(self, _field, _widget):

        print _widget+"->"+_field
        self.app = App.get_running_app()
        for widget in self.app.root_window.children:
            if isinstance(widget,Popup):
                if widget.title == _widget:
                    if (widget.title=="Maslow Optical Calibration"):
                        functions = {'do_Exit':widget.content.do_Exit}
                        if _field in functions:
                            print "_field:"+_field
                            #print functions[_field]
                            functions[_field]()


'''

                    method_to_call = getattr(OpticalCalibrationCanvas, 'do_Exit')

                    widget.content.on_CenterOnSquare(doCalibrate=True)

        if fields['action'][0] == "Calibrate":
            print "button1 at "+fields['widget'][0]
        elif fields['action'][0] == "Exit":
            print "button2 at "+fields['widget'][0]
            self.app = App.get_running_app()
            for widget in self.app.root_window.children:
                if isinstance(widget,Popup):
                    if widget.title == fields['widget'][0]:
                        widget.content.do_Exit()
        else:
            print "nada"
'''
