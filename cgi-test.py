#!/usr/bin/env python3
import cgi, cgitb; cgitb.enable()

f = cgi.FieldStorage()
mydata = f['MYDATA']

cgi.test()

print("yo, mydata is ",mydata)