# Process next queued action

# Get first action from queue
data modify storage action_framework:temp current_action set from storage action_framework:actions queue[0]
data remove storage action_framework:actions queue[0]

# Add to active list
data modify storage action_framework:actions active append from storage action_framework:temp current_action

# Route by action type
execute if data storage action_framework:temp current_action{type:"command"} run function action_framework:internal/exec_command
execute if data storage action_framework:temp current_action{type:"sound"} run function action_framework:internal/exec_sound
execute if data storage action_framework:temp current_action{type:"message"} run function action_framework:internal/exec_message
execute if data storage action_framework:temp current_action{type:"summon"} run function action_framework:internal/exec_summon
execute if data storage action_framework:temp current_action{type:"particle"} run function action_framework:internal/exec_particle
execute if data storage action_framework:temp current_action{type:"chain"} run function action_framework:internal/exec_chain
execute if data storage action_framework:temp current_action{type:"delay"} run function action_framework:internal/exec_delay
execute if data storage action_framework:temp current_action{type:"conditional"} run function action_framework:internal/exec_conditional

# Mark as completed
data modify storage action_framework:actions completed append from storage action_framework:temp current_action
data remove storage action_framework:actions active[0]

# Cleanup temp
data remove storage action_framework:temp current_action
