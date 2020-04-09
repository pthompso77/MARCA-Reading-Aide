"""
moving DB connection strings to separate file
for security, do not upload files with actual values!
(ﾉﾟ0ﾟ)ﾉ~
"""
try:
    #print('trying: `from marca.realDBConnect import myCreds`')
    from marca.realDBConnect import myCreds
    #print('success')
except Exception as e:
    #print('failed')
    #print('trying: `from realDBConnect import myCreds`')
    try:
        from realDBConnect import myCreds
        #print('success')
    except Exception as e:
        msg = 'still no go, E: '
        print('msg',e)

host = myCreds['host']
user = myCreds['user']
pw = myCreds['pw']
schema = myCreds['schema']
