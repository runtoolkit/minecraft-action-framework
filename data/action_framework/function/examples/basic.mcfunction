# Basic Example
# Demonstrates simple action queue usage

tellraw @a ["",\
    {"text":"[Example] ","color":"aqua","bold":true},\
    {"text":"Running basic example...","color":"white"}\
]

# Add a message action
data modify storage action_framework:temp api_input set value {\
    type:"message",\
    target:"@a",\
    message:'{"text":"Hello from Action Framework!","color":"gold"}'\
}
function action_framework:api/add_action

# Add a sound action
data modify storage action_framework:temp api_input set value {\
    type:"sound",\
    sound:"minecraft:entity.player.levelup",\
    source:"master",\
    target:"@a",\
    volume:"1.0",\
    pitch:"1.5"\
}
function action_framework:api/add_action

# Add a command action
data modify storage action_framework:temp api_input set value {\
    type:"command",\
    command:"particle minecraft:heart ~ ~2 ~ 1 1 1 0 50"\
}
function action_framework:api/add_action
