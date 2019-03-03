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


logger = logging.getLogger(__name__)

answers = []

class QuoraSearch(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_quora"

    def question_link(self, url):
        page = requests.get(url)
        response = page.text
        soup = bs4.BeautifulSoup(response, 'lxml')
        container = soup.find('a',{'class':'question_link'})
        link = container["href"]
        return link

    def scrappe(self, url):
        answers = []
    	page = requests.get(url)
    	response = page.text
    	soup = bs4.BeautifulSoup(response, 'lxml')
    	container = soup.find('div',{'class':'ui_qtext_expanded'})
    	for p in container:
    		answers.append(p.text)
        print (answers[0])
    	return answers[0]

    def run(self, dispatcher, tracker, domain):
    	query = tracker.latest_message.get('text')
    	search = query.replace(" ", "-")
    	question_url = "https://www.quora.com/"+search
        link = self.question_link(question_url)
        response_url = "https://www.quora.com/"+link
        response = self.scrappe(response_url)
        dispatcher.utter_message("The given information is not available on VIT's website. \nBut here is what I found on Quora:\n")
        dispatcher.utter_message(response)  # send the message back to the user
        return []


