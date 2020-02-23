#!usr/bin/python
import sys
import json


print('Content-type: text/html\r\n\r\n')
import cgitb
cgitb.enable()


args=sys.stdin.readline() #args comes in as a list with one item in it
# which is the parameter that you sent in from javascript
arguments=args[0]


def getTasks(userName):
    """This function will do some processing and get the required return
    value"""
    taskList=["dingdong"]
    #read JSON file and get the info.
    # with open("Somefile.json", 'r') as data_file:
    #     usersDictionary = json.load(data_file)
    # data_file.close()
    # """...do some process ing of data here, which will set some data into
    # the list called taskList"""
    return taskList #Return a list of all the tasks for the user.

print("we got to here!") #json.dumps(getTasks(arguments))
"""convert the json to a string and print it out. what you print out here
will be what you will get as a string in the .responseText of the
XMLHttpRequest
object"""
