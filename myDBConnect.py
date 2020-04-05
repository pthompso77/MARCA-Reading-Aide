"""
moving DB connection strings to separate file
for security, do not upload files with actual values!
(ﾉﾟ0ﾟ)ﾉ~
"""
from realDBConnect import myCreds
host = myCreds['host']
user = myCreds['user']
pw = myCreds['pw']
schema = myCreds['schema']
