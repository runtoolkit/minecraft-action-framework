# Minigame Start Example
# Start a minigame with countdown

# Countdown
title @a times 5 30 5

title @a title {"text":"3","color":"red","bold":true}
execute as @a at @s run playsound minecraft:block.note_block.hat master @s ~ ~ ~ 1 1
# Wait 1 second (would need delay system)

title @a title {"text":"2","color":"yellow","bold":true}
execute as @a at @s run playsound minecraft:block.note_block.hat master @s ~ ~ ~ 1 1.2
# Wait 1 second

title @a title {"text":"1","color":"green","bold":true}
execute as @a at @s run playsound minecraft:block.note_block.hat master @s ~ ~ ~ 1 1.5
# Wait 1 second

title @a title {"text":"GO!","color":"gold","bold":true}
execute as @a at @s run playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 2

# Start effects
effect give @a speed 30 1
effect give @a jump_boost 30 0

tellraw @a ["",\
    {"text":"[Minigame] ","color":"gold","bold":true},\
    {"text":"Game started!","color":"green"}\
]

# Fireworks
execute as @a at @s run particle minecraft:firework ~ ~1 ~ 1 1 1 0.2 50
