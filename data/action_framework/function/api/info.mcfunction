# Display framework info

# Header
tellraw @s ["",\
    {"text":"\n===== ","color":"gold","bold":true},\
    {"text":"Action Framework Info","color":"yellow","bold":true},\
    {"text":" =====\n","color":"gold","bold":true}\
]

# Version
tellraw @s ["",\
    {"text":"  Version: ","color":"gray"},\
    {"storage":"action_framework:main","nbt":"version","color":"yellow"}\
]

# MC Version
tellraw @s ["",\
    {"text":"  Minecraft: ","color":"gray"},\
    {"storage":"action_framework:main","nbt":"mc_version","color":"aqua"}\
]

# Build date
tellraw @s ["",\
    {"text":"  Build Date: ","color":"gray"},\
    {"storage":"action_framework:main","nbt":"build_date","color":"white"}\
]

# Status
execute if score #initialized af.system matches 1 run tellraw @s ["",\
    {"text":"  Status: ","color":"gray"},\
    {"text":"✓ Active","color":"green","bold":true}\
]

# Queue info
execute store result score #queue_size af.temp run data get storage action_framework:actions queue
tellraw @s ["",\
    {"text":"  Queue Size: ","color":"gray"},\
    {"score":{"name":"#queue_size","objective":"af.temp"},"color":"yellow"}\
]

# Active actions
execute store result score #active_size af.temp run data get storage action_framework:actions active
tellraw @s ["",\
    {"text":"  Active Actions: ","color":"gray"},\
    {"score":{"name":"#active_size","objective":"af.temp"},"color":"yellow"}\
]

# Links
tellraw @s ["",\
    {"text":"\n  "},\
    {"text":"[Documentation]","color":"aqua","underlined":true,\
        "clickEvent":{"action":"open_url","value":"https://github.com/runtoolkit"},\
        "hoverEvent":{"action":"show_text","contents":"View documentation"}},\
    {"text":" "},\
    {"text":"[GitHub]","color":"white","underlined":true,\
        "clickEvent":{"action":"open_url","value":"https://github.com/runtoolkit"},\
        "hoverEvent":{"action":"show_text","contents":"View on GitHub"}}\
]

# Footer
tellraw @s ["",\
    {"text":"\n==============================\n","color":"gold"}\
]
