from abc import ABC, abstractmethod
import dbConnect

class DatabaseObject(ABC):
    _tableName = ''
    _cols = []
    _pk = ''
    _rowVals = dict()
    def __setDict(self, rows_dict):
        for key, value in rows_dict.items():
            self._rowVals[key] = value
    def __init__(self, dict_Values):
        self._rowVals = dict((key, '') for key in self._cols)
        self.__setDict(dict_Values)
        self._myDBconnection = dbConnect.getDBConnection(printing=False)
    def _printme(self): #just for testing
        print(self._rowVals)
    @abstractmethod
    def updateDB(self, newValues_dict):
        # TODO some kind of error handling for dict/col values
        pass


class userAccount(DatabaseObject):
    _tableName = 'userAccounts'
    _cols = ['email','password','NaCl','create-time','sessionID']
    _pk = _cols[0]
    def updateDB(self, newValues_dict):
        #TODO make sure newValues has only one value? maybe...
        items = list(newValues_dict.items())
        (key, value) = items[0]
        '''	--  update email address'''
        query = "UPDATE `{tableName}`\
        SET `{setKey}` = '{newValue}'\
        WHERE `{whereKey}` = '{whereValue}';\
        ".format(tableName=self._tableName, setKey=key, newValue=value,\
                 whereKey=self._pk, whereValue=self._rowVals[self._pk])
        #dbConnect.runSetQuery(self._myDBconnection, query)
        print(query)
        results = dbConnect.runSetQuery(self._myDBconnection, query)
        print(results)
    







"""Testing"""

def doTesting():
    testDict = {'email':'a','password':'e','NaCl':'d'}
    ua = userAccount(testDict)
    ua._printme()
    
    testDict = {'email':'testemail1@mail.com','password':'e','NaCl':''}
    ua = userAccount(testDict)
    ua._printme()
    
    newVals = {'email':'new email'}
    ua.updateDB(newVals)
    ua._printme()
    

if __name__ == '__main__':
    doTesting()