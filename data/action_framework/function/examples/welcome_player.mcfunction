# Welcome Player Example
# Full welcome sequence for new players

# Title
title @s times 20 60 20
title @s subtitle {"text":"Welcome to the server!","color":"yellow"}
title @s title {"text":"Action Framework","color":"gold","bold":true}

# Message
tellraw @s ["",\
    {"text":"\n================================\n","color":"dark_gray"},\
    {"text":"  Welcome! ","color":"gold","bold":true},\
    {"text":"\n"},\
    {"text":"  This server uses Action Framework\n","color":"gray"},\
    {"text":"  for enhanced gameplay.\n","color":"gray"},\
    {"text":"\n"},\
    {"text":"  [Get Started]","color":"green","underlined":true,\
        "clickEvent":{"action":"run_command","value":"/function action_framework:api/help"},\
        "hoverEvent":{"action":"show_text","contents":"View help"}},\
    {"text":"\n================================\n","color":"dark_gray"}\
]

# Effects
effect give @s speed 10 0
effect give @s saturation 10 0

# Particles
execute at @s run particle minecraft:totem_of_undying ~ ~1 ~ 0.5 1 0.5 0.1 50

# Sound
execute at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1

# Kit
function action_framework:utils/give_kit
