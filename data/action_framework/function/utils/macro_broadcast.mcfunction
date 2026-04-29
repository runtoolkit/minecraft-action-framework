# Macro broadcast

$tellraw @a ["",\
    {"text":"[Broadcast] ","color":"gold","bold":true},\
    {"text":"$(message)","color":"white"}\
]

$execute as @a at @s run playsound minecraft:block.note_block.pling master @s ~ ~ ~ 0.5 2
