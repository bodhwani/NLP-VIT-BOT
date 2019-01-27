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
* affirm
 - utter_help_start

## story_VIT_international_relations
* international_relations
- utter_IR_response

## story_VIT_admissions_clarify_UG
* admissions
- utter_admissions_response
- utter_admissions_clarification
* admissions_UG
- utter_admissions_UG

## story_VIT_admissions_UG
* admissions_UG
- utter_admissions_UG

## story_VIT_admissions_clarify_PG
* admissions
- utter_admissions_response
- utter_admissions_clarification
* admissions_PG
- utter_admissions_PG

## story_VIT_admissions_PG
* admissions_PG
- utter_admissions_PG

## story_VIT_admissions_clarify_R
* admissions
- utter_admissions_response
- utter_admissions_clarification
* admissions_R
- utter_admissions_R

## story_VIT_admissions_R
* admissions_R
- utter_admissions_R

## story_VIT_admissions_clarify_IR
* admissions
- utter_admissions_response
- utter_admissions_clarification
* international_relations
- utter_admissions_IR

## story_VIT_admissions_bye
* admissions
- utter_admissions_response
- utter_admissions_clarification
* goodbye
- utter_goodbye

## story_VIT_admissions_deny
* admissions
- utter_admissions_response
- utter_admissions_clarification
* deny
- utter_goodbye

## story_name_wrong
* name{"name":"Lucy"}
 - utter_name_check
* deny
 - utter_rename
