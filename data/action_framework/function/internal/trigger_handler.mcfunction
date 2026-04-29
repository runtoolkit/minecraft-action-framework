# Handle trigger commands

# Route triggers
execute if score @s af.trigger matches 1 run function action_framework:api/debug_toggle
execute if score @s af.trigger matches 2 run function action_framework:api/info
execute if score @s af.trigger matches 99 run function action_framework:api/help

# Reset trigger
scoreboard players reset @s af.trigger
scoreboard players enable @s af.trigger
