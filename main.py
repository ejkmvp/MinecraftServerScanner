import threading
import time
import logging
from scapy.all import send

#TODO better setup the logger
logging.basicConfig(level=logging.DEBUG)

PACKET_SEND_INTERVAL = .1
SCAN_INTERVAL = 60 * 30

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

connectionTableBuffer = []
playerInformationBuffer = []
serverInformationBuffer = []

#Main Loop
lastScanTime = 0
while True:
    if time.time() > lastScanTime + SCAN_INTERVAL:
        logging.debug