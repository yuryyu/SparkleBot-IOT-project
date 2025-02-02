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



def insert_DB(client, topic, m_decode):
    # DHT case:
    if 'DHTEMU' in m_decode:         
        da.add_IOT_data('DHTEMU::Temperature', da.timestamp(), m_decode.split(' ')[1])
        battery_level = m_decode.split(' ')[3].split('%')[0]
        ic(battery_level)  
        da.add_IOT_data('DHTEMU::Battery', da.timestamp(), battery_level)
        if float(battery_level) < battery_level_min:
            warning_message = f"WARNING! Battery level is below {battery_level}: {battery_level}%"
            ic(warning_message)
            send_msg(client, pub_topic, warning_message)   
    
    # RELAYEMU --TBD--
    # You can here proccess and insert another data to local DB



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
    insert_DB(client, topic, m_decode)

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
    
