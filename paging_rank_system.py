import sqlite3
"""Paging Rank System
This module is the system for web page rank based on the linked numbers of each link.
"""
class PagingRank(object):
    """PagingRank class
    This class for paging rank.
    """
    def __init__(self):
        """Initializer
        Initialize object and prompt the program has been ignited.
        """
        print("Hello, the code begin")

    def fill_data(self):
        """Fill data to list from database.
        """
        data = []
        conn = sqlite3.connect('search_engine_DB.db')
        c = conn.cursor()
        print("Opened database successfully")
        cursor = c.execute("SELECT ID, KEYWORD, LINK, COUNT from WEBPAGE")
        for row in cursor:
            data.append(row)
        conn.close()
        return data

    def sort_third(self, val):
        """return linked numbers in database"""
        return val[3]
    
    def sort_data(self, data):
        """Sort the list based on linked counts."""
        data.sort(key = self.sort_third, reverse = True)
        return data
    
    def start(self):
        """start the program"""
        data = self.fill_data()
        data = self.sort_data(data)
        for item in data:
            print(item)
        return data
        
        
        

if __name__ =="__main__":
    pr = PagingRank()
    pr.start()
