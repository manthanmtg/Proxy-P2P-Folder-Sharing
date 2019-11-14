# -*- coding: utf-8 -*-
"""
Created on Mon Oct 7 14:12:37 2019

Run the program using: python3 NewServer.py

@author: Manthan B Y, Abhishek Patil, Adeesh
"""
# import all the required modules and code snippets here...
import time
import os
from os import path
from mimetypes import MimeTypes
import urllib
import socket
from html_snips import *
from resp_header import get_header
from my_zipper import create_zip
import logging
import urllib.parse
from Main import main
import myConnectionManager
logging.basicConfig(filename="server.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 
logger = logging.getLogger()
logger.setLevel(logging.DEBUG) 
home_dir = os.environ['HOME']
# home_dir = "/mnt/m"
times = 0
serverPort = 12555          # serverPort for the server
serverAddr = ('', serverPort)
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Using ipv4 addressing and TCP stream
serverSocket.bind(serverAddr)   # binding the address to the socket
manager = myConnectionManager.ConnectionManager(logger)
response = bytes()      # reponse bytes object
serverSocket.listen(5)
logger.info('The server lsitening at ' + str(serverPort))
prev_req_name = ''
prev_req_time = -1000   # previous request time to handle duplicate requests
prev_addr = 0
while 1:
    clientSocket, clientAddr = serverSocket.accept()
    connection = manager.getConnectionObject(clientSocket, clientAddr)
    connection.startConnection()
serverSocket.close()
