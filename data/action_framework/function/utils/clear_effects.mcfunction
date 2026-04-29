# Clear all effects from player

effect clear @s

execute at @s run particle minecraft:cloud ~ ~1 ~ 0.5 0.5 0.5 0.1 20

tellraw @s ["",\
    {"text":"[AF] ","color":"gold"},\
    {"text":"All effects cleared","color":"yellow"}\
]
