# Heal player to full health

effect give @s instant_health 1 10 true
effect give @s saturation 1 10 true

execute at @s run particle minecraft:heart ~ ~1 ~ 0.5 0.5 0.5 0 10
execute at @s run playsound minecraft:entity.player.levelup master @s ~ ~ ~ 0.3 2

tellraw @s ["",\
    {"text":"[AF] ","color":"gold"},\
    {"text":"Healed to full health","color":"green"}\
]
