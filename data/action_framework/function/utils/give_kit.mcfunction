# Give starter kit to player

give @s minecraft:diamond_sword{Enchantments:[{id:"sharpness",lvl:3}],display:{Name:'{"text":"Starter Sword","color":"aqua","italic":false}'}} 1
give @s minecraft:bow{Enchantments:[{id:"power",lvl:2}]} 1
give @s minecraft:arrow 64
give @s minecraft:cooked_beef 32
give @s minecraft:golden_apple 5

tellraw @s ["",\
    {"text":"[AF] ","color":"gold"},\
    {"text":"Starter kit received!","color":"green"}\
]

execute at @s run playsound minecraft:entity.player.levelup master @s ~ ~ ~ 0.5 1
