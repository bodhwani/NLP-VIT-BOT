# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import requests
import json
from rasa_core_sdk import Action

logger = logging.getLogger(__name__)


class ActionContact(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_contact"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        print(tracker.current_state())
        dispatcher.utter_message("CONTACT DETAILS")  # send the message back to the user
        return []
