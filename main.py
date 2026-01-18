import threading
import time
import logging
import queue
from scapy.all import send

#TODO better setup the logger
logging.basicConfig(level=logging.DEBUG)

PACKET_SEND_INTERVAL = .1       # 100 milliseconds
SCAN_INTERVAL = 60 * 10         # 10 minutes  
INTERVALS_PER_DEAD_SCAN = 6     # 60 minutes

send_lock = threading.Lock()
data_lock = threading.Lock()

lastPacketSendTime = 0
def sendPacket(packet):
    with send_lock:
        global lastPacketSendTime
        logging.debug("Acquired send lock")
        while time.time() < lastPacketSendTime + PACKET_SEND_INTERVAL:
            logging.debug("Trying to send packet too soon, waiting...")
        logging.debug("Sending packet")
        lastPacketSendTime = time.time()
        send(packet)
        logging.debug("Finished sending packet")

def logData(data):
    pass

#buffer for new connection table entries
connectionTableBuffer = []

#buffer for new player information table entries
playerInformationBuffer = []

#buffer for new server information table entries
serverInformationBuffer = []

#Dictionary from IP Addresses to TTLs
ipAddressTable = {}

#Send queue - queue for the initial TCP packets to send out
initialSendQueue = queue.Queue()
sendQueue = queue.Queue()



def senderThread():
    global initialSendQueue
    global sendQueue
    while True:
        message = None
        if sendQueue.size() != 0:
            message = sendQueue.pop(0)
            logging.debug("Sending message from sendqueue")
        elif initialSendQueue.size() != 0:
            message = initialSendQueue.pop(0)
            logging.debug("Sending message from initial send queue")
        if message is not None:
            sendPacket(message)

def receiverThread():
    



#Main Loop
lastScanTime = 0
while True:
    if time.time() > lastScanTime + SCAN_INTERVAL:
        logging.debug("SCAN Interval reached, starting a scan")
        lastScanTime = time.time()

        #for each ip address, if the TTL is 0, then add it. Then, set the TTL to 6
        keyList = list(ipAddressTable.keys())
        for key in keyList:
            ipAddressTable[key] -= 1
            if ipAddressTable[key] == 0:
                ipAddressTable[key] = 6
                logging.debug(f"Adding ip Address {key} to send queue")
                initialSendQueue.put(createTCPPacket(key))


