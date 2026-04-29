# Particle Show Example
# Create a visual particle display

tellraw @a ["",\
    {"text":"[Example] ","color":"aqua","bold":true},\
    {"text":"Particle show starting...","color":"white"}\
]

# Multiple particle effects
execute as @a at @s run particle minecraft:firework ~ ~2 ~ 1 1 1 0.1 50
execute as @a at @s run particle minecraft:end_rod ~ ~1 ~ 0.5 0.5 0.5 0.1 30
execute as @a at @s run particle minecraft:dragon_breath ~ ~0.5 ~ 0.3 0.3 0.3 0.05 20

execute as @a at @s run playsound minecraft:entity.firework_rocket.large_blast master @s ~ ~ ~ 1 1

tellraw @a ["",\
    {"text":"[Example] ","color":"aqua"},\
    {"text":"Particle show complete!","color":"green"}\
]
