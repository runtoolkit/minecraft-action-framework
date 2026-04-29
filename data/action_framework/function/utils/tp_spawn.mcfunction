# Teleport player to world spawn

execute at @s run tp @s ~ ~ ~ 
execute at @s run spawnpoint @s ~ ~ ~

tellraw @s ["",\
    {"text":"[AF] ","color":"gold"},\
    {"text":"Teleported to spawn","color":"green"}\
]
