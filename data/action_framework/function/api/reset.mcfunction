# Reset framework to default state

tellraw @s ["",\
    {"text":"[AF] ","color":"gold"},\
    {"text":"Resetting framework...","color":"yellow"}\
]

# Clear all data
function action_framework:api/clear_queue
data modify storage action_framework:actions active set value []
data modify storage action_framework:actions completed set value []
data modify storage action_framework:actions failed set value []

# Reset scoreboards
scoreboard players reset * af.action
scoreboard players reset * af.chain
scoreboard players reset * af.timer
scoreboard players reset * af.temp

# Reload
function action_framework:load

tellraw @s ["",\
    {"text":"[AF] ","color":"gold"},\
    {"text":"Framework reset complete","color":"green"}\
]
