from abc import ABC, abstractmethod

class DatabaseObject(ABC):
    _cols = []
    _pk = ''
    _columns = dict()
    def __setDict(self, rows_dict):
        for key, value in rows_dict.items():
            self._columns[key] = value
        #self._columns = rows_dict
        #_columnValues = rows_dict
    def __init__(self, dict_Values):
        self._columns = dict((key, '') for key in self._cols)
        self.__setDict(dict_Values)
    def _printme(self): #just for testing
        print(self._columns)
    @abstractmethod
    def updateDB(self, newValues_dict):
        pass


class userAccount(DatabaseObject):
    _cols = ['email','password','NaCl','create-time','sessionID']
    _pk = _cols[0]
    def updateDB(self, newValues_dict):
        pass
    







"""Testing"""

def doTesting():
    testDict = {'email':'a','password':'e','NaCl':'d'}
    ua = userAccount(testDict)
    ua._printme()
    
    testDict = {'email':'a','password':'e','NaCl':''}
    ua = userAccount(testDict)
    ua._printme()

if __name__ == '__main__':
    doTesting()