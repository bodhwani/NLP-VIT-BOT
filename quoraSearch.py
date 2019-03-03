# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
 
import logging
import requests
import json
from rasa_core_sdk import Action

import bs4
import requests
import pandas as pd
import re

logger = logging.getLogger(__name__)

answers = []
headers = {
    
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        
    }
class QuoraSearch(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_quora"

    def GoogleSearch(self, url):
        link = []
        page = requests.get(url, headers=headers)
        response = page.text
        soup = bs4.BeautifulSoup(response, 'lxml')
        # print "soup is",soup
        container = soup.find('li',{'class':'b_algo'})
        # print ("container is",container)
        
        for i in container.findAll('a'):
            link.append(i.get('href'))
        return link[0]

    def QuoraSearch(self, url):
        answers = []
        page = requests.get(url, headers=headers)
        response = page.text
        soup = bs4.BeautifulSoup(response, 'lxml')
        container = soup.find('div',{'class':'ui_qtext_expanded'})
        # print ("container in quora is",container)
        for p in container:
            answers.append(p.text)
        return answers[0]

    def run(self, dispatcher, tracker, domain):
    	query = tracker.latest_message.get('text')

        search = query.replace(" ", "+")
        question_url = "https://www.bing.com/search?q="+search+"quora"
        # print ("question_url=",question_url)

        quora_link = self.GoogleSearch(question_url)
        # print ("quora_link is ",quora_link)

        quora_answer = self.QuoraSearch(quora_link)
        if(len(quora_answer)>250):
            quora_answer_split = quora_answer.split(".")
            quora_answer = ".".join(quora_answer_split[:5])
        # print ("quora answers is",quora_answer)

        dispatcher.utter_message("The given information is not available on VIT's website. \nBut here is what I found on Quora:\n")
        dispatcher.utter_message(quora_answer)  # send the message back to the user
        dispatcher.utter_message("More information can be found at:")
        dispatcher.utter_message(quora_link)
        return []


