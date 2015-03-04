#--------------------//Intermediate SERVER//-----------------------
__author__ = "Ganapathy Raman"

""" @Arthor: Ganapathy Raman Madanagopal
    This is a program which act as a intermediate filesever or can be considered as an 
    application level gateway. On receiving a file download request from a client 
    forwards the request to the real File Server. It downloads the file from the real file sever
    and returns it back to the requested client. 
"""

import socket
import threading
import os

def downloadFromOriginalServer(filename):
    realServerIP = '50.0.0.2'
    realPort = 5000
    s = socket.socket()

    try:
        s.connect((realServerIP, realPort))
    except e:
        print e
        return False

    s.send(filename)
    data = s.recv(1024)

    if data[:6] == 'EXISTS':
        filesize = long(data[6:])
        s.send("OK")
        f = open(filename, 'wb')
        data = s.recv(1024)
        totalRecv = len(data)
        f.write(data)
        while totalRecv < filesize:
            data = s.recv(1024)
            totalRecv += len(data)
            f.write(data)
            print "{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done"
        print "Download Complete!"
        f.close()
        return True
    else:
        print "File Does Not Exist!"
        return False

def RetrFile(name, sock):
    filename = sock.recv(1024)

    try:
        result = downloadFromOriginalServer(filename)
    except:
        print "[Error]: Unable to process the request"
        sock.send("ERR ")
        sock.close()
        return

    if result == True:
        if os.path.isfile(filename):
            sock.send("EXISTS " + str(os.path.getsize(filename)))
            userResponse = sock.recv(1024)
            if userResponse[:2] == 'OK':
                with open(filename, 'rb') as f:
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
                    while bytesToSend != "":
                        bytesToSend = f.read(1024)
                        sock.send(bytesToSend)
    else:
        sock.send("ERR ")

    sock.close()

def Main():
    selfIP = '0.0.0.0'
    port = 5000


    s = socket.socket()
    s.bind((selfIP,port))

    s.listen(5)

    print "Server Started."
    while True:
        c, addr = s.accept()
        print "client connedted ip:<" + str(addr) + ">"
        t = threading.Thread(target=RetrFile, args=("RetrThread", c))
        t.start()

    s.close()

if __name__ == '__main__':
    Main()
