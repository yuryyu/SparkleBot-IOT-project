import socket


nb=1 # 0- HIT-"139.162.222.115", 1 - open HiveMQ - broker.hivemq.com
brokers=[str(socket.gethostbyname('vmm1.saaintertrade.com')), str(socket.gethostbyname('broker.hivemq.com'))]
ports=['80','1883']
usernames = ['MATZI',''] # should be modified for HIT
passwords = ['MATZI',''] # should be modified for HIT
broker_ip=brokers[nb]
port=ports[nb]
username = usernames[nb]
password = passwords[nb]

broker_ip=brokers[nb]
broker_port=ports[nb]
username = usernames[nb]
password = passwords[nb]


# Common/ topics
conn_time = 0 # 0 stands for endless loop
comm_topic = 'pr/home/SparkleBot'
sub_topic = comm_topic + '/sub'
pub_topic = comm_topic + '/pub'

# Acq init data
acqtime = 60.0 # sec
manag_time = 20 # sec

# DB init data 
db_name = 'data/project_data.db' # SQLite
db_init =  False   #False # True if we need reinit smart home setup

# Meters consuption limits"
battery_level_min=30
Elec_max=1.8