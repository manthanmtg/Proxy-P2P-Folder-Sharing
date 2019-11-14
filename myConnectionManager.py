# -*- coding: utf-8 -*-
"""
Created on Mon Oct 7 14:12:37 2019

Run the program using: python3 NewServer.py

@author: Manthan B Y
"""
import socket, threading
from ServerThread import ClientThread
class Connection:
    def __init__(self, clientSocket, clientAddr, logger, conn_no):
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr
        self.logger = logger
        self.conn_no = conn_no
    def startConnection(self):
        cthread = ClientThread(self)
        self.thread = cthread.getThread()
        cthread.start_thread()
    def receive(self):
        return self.clientSocket.recv(1024).decode() # receiving the request data from the client
    def send(self, resp):
        self.clientSocket.send(resp)
    def close(self):
        self.clientSocket.close()
        ConnectionManager.removeConnection(self.conn_no)

class ConnectionManager:
    curr_connection_no = 0
    current_connections = {}
    lock = threading.Lock()
    def __init__(self, logger):
        self.logger = logger
        self.conn_no = 0
    def getConnectionObject(self, clientSocket, clientAddr):
        self.conn_no = self.getConnectionNumber()
        conn = Connection(clientSocket, clientAddr, self.logger, self.conn_no)
        ConnectionManager.current_connections[self.conn_no] = conn
        self.addConnection(conn)
        return conn
    def getConnectionNumber(self):
        ConnectionManager.lock.acquire()
        ConnectionManager.curr_connection_no += 1
        ConnectionManager.lock.release()
        return ConnectionManager.curr_connection_no
    def addConnection(self, conn):
        ConnectionManager.lock.acquire()
        ConnectionManager.current_connections[self.conn_no] = conn
        print("Current Connections", ConnectionManager.current_connections)
        ConnectionManager.lock.release()
    @staticmethod
    def removeConnection(conn_no):
        ConnectionManager.current_connections.pop(conn_no)