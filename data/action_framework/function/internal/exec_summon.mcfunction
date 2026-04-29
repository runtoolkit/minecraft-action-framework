# Execute summon action

execute unless data storage action_framework:temp current_action.nbt run data modify storage action_framework:temp current_action.nbt set value "{}"

function action_framework:internal/macro_summon with storage action_framework:temp current_action
