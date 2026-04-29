execute if entity @s[tag=af.debug] run tag @s remove af.debug
execute unless entity @s[tag=af.debug] run tag @s add af.debug

execute if entity @s[tag=af.debug] run data modify storage action_framework:main config.debug set value 1b
execute unless entity @s[tag=af.debug] run data modify storage action_framework:main config.debug set value 0b

tellraw @s[tag=af.debug] [{"text":"[AF] ","color":"gold"},{"text":"Debug: ON","color":"green"}]
tellraw @s[tag=!af.debug] [{"text":"[AF] ","color":"gold"},{"text":"Debug: OFF","color":"red"}]

playsound minecraft:block.note_block.hat master @s ~ ~ ~ 0.5 1
