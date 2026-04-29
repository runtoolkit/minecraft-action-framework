# Action Framework Tick Function
# Runs every tick (20 times per second)

# ============================================
# PERFORMANCE CHECK
# ============================================

# Eğer sistem başlatılmamışsa çık
execute unless score #initialized af.system matches 1 run return 0

# ============================================
# QUEUE PROCESSING
# ============================================

# Action queue işle (her tick)
execute if data storage action_framework:actions queue[0] run function action_framework:internal/process_queue

# ============================================
# CHAIN SYSTEM
# ============================================

# Chain sistemini çalıştır
execute if data storage action_framework:actions active[0] run function action_framework:internal/process_chains

# ============================================
# TIMER SYSTEM
# ============================================

# Timer sistemini çalıştır
execute as @a[scores={af.timer=1..}] run function action_framework:internal/process_timers

# ============================================
# EVENT SYSTEM
# ============================================

# Event listener'ları kontrol et
function action_framework:systems/event_tick

# ============================================
# PLAYER ACTIONS
# ============================================

# Oyuncu başına eylemler
execute as @a[scores={af.action=1..}] run function action_framework:internal/player_actions

# Trigger command'lar için
execute as @a[scores={af.trigger=1..}] run function action_framework:internal/trigger_handler

# ============================================
# DEATH TRACKING
# ============================================

execute as @a[scores={af.death=1..}] run function action_framework:events/on_death

# ============================================
# PERIODIC TASKS (every second = 20 ticks)
# ============================================

# Her saniye çalışacak görevler
scoreboard players add #tick af.system 1
execute if score #tick af.system matches 20.. run function action_framework:internal/second_tick
execute if score #tick af.system matches 20.. run scoreboard players set #tick af.system 0

# ============================================
# DEBUG MODE
# ============================================

# Debug modu açıksa bilgi göster
execute if data storage action_framework:main {config:{debug:1b}} run function action_framework:internal/debug_tick
