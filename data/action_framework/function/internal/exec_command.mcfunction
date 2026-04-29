# Execute command action

# Validate command exists
execute unless data storage action_framework:temp current_action.command run return 0

# Execute via macro
function action_framework:internal/macro_command with storage action_framework:temp current_action

# Log
execute if data storage action_framework:main {config:{debug:1b}} run tellraw @a[tag=af.debug] ["",\
    {"text":"[AF] ","color":"gold"},\
    {"text":"Command executed: ","color":"gray"},\
    {"storage":"action_framework:temp","nbt":"current_action.command","color":"white"}\
]
