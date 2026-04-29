# Toggle debug mode

# Toggle tag
tag @s[tag=!af.debug] add af.debug
tag @s[tag=af.debug] remove af.debug

# Toggle storage
execute if entity @s[tag=af.debug] run data modify storage action_framework:main config.debug set value 1b
execute if entity @s[tag=!af.debug] run data modify storage action_framework:main config.debug set value 0b

# Feedback
tellraw @s[tag=af.debug] ["",\
    {"text":"[AF] ","color":"gold"},\
    {"text":"Debug mode: ","color":"white"},\
    {"text":"✓ ON","color":"green","bold":true}\
]
tellraw @s[tag=!af.debug] ["",\
    {"text":"[AF] ","color":"gold"},\
    {"text":"Debug mode: ","color":"white"},\
    {"text":"✗ OFF","color":"red","bold":true}\
]

# Play sound
execute at @s run playsound minecraft:block.note_block.hat master @s ~ ~ ~ 0.5 1
