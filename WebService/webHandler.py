#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from kivy.app                                import App
from kivy.uix.popup                          import Popup
from kivy.uix.screenmanager                  import Screen
from kivy.uix.floatlayout                    import FloatLayout
from UIElements.frontPage                    import FrontPage
from UIElements.zAxisPopupContent            import ZAxisPopupContent
from CalibrationWidgets.setSprocketsVertical import SetSprocketsVertical
from CalibrationWidgets.measureOutChains     import MeasureOutChains
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
            f = open("WebService/styles/"+self.path)
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return
        if self.path.endswith(".js"):
            print "at js"
            f = open("WebService/scripts/"+self.path)
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
        print self.path
        fields = json.loads(self.data_string)
        if 'action' in fields:
            if 'value' in fields:
                self.executeAction(fields['action'],fields['widget'],fields['value'])
            else:
                self.executeAction(fields['action'],fields['widget'])
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write("OK")
        if 'inputs' in fields:
            print fields['inputs']
            inputDict = self.getInputs(fields['inputs'])
            inputDictJSON = json.dumps(inputDict)
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(inputDictJSON)

    def executeAction(self, _field, _widget, value=None):
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
            functions = {'Home':activeWidget.home,
                         'UpLeft':activeWidget.upLeft,
                         'Up':activeWidget.up,
                         'UpRight':activeWidget.upRight,
                         'Left':activeWidget.left,
                         'Right':activeWidget.right,
                         'DownLeft':activeWidget.downLeft,
                         'Down':activeWidget.down,
                         'DownRight':activeWidget.downRight,
                         'ZAxis':activeWidget.zAxisPopup,
                         'Play':activeWidget.startRun,
                         'Pause':activeWidget.pause,
                         'Stop':activeWidget.stopRun,
                         'BackZ':activeWidget.moveGcodeZ,
                         'Back1':activeWidget.moveGcodeIndex,
                         'Goto':activeWidget.gotoLinePopup,
                         'ForwardZ':activeWidget.moveGcodeZ,
                         'Forward1':activeWidget.moveGcodeIndex,
                         'Macro1':activeWidget.macro,
                         'Macro2':activeWidget.macro
                         }
            arguments = { 'Macro1':{'index': 1},
                          'Macro2':{'index': 2},
                          'BackZ':{'moves': -1},
                          'Back1':{'dist': -1},
                          'FowardZ':{'moves':1},
                          'Forward1':{'dist':1}}
        elif (_widget=="ZAxisPopup"):
            functions = {'SetDist':activeWidget.setDist,
                         'Units':activeWidget.units,
                         'Raise':activeWidget.zOut,
                         'Plunge':activeWidget.goThere,
                         'Lower':activeWidget.zIn,
                         'Traverse':activeWidget.zUp,
                         'Done':activeWidget.close,
                         'DefineZero':activeWidget.zero,
                         'TouchZero':activeWidget.touchZero,
                         'GotoZero':activeWidget.zToZero,
                         'ZToCut':activeWidget.zToCut,
                         }
            arguments = { 'SetDist':{'value':value}}
        elif (_widget=="SetSprockets"):
            functions = {'Left360CCW':activeWidget.LeftCCW360,
                         'Left5CCW':activeWidget.LeftCCW5,
                         'Left1CCW':activeWidget.LeftCCW,
                         'LeftP1CCW':activeWidget.LeftCCWpoint1,
                         'Left360CW':activeWidget.LeftCW360,
                         'Left5CW':activeWidget.LeftCW5,
                         'Left1CW':activeWidget.LeftCW,
                         'LeftP1CW':activeWidget.LeftCWpoint1,
                         'Right360CCW':activeWidget.RightCCW360,
                         'Right5CCW':activeWidget.RightCCW5,
                         'Right1CCW':activeWidget.RightCCW,
                         'RightP1CCW':activeWidget.RightCCWpoint1,
                         'Right360CW':activeWidget.RightCW360,
                         'Right5CW':activeWidget.RightCW5,
                         'Right1CW':activeWidget.RightCW,
                         'RightP1CW':activeWidget.RightCWpoint1,
                         'Automatic':activeWidget.setVerticalAutomatic,
                         'SetZero':activeWidget.setZero,
                         }
            arguments = { }
        elif (_widget=="CalibrateChainLengths"):
            functions = {'AdjustLeft':activeWidget.startCountDownL,
                         'AdjustRight':activeWidget.startCountDownR,
                         'MoveToCenter':activeWidget.moveToCenter,
                         'Stop':activeWidget.stop,
                         'Next':activeWidget.next,
                         }
            arguments = { }



        if _field in functions and _field in arguments:
            functions[_field](**arguments[_field])
            return
        elif _field in functions:
            print "calling without arguments"
            functions[_field]()
            return

    def getInputs(self, inputs):
        self.app = App.get_running_app()
        activeWidget = self.app.activeWidget
        inputDict = {}
        print inputs
        for input in inputs:
            if type(activeWidget) is ZAxisPopupContent:
                if input=="distanceValue":
                    inputDict[input] = round(activeWidget.data.zStepSizeVal,3)
                if input=="unitsLabel":
                    inputDict[input] = activeWidget.data.zPopupUnits
        print inputDict
        return inputDict

    def getContentForActiveWidget(self):
        self.app = App.get_running_app()
        _widget = self.app.activeWidget
        print _widget
        if type(_widget) is OpticalCalibrationCanvas:
            fileName = "OpticalCalibration.html"
        elif type(_widget) is FrontPage:
            fileName = "FrontPage.html"
        elif type(_widget) is ZAxisPopupContent:
            fileName = "ZAxisPopup.html"
        elif type(_widget) is SetSprocketsVertical:
            fileName = "SetSprockets.html"
        elif type(_widget) is MeasureOutChains:
            fileName = "MeasureOutChains.html"
        else:
            fileName = "NotFound.html"
        f = open("WebService/views/"+fileName)
        content = f.read()

        content+="<script>disableBtn()</script><html>"
        return content
