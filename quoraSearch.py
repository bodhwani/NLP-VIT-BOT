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

class QuoraSearch(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_quora"

    def GoogleSearch(self, url):
        page = requests.get(url)
        response = page.text
        soup = bs4.BeautifulSoup(response, 'lxml')
        container = soup.find('h3',{'class':'r'})
    #     start = timeit.timeit()
        for l in container:
            link = l.get('href')
        quora_link = re.findall(r'q=[\'"]?([^\& >]+)', link)
        quora_link = "".join(quora_link)
        text = container.getText()
    #     end = timeit.timeit()
    #     print "time taken=",end - start
        return text,quora_link

    def QuoraSearch(self, url):
        page = requests.get(url)
        response = page.text
        soup = bs4.BeautifulSoup(response, 'lxml')
        container = soup.find('div',{'class':'ui_qtext_expanded'})
        for p in container:
            answers.append(p.text)
        return answers[0]

    def run(self, dispatcher, tracker, domain):
    	query = tracker.latest_message.get('text')

        search = query.replace(" ", "+")
        question_url = "https://google.com/search?q="+search

        text, quora_link = self.GoogleSearch(question_url)
        response_text = self.QuoraSearch(quora_link)

        dispatcher.utter_message("The given information is not available on VIT's website. \nBut here is what I found on Quora:\n")
        dispatcher.utter_message(response_text)  # send the message back to the user
        dispatcher.utter_message("More information can be found at:")
        dispatcher.utter_message(quora_link)
        return []


