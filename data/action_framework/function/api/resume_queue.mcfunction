# Resume queue processing

data modify storage action_framework:main config.paused set value 0b

tellraw @s ["",\
    {"text":"[AF] ","color":"gold"},\
    {"text":"Queue processing resumed","color":"green"}\
]
