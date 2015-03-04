#----------------------//CLIENT//-------------------------------

__author__ = "Ganapathy Raman"

"""
    This is a python program which act as a client for downlaoding a file from a remote server
"""
import socket
import os

def Main():
    intermediateServerIP = '180.180.180.5' #Intermediate Server IP address
    port = 5000

    s = socket.socket()
    s.connect((intermediateServerIP, port))

    filename = raw_input("Filename? -> ")
    if filename != 'q':
        s.send(filename)
        data = s.recv(1024)
        if data[:6] == 'EXISTS':
            filesize = long(data[6:])
            message = raw_input("File exists, " + str(filesize) +"Bytes, download? (y/n)? -> ")
            if message == 'y':
                s.send("OK")
                path, Nfilename = os.path.split(filename)
                newfilename = 'new_' + Nfilename
                newpath = os.path.join(path, newfilename)
                print newpath
                f = open(newpath, 'wb')
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
        else:
            print "File Does Not Exist!"

    s.close()


if __name__ == '__main__':
    Main()
