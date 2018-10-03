#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from kivy.app                                import App
from kivy.uix.popup                          import Popup
from kivy.uix.screenmanager                  import Screen
from kivy.uix.floatlayout                    import FloatLayout
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
                content = self.getContent(widget.title)
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(content)
                return
        for widget in self.app.root_window.children:
            if isinstance(widget,FloatLayout):
                for childWidget in widget.children:
                    print childWidget
                    if isinstance(childWidget,Screen):
                        content = self.getContent(childWidget.name)
                        self.send_response(200)
                        self.send_header('Content-type','text/html')
                        self.end_headers()
                        self.wfile.write(content)
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
                        functions = {'Exit':widget.content.do_Exit,
                                     'CalibrateSledRotation':widget.content.on_CenterOnSquare,
                                     'CalibrateDimensions':widget.content.on_CenterOnSquare}
                        arguments = { 'CalibrateSledRotation':{'findCenter':True},
                                      'CalibrateDimensions':{'doCalibrate':True}}
                        if _field in functions and _field in arguments:
                            functions[_field](**arguments[_field])
                            return
                        elif _field in functions:
                            print "calling without arguments"
                            functions[_field]()
                            return
        if _widget=="FrontPage":
            self.app.frontpage.home()

    def getContent(self,title):
        print title
        if title=="Maslow Optical Calibration":
            content = "<html><head><title>"+title+"</title></head>"
            content +="<body><form method='get'>"
            content +="<input type='hidden' id='widget' name='widget' value='"+title+"'>"
            content +="<button style='width:50px; height:30px;background-color:#ffcc00;' type='submit' name='action' value='Calibrate'>Calibrate</button>"
            content +="<button type='submit' name='action' value='Exit'>Exit</button>"
            content +="<button type='submit' name='action' value='CalibrateSledRotation'>Calibrate Center of Sled Rotation</button>"
            content +="<button type='submit' name='action' value='CalibrateDimensions'>Calibrate Dimensions</button>"
            content +="</form></body><html>"
            return content
        elif title=="FrontPage":
            content = "<html><head><title>"+title+"</title></head>"
            content +="<body><form method='get'>"
            content +="<input type='hidden' id='widget' name='widget' value='"+title+"'>"
            content +="<p>"+title+"</p>"
            content +="<button type='submit' name='action' value='Home'>Home</button>"
            content +="</form></body><html>"
            return content
        else:
            content = "<html><head><title>Could Not Find</title></head>"
            content +="<body><form method='get'>"
            content +="<p>Could not find.</p>"
            content +="</form></body><html>"
            return content


'''
        for widget in self.app.root_window.children:
            if isinstance(widget,FloatLayout):
                for childWidget in widget.children:
                    if isinstance(childWidget,Screen):
                        if (childWidget.name)=="FrontPage":
                            functions = {'Home':widget.home}
                            arguments = { 'CalibrateSledRotation':{'findCenter':True},
                                          'CalibrateDimensions':{'doCalibrate':True}}
                            if _field in functions and _field in arguments:
                                functions[_field](**arguments[_field])
                                return
                            elif _field in functions:
                                print "calling without arguments"
                                functions[_field]()
                                return
'''
