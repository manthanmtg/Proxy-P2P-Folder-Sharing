import socket, threading
from Main import main
class ClientThread:
    current_running_threads = []
    def __init__(self, conn):
        self.thread = threading.Thread(target = main, args= (conn,))
    def start_thread(self):
        ClientThread.current_running_threads.append(self.thread)
        print("Threads:")
        for t in threading.enumerate():
            print(t)
        print("------------------------------")
        self.thread.start()
    def getThread(self):
        return self.thread