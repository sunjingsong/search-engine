#!/usr/bin/python
"""Web Page Crawler
   This module is a crawler which crawling web pages from "https://google.com".
"""
import sqlite3

import requests    
import re    
from urllib.parse import urlparse    

class PyCrawler(object):
    """PyCrawler class
       This class is the class for crawling.
    """
    def __init__(self, starting_url):
        """Initializer
           Parameters
           -----------
           starting_url: str
           the initial searching point is initialized

           Returns
           -----------
           None
        """
        self.starting_url = starting_url
        self.visited = set()    

    def get_html(self, url):
        """Get HTML Page
           Parameters
           -----------
           url: str
           the http address for parsing

           Returns
           -----------
           str
             AHTML Web Page
        """
        try:    
            html = requests.get(url)    
        except Exception as e:    
            print(e)    
            return ""    
        return html.content.decode('latin-1')    

    def get_links(self, url):
        """Get Link
           Parameters
           -----------
           url: str
           the http address for parsing

           Returns
           -----------
           set
             a set of links in the web page
        """
        
        html = self.get_html(url)    
        parsed = urlparse(url)    
        base = f"{parsed.scheme}://{parsed.netloc}"    
        links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', html)    
        for i, link in enumerate(links):    
            if not urlparse(link).netloc:    
                link_with_base = base + link    
                links[i] = link_with_base    

        return set(filter(lambda x: 'mailto' not in x, links))    

    def extract_info(self, url):
        """Get Meta Data
           Parameters
           -----------
           url: str
           the http address for parsing

           Returns
           -----------
           dict
             a dict of {description: link}
        """
        html = self.get_html(url)    
        meta = re.findall("<meta .*?name=[\"'](.*?)['\"].*?content=[\"'](.*?)['\"].*?>", html)    
        return dict(meta)    

    def crawl(self, url):
        """Recursive Crawling The Web pages
           Parameters
           -----------
           url: str
           the http address for parsing

           Crawls each web page and extracts key words, links, and linked number. Put the information
           into database.
        """
        
        # noise word stored in a set for checking
        noise = {"a", "an", "the", "and", "or", "of", "to", "be", "is", "in", "out", "by", "as", "at", "off"}
        for link in self.get_links(url):    
            if link in self.visited:
                print("LINK REPEATED ################################################################")
                conn = sqlite3.connect('search_engine_DB.db')
                c = conn.cursor()
                print("Opened database successfully!")
                c.execute("UPDATE WEBPAGE set COUNT = COUNT + 1 where LINK = '" + link + "'")
                conn.commit()
                print("Records updated successfully")
                conn.close()
                continue
            
            self.visited.add(link)    
            info = self.extract_info(link)

            desc = info.get('description')
            keyword = info.get('keywords')
            if (desc == None and keyword == None):
                continue
            word = ""
            if (keyword != None):
                word += keyword
            if (desc != None):
                word += desc
            
            words = re.split(r'[^A-Za-z]', word)
            for i in range(len(words)):
                words[i] = words[i].strip()

            words = filter(lambda x: x.lower() not in noise and len(x) > 1, words)
            

            words = list(set(words))
            word = ' '.join(words)
            word = word.strip()
            if (word != ""  and word != None):
                conn = sqlite3.connect('search_engine_DB.db')
                c = conn.cursor()
                print("Opened database successfully!")
                c.execute("INSERT INTO WEBPAGE (KEYWORD,LINK,COUNT) \
                    VALUES (" + "'" + word.lower() + "', '" + link + "', " + "1)")
                conn.commit()
                print("Records created successfully")
                conn.close()
            print("Hello: " + word)
            print(f"""Link: {link}    
Description: {info.get('description')}    
Keywords: {info.get('keywords')}    
           """)    

            self.crawl(link)    

    def create_database(self):
        """Create a new database and table for storing information from crawler
        """
        conn = sqlite3.connect('search_engine_DB.db')

        print ("Opened database successfully");

        c = conn.cursor()
        c.execute('''CREATE TABLE WEBPAGE
            (ID INTEGER PRIMARY KEY    AUTOINCREMENT,
             KEYWORD           TEXT   NOT NULL,
             LINK              TEXT   NOT NULL,
             COUNT             INT    NOT NULL);''')
        print ("Table created successfully")
        conn.commit()
        conn.close()
        
    def start(self):
        """Start the crawling process
        """
        self.create_database()
        self.crawl(self.starting_url)    

if __name__ == "__main__":    
    crawler = PyCrawler("https://google.com")     
    crawler.start()
