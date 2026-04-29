# Display performance metrics

# Queue size
execute store result score #queue_size af.temp run data get storage action_framework:actions queue

# Active actions
execute store result score #active_size af.temp run data get storage action_framework:actions active

# Display to debug users
tellraw @a[tag=af.debug] ["",\
    {"text":"[AF Metrics] ","color":"yellow"},\
    {"text":"Queue: ","color":"gray"},\
    {"score":{"name":"#queue_size","objective":"af.temp"},"color":"white"},\
    {"text":" | Active: ","color":"gray"},\
    {"score":{"name":"#active_size","objective":"af.temp"},"color":"white"},\
    {"text":" | Players: ","color":"gray"},\
    {"score":{"name":"#players","objective":"af.system"},"color":"white"}\
]
