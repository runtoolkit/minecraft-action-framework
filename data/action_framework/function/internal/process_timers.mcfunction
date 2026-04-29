# Process player timers

# Decrement timer
scoreboard players remove @s af.timer 1

# Check if timer reached 0
execute if score @s af.timer matches 0 run function action_framework:internal/timer_complete
