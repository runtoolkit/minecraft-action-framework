# Start a countdown
# Sets af.timer score

scoreboard players set @s af.timer 100

tellraw @s ["",\
    {"text":"[AF] ","color":"gold"},\
    {"text":"Countdown started: 5 seconds","color":"yellow"}\
]
