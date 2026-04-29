# Timer completed callback

# Execute stored action if any
# This would reference stored action in player data

# Reset timer
scoreboard players reset @s af.timer

# Callback notification
execute if data storage action_framework:main {config:{debug:1b}} run tellraw @s ["",\
    {"text":"[AF] ","color":"gold"},\
    {"text":"Timer completed","color":"green"}\
]
