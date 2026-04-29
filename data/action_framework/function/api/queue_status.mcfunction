# Show queue status

# Calculate sizes
execute store result score #queue_size af.temp run data get storage action_framework:actions queue
execute store result score #active_size af.temp run data get storage action_framework:actions active
execute store result score #completed_size af.temp run data get storage action_framework:actions completed

tellraw @s ["",\
    {"text":"\n===== ","color":"gold"},\
    {"text":"Queue Status","color":"yellow","bold":true},\
    {"text":" =====\n","color":"gold"}\
]

tellraw @s ["",\
    {"text":"  Queued: ","color":"gray"},\
    {"score":{"name":"#queue_size","objective":"af.temp"},"color":"yellow"}\
]

tellraw @s ["",\
    {"text":"  Active: ","color":"gray"},\
    {"score":{"name":"#active_size","objective":"af.temp"},"color":"green"}\
]

tellraw @s ["",\
    {"text":"  Completed: ","color":"gray"},\
    {"score":{"name":"#completed_size","objective":"af.temp"},"color":"aqua"}\
]

execute if data storage action_framework:main {config:{paused:1b}} run tellraw @s ["",\
    {"text":"  Status: ","color":"gray"},\
    {"text":"PAUSED","color":"red","bold":true}\
]

execute unless data storage action_framework:main {config:{paused:1b}} run tellraw @s ["",\
    {"text":"  Status: ","color":"gray"},\
    {"text":"RUNNING","color":"green","bold":true}\
]

tellraw @s ["",\
    {"text":"\n====================\n","color":"gold"}\
]
