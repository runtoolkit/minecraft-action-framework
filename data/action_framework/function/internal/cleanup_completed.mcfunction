# Cleanup completed actions list

# Keep only last 5 completed actions
data modify storage action_framework:temp completed_backup set from storage action_framework:actions completed
data modify storage action_framework:actions completed set value []

# Would need recursive function to copy last 5
# For now, just clear
