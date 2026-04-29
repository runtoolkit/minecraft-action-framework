# Pause queue processing

data modify storage action_framework:main config.paused set value 1b

tellraw @s ["",\
    {"text":"[AF] ","color":"gold"},\
    {"text":"Queue processing paused","color":"yellow"}\
]
