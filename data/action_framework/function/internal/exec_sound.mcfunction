# Execute sound action

# Default values if not specified
execute unless data storage action_framework:temp current_action.source run data modify storage action_framework:temp current_action.source set value "master"
execute unless data storage action_framework:temp current_action.target run data modify storage action_framework:temp current_action.target set value "@a"
execute unless data storage action_framework:temp current_action.volume run data modify storage action_framework:temp current_action.volume set value "1.0"
execute unless data storage action_framework:temp current_action.pitch run data modify storage action_framework:temp current_action.pitch set value "1.0"

# Execute via macro
function action_framework:internal/macro_sound with storage action_framework:temp current_action
