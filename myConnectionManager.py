# -*- coding: utf-8 -*-
"""
Created on Mon Oct 7 14:12:37 2019

Run the program using: python3 NewServer.py

@author: Manthan B Y
"""
import socket, threading
from ServerThread import ClientThread
"""
Connection class:
    needs clientSocket, clientAddr, logger object, connection number while initializing

    This class maintains the connection state of a single object
    
"""
class Connection:
    def __init__(self, clientSocket, clientAddr, logger, conn_no):
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr
        self.logger = logger
        self.conn_no = conn_no
    def startConnection(self):
        cthread = ClientThread(self)    # Asks ClientThread to return an object which contains the thread details of the thread assigned to current connection
        self.thread = cthread.getThread()   # connection object will get the thread that is assigned ( can be useful :) )
        cthread.start_thread()  # ask cthread(user-defined) ( Proxy Design PAttern) to start the thread
    def receive(self):
        return self.clientSocket.recv(1024).decode() # receiving the request data from the client
    def send(self, resp):
        self.clientSocket.send(resp)    # sending response to client
    def close(self):
        self.clientSocket.close()   # closing the connection
        ConnectionManager.removeConnection(self.conn_no)

class ConnectionManager:
    curr_connection_no = 0  # critical section
    current_connections = {}    # critical section
    lock = threading.Lock()
    def __init__(self, logger):
        self.logger = logger
        self.conn_no = 0
    def getConnectionObject(self, clientSocket, clientAddr):
        self.conn_no = self.getConnectionNumber()
        conn = Connection(clientSocket, clientAddr, self.logger, self.conn_no)  # create connection object
        ConnectionManager.current_connections[self.conn_no] = conn
        self.addConnection(conn)    # keep reference of connections in manager
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