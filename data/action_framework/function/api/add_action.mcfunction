# Add action to queue
# Usage: data modify storage action_framework:temp api_input set value {type:"command", command:"say Hello"}
#        function action_framework:api/add_action

# Validate input exists
execute unless data storage action_framework:temp api_input run return run tellraw @s [\
    {"text":"[AF Error] ","color":"red","bold":true},\
    {"text":"No input data provided","color":"white"}\
]

# Add to queue
data modify storage action_framework:actions queue append from storage action_framework:temp api_input

# Feedback
tellraw @s[tag=af.debug] ["",\
    {"text":"[AF] ","color":"gold"},\
    {"text":"Action queued","color":"green"}\
]

# Clear input
data remove storage action_framework:temp api_input
