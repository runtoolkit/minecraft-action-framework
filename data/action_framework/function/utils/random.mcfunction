# Generate random number
# Returns random number in af.temp score

# Use world time and player count for randomness
execute store result score #random af.temp run time query gametime
execute store result score #players af.temp if entity @a
scoreboard players operation #random af.temp += #players af.temp

# Modulo operation if needed (example: random 0-99)
scoreboard players operation #random af.temp %= #100 af.system
