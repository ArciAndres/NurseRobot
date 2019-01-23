## story_greet
* greet <!--- User input expressed as intent. In this case it represents users message 'Hello'. --> 
 - utter_greet <!--- The response of the chatbot expressed as an action. In this case it represents chatbot's response 'Hello, how can I help?' --> 
 
## story_goodbye
* goodbye
 - utter_standby

## story_thanks
* thanks
 - utter_thanks
 - utter_somethingelse
 

 ## story_joke1
* joke
 - action_joke
* goodbye
 - utter_standby

 ## story_joke2
* joke
 - action_joke
* goodbye
 - utter_standby

 ## story_joke3
* joke
 - action_joke
 
 ## story_joke4
* greet
 - utter_greet
* joke
 - action_joke
* thanks
 - utter_thanks
 - utter_somethingelse
* deny
 - utter_standby 



## story_reach1
* reach
 - utter_reach
 
## story_reach2
* greet 
 - utter_greet
* reach[object=phone]
 - slot{"object":"phone"}
 - utter_reach

 ## story_reach3
* reach[object=cane]
 - slot{"object":"cane"}
 - utter_reach
* goodbye
 - utter_standby

 ## story_reach4
 * reach[object=remote]
 - slot{"object":"remote"}
 - utter_reach

 ## story_reach5
 * reach[object=remote]
 - slot{"object":"remote"}
 - utter_reach


 ## story_move1
 * move[place=bedroom]
 - slot{"place":"bedroom"}
 - utter_move
 - utter_somethingelse
 
## story_move2
* greet
 - utter_greet
* move
 - utter_whereto

## story_move3
* move
 - utter_whereto

## story_move4
* attention
 - utter_attention
* move 
 - utter_whereto
* move[place=bathroom]
 - slot{"place":"bathroom"}
 - utter_move
 - utter_somethingelse
* thanks
 - utter_thanks
 - utter_somethingelse
* deny
 - utter_standby 

## story_affirm1
* affirm
 - utter_attention

## story_affirm2
* attention
 - utter_attention
* move[place=bathroom]
- utter_move
- utter_somethingelse

## story_status1
- utter_askstatus
* status[status:pain]
- slot{"status":"pain"}
- action_status

## story_status2
* attention
- utter_attention
* status[status:pain]
- slot{"status":"pain"}
- action_status
* thanks
- utter_thanks
- utter_somethingelse

## story_status3
* status[status:pain]
- slot{"status":"pain"}
- action_status

## story_misc1
- utter_somethingelse
* deny
- utter_standby 

## story_misc2
- utter_thanks
- utter_somethingelse
* affirm
- utter_attention

 ## story_misc2
* greet
 - utter_greet
* reach{"object": "phone"}
- slot{"object": "phone"}
- utter_reach
* thanks
- utter_thanks
- utter_somethingelse
* deny
- utter_standby 

## story_call1
* call[callto:doctor]
- slot{"callto": "doctor"}
- action_call

## story_call2
* call[callto:daughter]
- slot{"callto": "daughter"}
- action_call

## story_call2
* attention
- utter_attention
* call[callto:ambulance]
- slot{"callto":"ambulance"}
- action_call

## story_call3
* attention
- utter_attention
* call[callto:doctor]
- slot{"callto":"doctor"}
- action_call
- utter_somethingelse

## story_call4
* greet
- utter_greet
* call[callto:son]
- slot{"callto":"son"}
- action_call
- utter_somethingelse
* deny
- utter_standby

## story_call5
* attention
- utter_attention
* call[callto:ambulance]
- slot{"callto":"ambulance"}
- action_call
* thanks
- utter_thanks