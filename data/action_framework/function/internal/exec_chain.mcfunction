# Execute chain action

# Copy chain actions to temp storage
data modify storage action_framework:temp chain_actions set from storage action_framework:temp current_action.actions

# Process chain recursively
function action_framework:internal/chain_next
