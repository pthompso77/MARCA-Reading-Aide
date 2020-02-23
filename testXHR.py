#!usr/bin/python
import sys
import json

args=sys.stdin.readlines() #args comes in as a list with one item in it
which is the parameter that you sent in from javascript

arguments=args[0]
print "Content-Type: text/html"
print ""

def getTasks(userName):
    """This function will do some processing and get the required return
    value"""
    taskList=[]
    #read JSON file and get the info.
    with open("Somefile.json", 'r') as data_file:
        usersDictionary = json.load(data_file)
    data_file.close()
    """...do some process ing of data here, which will set some data into
    the list called taskList"""
    return taskList #Return a list of all the tasks for the user.

print json.dumps(getTasks(arguments))
"""convert the json to a string and print it out. what you print out here
will be what you will get as a string in the .responseText of the
XMLHttpRequest
object"""
