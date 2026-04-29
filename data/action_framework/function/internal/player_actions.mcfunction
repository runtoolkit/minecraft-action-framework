# Player-specific actions

# Route to specific action by score value
execute if score @s af.action matches 1 run function action_framework:actions/action_1
execute if score @s af.action matches 2 run function action_framework:actions/action_2
execute if score @s af.action matches 3 run function action_framework:actions/action_3
execute if score @s af.action matches 4 run function action_framework:actions/action_4
execute if score @s af.action matches 5 run function action_framework:actions/action_5

# Reset action score
scoreboard players reset @s af.action
