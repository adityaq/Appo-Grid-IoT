################################ Start
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient # AWS IoT Python SDK libary for AWS (You can install it by this command  sudo pip3 install AWSIoTPythonSDK (Only for Raspberry Pi))
import time # Time libary to give delay
import paho.mqtt.client as mqtt # Mqtt libary for NodeMCU to Raspberry Pi (You can install it by this command  sudo pip3 install paho-mqtt (Only for Raspberry Pi))
################################
myMQTTClient = AWSIoTMQTTClient("Appo-Grid-IoT-Client") # Define a Client
myMQTTClient.configureEndpoint("a3eclw3540smf4-ats.iot.us-west-2.amazonaws.com", 8883) # End Point
myMQTTClient.configureCredentials(r"C:\Users\admin\Desktop\Appo-Grid-IoT\Appo-Grid-Amazon-Web-Services-Certificate\Appo-Grid-IoT-Root-CA.txt", r"C:\Users\admin\Desktop\Appo-Grid-IoT\Appo-Grid-Amazon-Web-Services-Certificate\Appo-Gris-IoT-Private.pem.key",r"C:\Users\admin\Desktop\Appo-Grid-IoT\Appo-Grid-Amazon-Web-Services-Certificate\Appo-Grid-IoT-Certificate.pem.crt") # Root CA, Private, Certificate are there to intract with AWS
myMQTTClient.configureOfflinePublishQueueing(-1)  
myMQTTClient.configureDrainingFrequency(2)  
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)
time.sleep(5) # Wating for 5 second after starting the loop
################################
def on_message(client, userdata, message): # Note - Json is coming from the NodeMCU so that's whay we are not converting it hear for AWS
    myMQTTClient.publish("Appo-Grid-IoT-Pub",str(message.payload.decode("utf-8")), 0) # Publish the payload to the AWS from NodeMCU with the format of Json
    print("Json coming by device is this ===>>",str(message.payload.decode("utf-8"))) # Printing the data which is coming from NodeMCU
################################
client = mqtt.Client("Appo-Grid-IoT-Client") # Define a Client for NodeMCU
client.on_message=on_message 
client.connect("192.168.1.6") # Raspberry Pi Ip (You can run this command to get the Ip hostname -I)
client.loop_start() # Starting the loop forever to get the data
client.subscribe("Appo-Grid-IoT") # Topic to subscribe for NodeMCU to Raspberry Pi
################################
connecting_time = time.time() + 10
if time.time() < connecting_time: # Checking that it is connected or not to AWS 
    myMQTTClient.connect()
    myMQTTClient.publish("Appo-Grid-IoT-Pub", '{ "Status": "Connected"}', 0) # Sending to AWS this device is connected in the format of Json
    print ("MQTT Client connection success!")
    
else:
    print ("Error: Check your AWS details in the program")
################################ end
