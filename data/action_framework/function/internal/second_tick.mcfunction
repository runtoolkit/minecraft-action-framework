# Runs every second (20 ticks)

# Update player count
execute store result score #players af.system if entity @a

# Cleanup old completed actions (keep last 10)
execute store result score #completed_count af.temp run data get storage action_framework:actions completed
execute if score #completed_count af.temp matches 10.. run function action_framework:internal/cleanup_completed

# Performance metrics
execute if data storage action_framework:main {config:{debug:1b}} run function action_framework:internal/metrics
