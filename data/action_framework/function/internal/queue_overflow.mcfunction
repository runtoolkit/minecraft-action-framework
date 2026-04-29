# Queue overflow handler

tellraw @a[tag=af.admin] ["",\
    {"text":"[AF Warning] ","color":"yellow","bold":true},\
    {"text":"Action queue overflow! Clearing old actions...","color":"red"}\
]

# Keep only last 50 items
data modify storage action_framework:temp queue_backup set from storage action_framework:actions queue
data modify storage action_framework:actions queue set value []

# This would need a recursive function to copy last 50 items
# For now, just clear
function action_framework:api/clear_queue

# Log error
scoreboard players add #queue_overflow af.system 1
