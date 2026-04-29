# Chain Example
# Demonstrates chained actions

tellraw @a ["",\
    {"text":"[Example] ","color":"aqua","bold":true},\
    {"text":"Running chain example...","color":"white"}\
]

# Create a chain of actions
data modify storage action_framework:temp api_input set value {\
    type:"chain",\
    actions:[\
        {type:"message",target:"@a",message:'{"text":"Step 1: Starting...","color":"yellow"}'},\
        {type:"sound",sound:"minecraft:block.note_block.hat",source:"master",target:"@a",volume:"1",pitch:"1"},\
        {type:"message",target:"@a",message:'{"text":"Step 2: Processing...","color":"yellow"}'},\
        {type:"sound",sound:"minecraft:block.note_block.hat",source:"master",target:"@a",volume:"1",pitch:"1.2"},\
        {type:"message",target:"@a",message:'{"text":"Step 3: Complete!","color":"green"}'},\
        {type:"sound",sound:"minecraft:entity.player.levelup",source:"master",target:"@a",volume:"1",pitch:"2"}\
    ]\
}
function action_framework:api/add_action
