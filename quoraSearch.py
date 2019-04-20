# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
 
import logging
import requests
import json
from rasa_core_sdk import Action
import time

import bs4
import requests
import pandas as pd
import re
import operator

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)

sid = SentimentIntensityAnalyzer()

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
        page = requests.get(url)
        response = page.text
        soup = bs4.BeautifulSoup(response, 'lxml')
        # print ("soup is",soup)
        container = soup.findAll('div',{'class':'ui_qtext_expanded'})
        for p in container:
            answers.append(p.text)
        # print ("answers are",answers)
        return answers

    def sentimentalAnalysis(self, quora_answer):
        dic = {}
        for sentence in quora_answer:
        #     print "snetence is ",sentence[0:100],snt
            snt = sid.polarity_scores(sentence)
            dic[sentence] = snt['pos']
        # for i,o in dic.iteritems():
        #     print ("\n",i[0:50], o)
        # print"\n\n dic is ===== ", dic
        posAnswer = max(dic.items(), key=operator.itemgetter(1))[0]
        return posAnswer


    def run(self, dispatcher, tracker, domain):
        query = tracker.latest_message.get('text')
    	#query = tracker.latest_message.get('text')
        search = query.replace(" ","+")
        question_url = "https://www.bing.com/search?q="+search+"quora"
        quora_link = self.GoogleSearch(question_url)
        # print ("quora link is", quora_link)

        quora_answer = self.QuoraSearch(quora_link)
        # print ("Length of quora_answer is ",len(quora_answer))

        sentimentalAnswer = self.sentimentalAnalysis(quora_answer)

        if(len(sentimentalAnswer)>250):
            answer_split = sentimentalAnswer.split(".")
            sentimentalAnswer = ".".join(answer_split[:5])
        # print ("quora answers is",quora_answer)
        dispatcher.utter_message("The given information is not available on VIT's website.But here is what I found on Quora:")
        dispatcher.utter_message(str(sentimentalAnswer))  # send the message back to the user
        dispatcher.utter_message("More information can be found at:")
        dispatcher.utter_message(str(quora_link))
        dispatcher
        return []


