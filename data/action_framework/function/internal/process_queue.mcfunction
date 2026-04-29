# Process action queue
# Called every tick if queue has items

# Safety check: max queue size
execute store result score #queue_size af.temp run data get storage action_framework:actions queue
execute if score #queue_size af.temp matches 100.. run function action_framework:internal/queue_overflow

# Process next action
execute if data storage action_framework:actions queue[0] run function action_framework:internal/queue_next

# Queue metrics
execute if data storage action_framework:main {config:{log_actions:1b}} run function action_framework:internal/log_queue
