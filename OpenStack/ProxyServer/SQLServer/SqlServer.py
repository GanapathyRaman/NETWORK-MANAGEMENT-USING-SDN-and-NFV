#!/usr/bin/env python

__author__ = "Ganapathy Raman"

"""
This program on receiving a request from proxy server, queries the requested name from the Sqlite3 database and
sends back the results
"""

import socket
import os
import sqlite3
import socket
import pickle

host = ''
port = 50000
backlog = 5
size = 8192
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)
print "Started Server at port", port
while 1:
    client, address = s.accept()
    name = client.recv(size)
    if name:
        conn = sqlite3.connect('test.db')
        print "Opened database successfully";
        command = "select * from company where name = '%s'" %name
        print command

        try:
            cursor = conn.execute(command)
        except:
            client.send("NULL")
            client.close()
        ID = None
        if cursor:
            for row in cursor:
               ID = row[0]
               NAME = row[1]
               AGE = row[2]
               ADDRESS = row[3]
               SALARY = row[4]
            if ID:
                queryValue = str(ID) + " " + str(NAME) + " " + str(AGE) + " " + str(ADDRESS) + " " + str(SALARY)
                client.send(queryValue)
        else:
            client.send("NULL")
    client.close()
