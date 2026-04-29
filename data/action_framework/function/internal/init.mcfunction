# Internal initialization
# Run once on load

# Setup default player scores
scoreboard players set @a af.player 0

# Initialize player tracking
execute as @a run function action_framework:systems/player_join

# System ready
data modify storage action_framework:main system_ready set value 1b
scoreboard players set #initialized af.system 1

# Log
execute if data storage action_framework:main {config:{debug:1b}} run say [AF] Internal systems initialized
