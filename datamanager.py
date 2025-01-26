import paho.mqtt.client as mqtt
import time
import random
from mqtt_init import *
from icecream import ic
from datetime import datetime
import sqlite3
from PyQt5 import QtWidgets, QtCore

def time_format():
    return f'{datetime.now()}  Manager|> '

ic.configureOutput(prefix=time_format)
ic.configureOutput(includeContext=False)

# Database setup
def create_database():
    conn = sqlite3.connect('project_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS battery_status (timestamp TEXT, battery_level REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS relay_errors (timestamp TEXT, error_message TEXT)''')
    conn.commit()
    return conn

conn = create_database()
c = conn.cursor()

# GUI setup
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Project GUI')
        self.layout = QtWidgets.QVBoxLayout()
        self.message_label = QtWidgets.QLabel('')
        self.layout.addWidget(self.message_label)
        self.setLayout(self.layout)

    def update_gui(self, message):
        self.message_label.setText(message)
        QtWidgets.QApplication.processEvents()

    def insert_battery_status(self, timestamp, battery_level):
        try:
            c.execute("INSERT INTO battery_status (timestamp, battery_level) VALUES (?, ?)", (timestamp, battery_level))
            conn.commit()
        except sqlite3.Error as e:
            ic(f"Database error in battery_status: {e}")

    def insert_relay_error(self, timestamp, error_message):
        try:
            c.execute("INSERT INTO relay_errors (timestamp, error_message) VALUES (?, ?)", (timestamp, error_message))
            conn.commit()
        except sqlite3.Error as e:
            ic(f"Database error in relay_errors: {e}")

app = QtWidgets.QApplication([])
main_window = MainWindow()
main_window.show()

# MQTT callback functions
def on_log(client, userdata, level, buf):
    ic("log: " + buf)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        ic("Connected OK")
    else:
        ic(f"Bad connection, returned code: {rc}")

def on_disconnect(client, userdata, flags, rc=0):
    ic(f"Disconnected with result code: {rc}")

def on_message(client, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    ic(f"Message from: {topic}", m_decode)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if topic == "pr/home/SparkleBot":
        if "Battery" in m_decode:
            try:
                battery_level = float(m_decode.split('Battery: ')[1].split('%')[0])
                if battery_level < 70:
                    warning_message = f"Battery level is below 70%: {battery_level}%"
                    ic(warning_message)
                    main_window.update_gui(warning_message)
                    QtCore.QTimer.singleShot(0, lambda: main_window.insert_battery_status(timestamp, battery_level))
            except (ValueError, IndexError) as e:
                ic(f"Error parsing battery level: {e}")

    elif topic == "pr/home/SparkleBot/Relay":
        if "error" in m_decode.lower():
            error_message = m_decode
            ic(f"Error from RELAYEMU: {error_message}")
            main_window.update_gui(f"Error from RELAYEMU: {error_message}")
            QtCore.QTimer.singleShot(0, lambda: main_window.insert_relay_error(timestamp, error_message))
    elif topic == "pr/home/button/SparkleBot":
        error_message = "ATTENTION : SPARKLEBOT IS ON!"
        ic(error_message)
        main_window.update_gui(error_message)
        QtCore.QTimer.singleShot(0, lambda: main_window.insert_relay_error(timestamp, error_message))

def send_msg(client, topic, message):
    ic(f"Sending message: {message}")
    client.publish(topic, message)

def client_init(cname):
    r = random.randrange(1, 10000000)
    ID = f"{cname}{r + 21}"
    client = mqtt.Client(ID, clean_session=True)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_log = on_log
    client.on_message = on_message

    if username:
        client.username_pw_set(username, password)

    ic(f"Connecting to broker {broker_ip}")
    client.connect(broker_ip, int(port))
    return client

def main():
    cname = "Manager-"
    client = client_init(cname)
    client.loop_start()
    client.subscribe("pr/home/SparkleBot")
    client.subscribe("pr/home/SparkleBot/Relay")
    client.subscribe("pr/home/button/SparkleBot")

    try:
        while conn_time == 0:
            time.sleep(conn_time + 5)
            ic(f"Time for sleep: {conn_time + 5}")
            time.sleep(3)
    except KeyboardInterrupt:
        ic("Interrupted by keyboard")
        client.disconnect()

    client.loop_stop()
    ic("End manager run script")

if __name__ == "__main__":
    main()
    app.exec_()
