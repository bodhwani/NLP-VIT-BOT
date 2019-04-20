## story_greet <!--- The name of the story. It is not mandatory, but useful for debugging. --> 
* greet <!--- User input expressed as intent. In this case it represents users message 'Hello'. --> 
 - utter_name <!--- The response of the chatbot expressed as an action. In this case it represents chatbot's response 'Hello, how can I help?' --> 
 
## story_goodbye
* goodbye
 - utter_goodbye

## story_thanks
* thanks
 - utter_thanks
 
## story_name_correct
* name{"name":"Lucy"}
 - utter_name_check


## story_VIT_international_relations
* international_relations
- utter_IR_response

## story_name_wrong
* name{"name":"Lucy"}
 - utter_name_check
* deny
 - utter_rename