import paho.mqtt.client as mqtt
import time
import random
from mqtt_init import *
from icecream import ic
from datetime import datetime
import sqlite3
import data_acq as da

def time_format():
    return f'{datetime.now()}  Manager|> '

ic.configureOutput(prefix=time_format)
ic.configureOutput(includeContext=False)


#--TBD--
def insert_DB(topic, m_decode):
    # DHT case:
    if 'DHT' in m_decode: 
        value=parse_data(m_decode)
        if value != 'NA':
            da.add_IOT_data(m_decode.split('From: ')[1].split(' Temperature: ')[0], da.timestamp(), value)
            # TODO - update IOT device last_updated         
    # Elec Meter case:
    elif 'Meter' in m_decode:        
        da.add_IOT_data('ElectricityMeter', da.timestamp(), m_decode.split(' Electricity: ')[1].split(' Water: ')[0])
        da.add_IOT_data('WaterMeter', da.timestamp(), m_decode.split(' Water: ')[1])
#--TBD--
def parse_data(m_decode):
    value = 'NA'
    # 'From: ' + self.name+ ' Temperature: '+str(temp)+' Humidity: '+str(hum)
    value = m_decode.split(' Temperature: ')[1].split(' Humidity: ')[0]
    return value

#G1
def insert_battery_status(self, timestamp, battery_level):
        try:
            c.execute("INSERT INTO battery_status (timestamp, battery_level) VALUES (?, ?)", (timestamp, battery_level))
            conn.commit()
        except sqlite3.Error as e:
            ic(f"Database error in battery_status: {e}")
#G2
def insert_relay_error(self, timestamp, error_message):
        try:
            c.execute("INSERT INTO relay_errors (timestamp, error_message) VALUES (?, ?)", (timestamp, error_message))
            conn.commit()
        except sqlite3.Error as e:
            ic(f"Database error in relay_errors: {e}")

#G3
def poka_govno():    
    if topic == "pr/home/SparkleBot":
        if "Battery" in m_decode:
            try:
                battery_level = float(m_decode.split('Battery: ')[1].split('%')[0])
                if battery_level < battery_level_min:
                    warning_message = f"Battery level is below {battery_level}: {battery_level}%"
                    ic(warning_message)
                    
            except (ValueError, IndexError) as e:
                ic(f"Error parsing battery level: {e}")

    elif topic == "pr/home/SparkleBot/Relay":
        if "error" in m_decode.lower():
            error_message = m_decode
            ic(f"Error from RELAYEMU: {error_message}")
            
    elif topic == "pr/home/button/SparkleBot":
        error_message = "ATTENTION : SPARKLEBOT IS ON!"
        ic(error_message)

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
    insert_DB(topic, m_decode)

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
    # main monitoring loop
    client.loop_start()  # Start loop
    client.subscribe(comm_topic+'/#')
    try:
        while conn_time==0:
            #check_DB_for_change(client)
            time.sleep(conn_time+manag_time)
            #check_Data(client) 
            time.sleep(1)       
        ic("con_time ending") 
    except KeyboardInterrupt:
        client.disconnect() # disconnect from broker
        ic("interrrupted by keyboard")

    client.loop_stop()    #Stop loop
    # end session
    client.disconnect() # disconnect from broker
    ic("End manager run script")

if __name__ == "__main__":
    main()
    
