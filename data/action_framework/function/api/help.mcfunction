# Display help menu

tellraw @s ["",\
    {"text":"\n===== ","color":"gold","bold":true},\
    {"text":"Action Framework Help","color":"yellow","bold":true},\
    {"text":" =====\n","color":"gold","bold":true}\
]

tellraw @s ["",\
    {"text":"  Commands:","color":"yellow","underlined":true}\
]

tellraw @s ["",\
    {"text":"  • ","color":"gray"},\
    {"text":"/function action_framework:api/info","color":"aqua",\
        "clickEvent":{"action":"suggest_command","value":"/function action_framework:api/info"},\
        "hoverEvent":{"action":"show_text","contents":"Show framework info"}},\
    {"text":"\n    "},\
    {"text":"Show framework information","color":"gray"}\
]

tellraw @s ["",\
    {"text":"  • ","color":"gray"},\
    {"text":"/function action_framework:api/debug_toggle","color":"aqua",\
        "clickEvent":{"action":"suggest_command","value":"/function action_framework:api/debug_toggle"},\
        "hoverEvent":{"action":"show_text","contents":"Toggle debug mode"}},\
    {"text":"\n    "},\
    {"text":"Toggle debug mode","color":"gray"}\
]

tellraw @s ["",\
    {"text":"  • ","color":"gray"},\
    {"text":"/function action_framework:api/clear_queue","color":"aqua",\
        "clickEvent":{"action":"suggest_command","value":"/function action_framework:api/clear_queue"},\
        "hoverEvent":{"action":"show_text","contents":"Clear action queue"}},\
    {"text":"\n    "},\
    {"text":"Clear action queue","color":"gray"}\
]

tellraw @s ["",\
    {"text":"  • ","color":"gray"},\
    {"text":"/function action_framework:examples/basic","color":"aqua",\
        "clickEvent":{"action":"suggest_command","value":"/function action_framework:examples/basic"},\
        "hoverEvent":{"action":"show_text","contents":"Run basic example"}},\
    {"text":"\n    "},\
    {"text":"Run basic example","color":"gray"}\
]

tellraw @s ["",\
    {"text":"\n  For more help, visit: ","color":"gray"},\
    {"text":"github.com/runtoolkit","color":"aqua","underlined":true,\
        "clickEvent":{"action":"open_url","value":"https://github.com/runtoolkit"},\
        "hoverEvent":{"action":"show_text","contents":"Open documentation"}}\
]

tellraw @s ["",\
    {"text":"\n==============================\n","color":"gold"}\
]
