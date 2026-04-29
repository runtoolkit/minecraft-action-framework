# Boss Introduction Example
# Dramatic boss spawn sequence

# Warning message
tellraw @a ["",\
    {"text":"\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n","color":"dark_red","bold":true},\
    {"text":"  ⚠ WARNING ⚠  \n","color":"red","bold":true},\
    {"text":"  A boss is approaching!\n","color":"yellow"},\
    {"text":"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n","color":"dark_red","bold":true}\
]

# Sounds
execute as @a at @s run playsound minecraft:entity.wither.spawn hostile @s ~ ~ ~ 1 0.5
execute as @a at @s run playsound minecraft:entity.ender_dragon.growl hostile @s ~ ~ ~ 1 0.8

# Effects
execute as @a run effect give @s darkness 5 0
execute as @a run effect give @s blindness 3 0

# Particles at spawn location
particle minecraft:large_smoke 0 70 0 5 5 5 0.1 200
particle minecraft:soul_fire_flame 0 70 0 5 5 5 0.1 100
particle minecraft:dragon_breath 0 70 0 5 5 5 0.2 150

# Title
title @a times 20 80 20
title @a subtitle {"text":"Prepare for battle!","color":"red"}
title @a title {"text":"⚔ BOSS FIGHT ⚔","color":"dark_red","bold":true}

# Summon boss (example)
# summon minecraft:wither 0 70 0 {CustomName:'{"text":"The Destroyer","color":"dark_red","bold":true}',Health:500f,Attributes:[{Name:"generic.max_health",Base:500}]}
