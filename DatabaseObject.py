
class DatabaseObject:
    _cols = []
    _columns = dict()
    def __setDict(self, rows_dict):
        for key, value in rows_dict.items():
            self._columns[key] = value
        #self._columns = rows_dict
        #_columnValues = rows_dict
    def __init__(self, dict_Values):
        self._columns = dict((key, '') for key in self._cols)
        self.__setDict(dict_Values)
    def printme(self):
        print(self._columns)
    def setCols(self, colsList):
        self._coldict = dict((key, '') for key in colsList)
        #return _coldict
        
        
class userAccount(DatabaseObject):
    _cols = ['email','password','NaCl','create-time','sessionID']







"""Testing"""

def doTesting():
    testDict = {'email':'a','password':'e','NaCl':'d'}
    ua = userAccount(testDict)
    ua.printme()
    
    testDict = {'email':'a','password':'e','NaCl':''}
    ua = userAccount(testDict)
    ua.printme()

if __name__ == '__main__':
    doTesting()