# Execute message action

execute unless data storage action_framework:temp current_action.target run data modify storage action_framework:temp current_action.target set value "@a"

function action_framework:internal/macro_message with storage action_framework:temp current_action
