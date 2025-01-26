import os
import sys
import PyQt5
import random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paho.mqtt.client as mqtt
import time
import datetime
from mqtt_init import *


# Creating Client name - should be unique 
global clientname
r = random.randrange(1, 100000)
clientname = "IOT_client-Id-" + str(r)


class Mqtt_client():
    
    def __init__(self):
        # broker IP address:
        self.broker = ''
        self.topic = ''
        self.port = '' 
        self.clientname = ''
        self.username = ''
        self.password = ''        
        self.subscribeTopic = ''
        self.publishTopic = ''
        self.publishMessage = ''
        self.on_connected_to_form = ''
        
    # Setters and getters
    def set_on_connected_to_form(self, on_connected_to_form):
        self.on_connected_to_form = on_connected_to_form
    def get_broker(self):
        return self.broker
    def set_broker(self, value):
        self.broker = value         
    def get_port(self):
        return self.port
    def set_port(self, value):
        self.port = value     
    def get_clientName(self):
        return self.clientName
    def set_clientName(self, value):
        self.clientName = value        
    def get_username(self):
        return self.username
    def set_username(self, value):
        self.username = value     
    def get_password(self):
        return self.password
    def set_password(self, value):
        self.password = value         
    def get_subscribeTopic(self):
        return self.subscribeTopic
    def set_subscribeTopic(self, value):
        self.subscribeTopic = value        
    def get_publishTopic(self):
        return self.publishTopic
    def set_publishTopic(self, value):
        self.publishTopic = value         
    def get_publishMessage(self):
        return self.publishMessage
    def set_publishMessage(self, value):
        self.publishMessage = value 
        
        
    def on_log(self, client, userdata, level, buf):
        print("log: " + buf)
            
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("connected OK")
            self.on_connected_to_form()            
        else:
            print("Bad connection Returned code=", rc)
            
    def on_disconnect(self, client, userdata, flags, rc=0):
        print("DisConnected result code " + str(rc))
            
    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        print("message from:" + topic, m_decode)

        # Trigger warning if message contains "error"
        if "error" in m_decode.lower():
            mainwin.warningDock.add_warning(f"ALERT: {m_decode}")  # Show warning/alert message in the dock
        if topic == "pr/home/SparkleBot":
          if "Battery" in m_decode:
            battery_level = float(m_decode.split('Battery: ')[1].split('%')[0])
            if battery_level < 70:
                warning_message = f"Battery level is below 70%: {battery_level}%"
                mainwin.warningDock.add_warning(f"ALERT: battery is below 70%!!!")  # Show warning/alert message in the dock  
        if topic == "pr/home/button/SparkleBot":
        # Add an error message when the button is clicked
         if m_decode.lower() == "Start Cleaning your home!":
                mainwin.warningDock.add_warning("ALERT: Button pressed on pr/home/button/SparkleBot")
        mainwin.subscribeDock.update_mess_win(m_decode)
        if topic == "pr/home/button/SparkleBot":
    # Use case-insensitive comparison
         if "start cleaning" in m_decode.lower():
          mainwin.warningDock.add_warning("ALERT: SparkleBot is ON")


    def connect_to(self):
        # Init paho mqtt client class        
        self.client = mqtt.Client(self.clientname, clean_session=True) # create new client instance        
        self.client.on_connect = self.on_connect  #bind callback function
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log
        self.client.on_message = self.on_message
        self.client.username_pw_set(self.username, self.password)        
        print("Connecting to broker ", self.broker)        
        self.client.connect(self.broker, self.port)     #connect to broker
    
    def disconnect_from(self):
        self.client.disconnect()                   
    
    def start_listening(self):        
        self.client.loop_start()        
    
    def stop_listening(self):        
        self.client.loop_stop()    
    
    def subscribe_to(self, topic):        
        self.client.subscribe(topic)
              
    def publish_to(self, topic, message):
        self.client.publish(topic, message)        


class ConnectionDock(QDockWidget):
    """Main """
    def __init__(self, mc):
        QDockWidget.__init__(self)
        
        self.mc = mc
        self.mc.set_on_connected_to_form(self.on_connected)
        self.eHostInput = QLineEdit()
        self.eHostInput.setInputMask('999.999.999.999')
        self.eHostInput.setText(broker_ip)
        
        self.ePort = QLineEdit()
        self.ePort.setValidator(QIntValidator())
        self.ePort.setMaxLength(4)
        self.ePort.setText(broker_port)
        
        self.eClientID = QLineEdit()
        global clientname
        self.eClientID.setText(clientname)
        
        self.eUserName = QLineEdit()
        self.eUserName.setText(username)
        
        self.ePassword = QLineEdit()
        self.ePassword.setEchoMode(QLineEdit.Password)
        self.ePassword.setText(password)
        
        self.eKeepAlive = QLineEdit()
        self.eKeepAlive.setValidator(QIntValidator())
        self.eKeepAlive.setText("60")
        
        self.eSSL = QCheckBox()
        
        self.eCleanSession = QCheckBox()
        self.eCleanSession.setChecked(True)
        
        self.eConnectbtn = QPushButton("Connect", self)
        self.eConnectbtn.setToolTip("click me to connect")
        self.eConnectbtn.clicked.connect(self.on_button_connect_click)
        self.eConnectbtn.setStyleSheet("background-color: red")
        
        formLayot = QFormLayout()
        formLayot.addRow("Host", self.eHostInput)
        formLayot.addRow("Port", self.ePort)
        formLayot.addRow("Client ID", self.eClientID)
        formLayot.addRow("User Name", self.eUserName)
        formLayot.addRow("Password", self.ePassword)
        formLayot.addRow("Keep Alive", self.eKeepAlive)
        formLayot.addRow("SSL", self.eSSL)
        formLayot.addRow("Clean Session", self.eCleanSession)
        formLayot.addRow("", self.eConnectbtn)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)     
        self.setWindowTitle("Connect") 
        
    def on_connected(self):
        self.eConnectbtn.setStyleSheet("background-color: green")
                    
    def on_button_connect_click(self):
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientName(self.eClientID.text())
        self.mc.set_username(self.eUserName.text())
        self.mc.set_password(self.ePassword.text())        
        self.mc.connect_to()        
        self.mc.start_listening()


class PublishDock(QDockWidget):
    """Publisher """
    def __init__(self, mc):
        QDockWidget.__init__(self)
        
        self.mc = mc        
                
        self.ePublisherTopic = QLineEdit()
        self.ePublisherTopic.setText(pub_topic)

        self.eQOS = QComboBox()
        self.eQOS.addItems(["0", "1", "2"])

        self.eRetainCheckbox = QCheckBox()

        self.eMessageBox = QPlainTextEdit()        
        self.ePublishButton = QPushButton("Publish", self)
        
        formLayot = QFormLayout()        
        formLayot.addRow("Topic", self.ePublisherTopic)
        formLayot.addRow("QOS", self.eQOS)
        formLayot.addRow("Retain", self.eRetainCheckbox)
        formLayot.addRow("Message", self.eMessageBox)
        formLayot.addRow("", self.ePublishButton)
        
        self.ePublishButton.clicked.connect(self.on_button_publish_click)
        
        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setWidget(widget) 
        self.setWindowTitle("Publish")         
       
    def on_button_publish_click(self):
        self.mc.publish_to(self.ePublisherTopic.text(), self.eMessageBox.toPlainText())
        self.ePublishButton.setStyleSheet("background-color: yellow")


class SubscribeDock(QDockWidget):
    """Subscribe """
    def __init__(self, mc):
        QDockWidget.__init__(self)        
        self.mc = mc
        
        self.eSubscribeTopic = QLineEdit()
        self.eSubscribeTopic.setText(sub_topic) 
        
        self.eQOS = QComboBox()
        self.eQOS.addItems(["0", "1", "2"])
        
        self.eRecMess = QTextEdit()

        self.eSubscribeButton = QPushButton("Subscribe", self)
        self.eSubscribeButton.clicked.connect(self.on_button_subscribe_click)

        formLayot = QFormLayout()       
        formLayot.addRow("Topic", self.eSubscribeTopic)
        formLayot.addRow("QOS", self.eQOS)
        formLayot.addRow("Received", self.eRecMess)
        formLayot.addRow("", self.eSubscribeButton)
                
        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setWidget(widget)
        self.setWindowTitle("Subscribe")
        
    def on_button_subscribe_click(self):
        print(self.eSubscribeTopic.text())
        self.mc.subscribe_to(self.eSubscribeTopic.text())
        self.eSubscribeButton.setStyleSheet("background-color: yellow")
    
    def update_mess_win(self, text):
        self.eRecMess.append(text)


class WarningDock(QDockWidget):
    """Warning/Alarms Status"""
    
    def __init__(self, mc):
        QDockWidget.__init__(self)
        
        self.mc = mc
        
        self.eWarningMessage = QTextEdit()  # Text area for warnings
        self.eWarningMessage.setReadOnly(True)  # Make the text area read-only
        
        self.eClearButton = QPushButton("Clear", self)  # Button to clear messages
        self.eClearButton.clicked.connect(self.on_button_clear_click)
        
        formLayout = QFormLayout()
        formLayout.addRow("Warnings/Alarms", self.eWarningMessage)
        formLayout.addRow("", self.eClearButton)
        
        widget = QWidget(self)
        widget.setLayout(formLayout)
        self.setWidget(widget)
        self.setWindowTitle("Warnings/Alarms")
        
    def on_button_clear_click(self):
        """Clear the warning messages."""
        self.eWarningMessage.clear()

    def add_warning(self, message):
        """Add a warning message to the text area."""
        self.eWarningMessage.append(message)


class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        
        # Init of Mqtt_client class
        self.mc = Mqtt_client()
        
        # general GUI settings
        self.setUnifiedTitleAndToolBarOnMac(True)

        # set up main window
        self.setGeometry(30, 100, 800, 600)
        self.setWindowTitle('SparkleBot Main GUI')

        # Init QDockWidget objects        
        self.connectionDock = ConnectionDock(self.mc)        
        self.publishDock = PublishDock(self.mc)
        self.subscribeDock = SubscribeDock(self.mc)
        self.warningDock = WarningDock(self.mc)  # Add the WarningDock

        # Add dock widgets to the main window
        self.addDockWidget(Qt.TopDockWidgetArea, self.connectionDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.publishDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.subscribeDock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.warningDock)  # Place the WarningDock on the right


app = QApplication(sys.argv)
mainwin = MainWindow()
mainwin.show()
app.exec_()