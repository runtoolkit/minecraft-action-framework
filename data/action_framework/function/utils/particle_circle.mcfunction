# Create particle circle around player

# This would need more complex math for proper circle
# Using simple 8-point circle
execute at @s run particle minecraft:end_rod ~1 ~1 ~ 0 0 0 0 1
execute at @s run particle minecraft:end_rod ~0.7 ~1 ~0.7 0 0 0 0 1
execute at @s run particle minecraft:end_rod ~ ~1 ~1 0 0 0 0 1
execute at @s run particle minecraft:end_rod ~-0.7 ~1 ~0.7 0 0 0 0 1
execute at @s run particle minecraft:end_rod ~-1 ~1 ~ 0 0 0 0 1
execute at @s run particle minecraft:end_rod ~-0.7 ~1 ~-0.7 0 0 0 0 1
execute at @s run particle minecraft:end_rod ~ ~1 ~-1 0 0 0 0 1
execute at @s run particle minecraft:end_rod ~0.7 ~1 ~-0.7 0 0 0 0 1
