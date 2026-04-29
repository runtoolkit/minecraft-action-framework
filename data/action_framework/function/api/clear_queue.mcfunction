# Clear action queue

data modify storage action_framework:actions queue set value []

tellraw @s ["",\
    {"text":"[AF] ","color":"gold"},\
    {"text":"Action queue cleared","color":"yellow"}\
]
