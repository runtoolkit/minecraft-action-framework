# Add action via macro
# Usage: function action_framework:api/add_action_macro {type:"command",command:"say test"}

$data modify storage action_framework:actions queue append value {type:"$(type)",command:"$(command)"}

tellraw @s[tag=af.debug] ["",\
    {"text":"[AF] ","color":"gold"},\
    {"text":"Action queued via macro","color":"green"}\
]
