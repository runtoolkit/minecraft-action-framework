# Process next action in chain

# Check if chain has more actions
execute unless data storage action_framework:temp chain_actions[0] run return 0

# Add first chain action to main queue
data modify storage action_framework:actions queue append from storage action_framework:temp chain_actions[0]

# Remove from chain temp
data remove storage action_framework:temp chain_actions[0]

# Continue with next (recursive)
execute if data storage action_framework:temp chain_actions[0] run function action_framework:internal/chain_next
