# Debug information (runs every tick in debug mode)

# Display action bar info to debug users
title @a[tag=af.debug] actionbar ["",\
    {"text":"AF Debug | ","color":"gold"},\
    {"text":"Q:","color":"gray"},\
    {"score":{"name":"#queue_size","objective":"af.temp"},"color":"yellow"},\
    {"text":" A:","color":"gray"},\
    {"score":{"name":"#active_size","objective":"af.temp"},"color":"yellow"}\
]
