#!/usr/bin/python

import json
import xml.sax
import sys
import codecs
from unidecode import unidecode

journals = []

class DBLPHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.title =  ""
        self.article = {'year':'', 'title':'', 'journal':''}
        self.file = codecs.open("journals/dblp_journals.csv", "w", "iso-8859-1")

    def startElement(self, tag, attributes):
        self.CurrentData = tag

    def endElement(self, tag):
        if tag == "title":
            self.article['title'] = self.title
        if tag == "year":
            self.article['year'] = self.year
        if tag == "journal":
            self.article['journal'] = self.journal

        if len(self.article['title']) > 0 and len(self.article['year']) > 0 and len(self.article['journal']) > 0 and (self.article['journal'] in journals):
            data = unidecode(self.article['year'] + ',' + self.article['title'] + ',' + self.article['journal'] + '\n')
            self.file.write(data)
            self.article['title'] = ""
            self.article['year'] = ""
            self.article['journal'] = ""
        elif self.CurrentData == "dblp":
            self.file.close()
            sys.exit("stop")

    def characters(self, content):
        if self.CurrentData == "title":
            self.title = content.strip().replace('"', '').replace("'", "").replace(",", "").rstrip('\n')
        elif self.CurrentData == "year":
            self.year = content.strip().rstrip('\n')
        elif self.CurrentData == "journal":
            self.journal = content.strip().replace('"', '').replace("'", "").replace(",", "").rstrip('\n')

if ( __name__ == "__main__"):
    json_data = open('./src/json/journals.json')
    journals = json.load(json_data)
    json_data.close()
    
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = DBLPHandler()
    parser.setContentHandler(Handler)
    parser.parse("src/dblp/dblp.xml")
