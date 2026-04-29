"""
Minecraft Action Framework Builder
Author: asn44nb (https://github.com/asn44nb)
Organization: RunToolkit (https://github.com/runtoolkit)
License: MIT
Version: 2.0.0
"""

import os
import sys
import json
import shutil
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Proje kök dizini
ROOT_DIR = Path(__file__).parent
SRC_DIR = ROOT_DIR / "src"
CONFIG_DIR = ROOT_DIR / "config"
TEMPLATES_DIR = ROOT_DIR / "templates"
OUTPUT_DIR = ROOT_DIR / "output"
DOCS_DIR = ROOT_DIR / "docs"

# Src modüllerini import et
sys.path.insert(0, str(SRC_DIR))

from builder import DatapackBuilder
from action_handler import ActionHandler
from macro_processor import MacroProcessor
from storage_manager import StorageManager
from validator import SyntaxValidator
from cli import CLI
from utils import Logger, FileUtils, ColorOutput

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('build.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class FrameworkBuilder:
    """Ana framework builder sınıfı - Geliştirilmiş"""
    
    def __init__(self, config_path: Path = None, verbose: bool = False):
        self.version = "2.0.0"
        self.mc_version = "1.21.4"
        self.pack_format = 48  # MC 1.21.4
        self.output_dir = OUTPUT_DIR
        self.datapack_name = "ActionFramework"
        self.verbose = verbose
        self.color = ColorOutput()
        self.stats = {
            'functions_created': 0,
            'actions_created': 0,
            'macros_created': 0,
            'errors': 0,
            'warnings': 0
        }
        
        # Config yolu
        self.config_path = config_path or CONFIG_DIR / "settings.json"
        
        # Validator başlat
        self.validator = SyntaxValidator(self.mc_version)
        
        logger.info(f"Framework Builder v{self.version} başlatıldı")
        
    def build(self):
        """Ana build işlemi"""
        try:
            start_time = datetime.now()
            
            print(self.color.header("=" * 60))
            print(self.color.header("🎮 Minecraft Action Framework Builder v" + self.version))
            print(self.color.header("=" * 60))
            print()
            
            # Build adımları
            self.setup_directories()
            self.load_config()
            self.generate_pack_mcmeta()
            self.generate_load_function()
            self.generate_tick_function()
            self.generate_internal_functions()
            self.generate_action_functions()
            self.generate_macro_functions()
            self.generate_api_functions()
            self.generate_utility_functions()
            self.generate_example_functions()
            self.create_documentation()
            self.create_readme()
            self.create_changelog()
            self.validate_output()
            self.create_archive()
            
            # Süre hesapla
            duration = (datetime.now() - start_time).total_seconds()
            
            # İstatistikleri göster
            self.print_statistics(duration)
            
            logger.info("Build başarıyla tamamlandı!")
            return True
            
        except Exception as e:
            logger.error(f"Build hatası: {e}", exc_info=True)
            print(self.color.error(f"\n❌ Build başarısız: {e}"))
            return False
    
    def setup_directories(self):
        """Çıktı dizinlerini hazırla"""
        print(self.color.info("🔧 Dizinler hazırlanıyor..."))
        
        # Eski output'u temizle
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        
        # Ana dizinler
        base_data = self.output_dir / self.datapack_name / "data"
        framework_ns = base_data / "action_framework"
        minecraft_ns = base_data / "minecraft"
        
        # Yeni dizin yapısını oluştur
        dirs = [
            # Framework namespace
            framework_ns / "function",
            framework_ns / "function" / "internal",
            framework_ns / "function" / "actions",
            framework_ns / "function" / "macros",
            framework_ns / "function" / "api",
            framework_ns / "function" / "utils",
            framework_ns / "function" / "examples",
            framework_ns / "function" / "events",
            framework_ns / "function" / "systems",
            
            # Tags
            minecraft_ns / "tags" / "function",
            framework_ns / "tags" / "function",
            
            # Predicates
            framework_ns / "predicate",
            
            # Item modifiers
            framework_ns / "item_modifier",
            
            # Loot tables
            framework_ns / "loot_table",
            
            # Advancements
            framework_ns / "advancement",
            
            # Docs
            DOCS_DIR,
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            
        print(self.color.success("✅ Dizinler oluşturuldu"))
        logger.info(f"{len(dirs)} dizin oluşturuldu")
        
    def load_config(self):
        """Konfigürasyon dosyalarını yükle"""
        print(self.color.info("📝 Konfigürasyon yükleniyor..."))
        
        config_file = CONFIG_DIR / "settings.json"
        actions_file = CONFIG_DIR / "actions.json"
        macros_file = CONFIG_DIR / "macros.json"
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.settings = json.load(f)
                
            with open(actions_file, 'r', encoding='utf-8') as f:
                self.actions = json.load(f)
                
            with open(macros_file, 'r', encoding='utf-8') as f:
                self.macros = json.load(f)
                
            # Settings'den değerleri al
            if 'datapack' in self.settings:
                self.datapack_name = self.settings['datapack'].get('name', self.datapack_name)
                self.pack_format = self.settings['datapack'].get('pack_format', self.pack_format)
                
            action_count = len(self.actions.get('actions', []))
            macro_count = len(self.macros.get('macros', []))
            
            print(self.color.success(f"✅ {action_count} eylem, {macro_count} makro yüklendi"))
            logger.info(f"Config yüklendi: {action_count} actions, {macro_count} macros")
            
        except FileNotFoundError as e:
            logger.error(f"Config dosyası bulunamadı: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse hatası: {e}")
            raise
        
    def generate_pack_mcmeta(self):
        """pack.mcmeta dosyasını oluştur"""
        print(self.color.info("📦 pack.mcmeta oluşturuluyor..."))
        
        pack_data = {
            "pack": {
                "pack_format": self.pack_format,
                "description": {
                    "text": "Advanced Action Framework",
                    "color": "gold",
                    "bold": True,
                    "extra": [
                        {"text": "\n"},
                        {"text": f"v{self.version} ", "color": "yellow", "bold": False},
                        {"text": "by RunToolkit", "color": "gray", "bold": False},
                        {"text": "\n"},
                        {"text": "MC " + self.mc_version, "color": "dark_gray", "bold": False, "italic": True}
                    ]
                },
                "supported_formats": {
                    "min_inclusive": 48,
                    "max_inclusive": 48
                }
            },
            "meta": {
                "version": self.version,
                "authors": ["asn44nb", "RunToolkit"],
                "homepage": "https://github.com/runtoolkit",
                "source": "https://github.com/runtoolkit/minecraft-action-framework"
            }
        }
        
        output_file = self.output_dir / self.datapack_name / "pack.mcmeta"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(pack_data, f, indent=2, ensure_ascii=False)
            
        # Pack icon ekle (varsa)
        icon_path = TEMPLATES_DIR / "pack.png"
        if icon_path.exists():
            shutil.copy(icon_path, self.output_dir / self.datapack_name / "pack.png")
            
        print(self.color.success("✅ pack.mcmeta oluşturuldu"))
        self.stats['functions_created'] += 1
        
    def generate_load_function(self):
        """Load fonksiyonunu oluştur - Geliştirilmiş"""
        print(self.color.info("🚀 Load fonksiyonu oluşturuluyor..."))
        
        content = """# Action Framework Load Function
# Generated by RunToolkit Framework Builder v{self.version}
# https://github.com/runtoolkit
# Build Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# ============================================
# SCOREBOARD INITIALIZATION
# ============================================

scoreboard objectives add af.system dummy "AF System"
scoreboard objectives add af.action dummy "AF Action"
scoreboard objectives add af.chain dummy "AF Chain"
scoreboard objectives add af.timer dummy "AF Timer"
scoreboard objectives add af.player dummy "AF Player"
scoreboard objectives add af.temp dummy "AF Temp"
scoreboard objectives add af.config dummy "AF Config"
scoreboard objectives add af.trigger trigger "AF Trigger"
scoreboard objectives add af.event dummy "AF Event"

# Health tracking (optional)
scoreboard objectives add af.health health {{"text":"❤","color":"red"}}
scoreboard objectives add af.death deathCount "Deaths"

# ============================================
# STORAGE INITIALIZATION
# ============================================

# Main storage
data merge storage action_framework:main {{\\
    initialized:1b,\\
    version:"{self.version}",\\
    mc_version:"{self.mc_version}",\\
    build_date:"{datetime.now().isoformat()}",\\
    config:{{\\
        debug:0b,\\
        log_actions:1b,\\
        max_queue_size:100,\\
        tick_rate:20\\
    }}\\
}}

# Action storage
data merge storage action_framework:actions {{\\
    queue:[],\\
    active:[],\\
    completed:[],\\
    failed:[]\\
}}

# Macro storage
data merge storage action_framework:macros {{\\
    templates:{{}},\\
    cache:{{}}\\
}}

# Temporary storage
data merge storage action_framework:temp {{\\
    data:{{}},\\
    current_action:{{}},\\
    chain_actions:[]\\
}}

# Event storage
data merge storage action_framework:events {{\\
    listeners:{{}},\\
    queue:[]\\
}}

# Player data storage
data merge storage action_framework:players {{\\
    data:{{}},\\
    online:[]\\
}}

# ============================================
# SYSTEM CONSTANTS
# ============================================

scoreboard players set #-1 af.system -1
scoreboard players set #0 af.system 0
scoreboard players set #1 af.system 1
scoreboard players set #2 af.system 2
scoreboard players set #5 af.system 5
scoreboard players set #10 af.system 10
scoreboard players set #20 af.system 20
scoreboard players set #50 af.system 50
scoreboard players set #100 af.system 100
scoreboard players set #1000 af.system 1000

# Version number
scoreboard players set #major af.system 2
scoreboard players set #minor af.system 0
scoreboard players set #patch af.system 0

# ============================================
# TEAM SETUP (for visual effects)
# ============================================

team add af.admin "AF Admin"
team modify af.admin color gold
team modify af.admin prefix {{"text":"[AF] ","color":"gold","bold":true}}

team add af.debug "AF Debug"
team modify af.debug color yellow
team modify af.debug prefix {{"text":"[DEBUG] ","color":"yellow"}}

# ============================================
# GAMERULES (optional, configurable)
# ============================================

# Uncomment if needed:
# gamerule commandBlockOutput false
# gamerule sendCommandFeedback false
# gamerule logAdminCommands false

# ============================================
# LOAD MESSAGE
# ============================================

tellraw @a ["",\\
    {{"text":"\\n================================\\n","color":"dark_gray"}},\\
    {{"text":"  Action Framework  ","color":"gold","bold":true}},\\
    {{"text":"\\n"}},\\
    {{"text":"  Version: ","color":"gray"}},\\
    {{"text":"{self.version}","color":"yellow"}},\\
    {{"text":"\\n"}},\\
    {{"text":"  Minecraft: ","color":"gray"}},\\
    {{"text":"{self.mc_version}","color":"aqua"}},\\
    {{"text":"\\n"}},\\
    {{"text":"  Status: ","color":"gray"}},\\
    {{"text":"✓ Loaded","color":"green","bold":true}},\\
    {{"text":"\\n"}},\\
    {{"text":"  [Docs]","color":"aqua","underlined":true,\\
        "clickEvent":{{"action":"open_url","value":"https://github.com/runtoolkit"}},\\
        "hoverEvent":{{"action":"show_text","contents":"Dokümantasyonu aç"}}}},\\
    {{"text":" | "}},\\
    {{"text":"[GitHub]","color":"white","underlined":true,\\
        "clickEvent":{{"action":"open_url","value":"https://github.com/runtoolkit"}},\\
        "hoverEvent":{{"action":"show_text","contents":"GitHub'da görüntüle"}}}},\\
    {{"text":"\\n================================\\n","color":"dark_gray"}}\\
]

# Play load sound
execute as @a at @s run playsound minecraft:block.note_block.pling master @s ~ ~ ~ 0.5 2

# ============================================
# INITIALIZE SUBSYSTEMS
# ============================================

function action_framework:internal/init
function action_framework:systems/event_init
function action_framework:systems/player_init

# ============================================
# SETUP COMPLETE
# ============================================

scoreboard players set #initialized af.system 1
data modify storage action_framework:main system_ready set value 1b

# Debug log
execute if data storage action_framework:main {{config:{{debug:1b}}}} run tellraw @a[tag=af.debug] [\\
    {{"text":"[AF Debug] ","color":"yellow"}},\\
    {{"text":"Framework initialized successfully","color":"green"}}\\
]
"""
        content = content.replace("{{", "{").replace("}}", "}")
        content = content.replace("{self.version}", self.version).replace("{self.mc_version}", self.mc_version)
        content = content.replace("{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        output_file.write_text(content, encoding='utf-8')
        
        # Load tag'ini oluştur
        load_tag = {
            "values": [
                "action_framework:load"
            ]
        }
        
        tag_file = self.output_dir / self.datapack_name / "data" / "minecraft" / "tags" / "function" / "load.json"
        with open(tag_file, 'w', encoding='utf-8') as f:
            json.dump(load_tag, f, indent=2)
            
        print(self.color.success("✅ Load fonksiyonu oluşturuldu"))
        self.stats['functions_created'] += 1
        
    def generate_tick_function(self):
        """Tick fonksiyonunu oluştur - Geliştirilmiş"""
        print(self.color.info("⏱️  Tick fonksiyonu oluşturuluyor..."))
        
        content = """# Action Framework Tick Function
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
"""
        
        output_file = self.output_dir / self.datapack_name / "data" / "action_framework" / "function" / "tick.mcfunction"
        output_file.write_text(content, encoding='utf-8')
        
        # Tick tag'ini oluştur
        tick_tag = {
            "values": [
                "action_framework:tick"
            ]
        }
        
        tag_file = self.output_dir / self.datapack_name / "data" / "minecraft" / "tags" / "function" / "tick.json"
        with open(tag_file, 'w', encoding='utf-8') as f:
            json.dump(tick_tag, f, indent=2)
            
        print(self.color.success("✅ Tick fonksiyonu oluşturuldu"))
        self.stats['functions_created'] += 1
        
    def generate_internal_functions(self):
        """İç sistem fonksiyonlarını oluştur - Geliştirilmiş"""
        print(self.color.info("⚙️  İç fonksiyonlar oluşturuluyor..."))
        
        internal_dir = self.output_dir / self.datapack_name / "data" / "action_framework" / "function" / "internal"
        
        functions = {
            "init.mcfunction": """# Internal initialization
# Run once on load

# Setup default player scores
scoreboard players set @a af.player 0

# Initialize player tracking
execute as @a run function action_framework:systems/player_join

# System ready
data modify storage action_framework:main system_ready set value 1b
scoreboard players set #initialized af.system 1

# Log
execute if data storage action_framework:main {config:{debug:1b}} run say [AF] Internal systems initialized
""",

            "process_queue.mcfunction": """# Process action queue
# Called every tick if queue has items

# Safety check: max queue size
execute store result score #queue_size af.temp run data get storage action_framework:actions queue
execute if score #queue_size af.temp matches 100.. run function action_framework:internal/queue_overflow

# Process next action
execute if data storage action_framework:actions queue[0] run function action_framework:internal/queue_next

# Queue metrics
execute if data storage action_framework:main {config:{log_actions:1b}} run function action_framework:internal/log_queue
""",

            "queue_next.mcfunction": """# Process next queued action

# Get first action from queue
data modify storage action_framework:temp current_action set from storage action_framework:actions queue[0]
data remove storage action_framework:actions queue[0]

# Add to active list
data modify storage action_framework:actions active append from storage action_framework:temp current_action

# Route by action type
execute if data storage action_framework:temp current_action{type:"command"} run function action_framework:internal/exec_command
execute if data storage action_framework:temp current_action{type:"sound"} run function action_framework:internal/exec_sound
execute if data storage action_framework:temp current_action{type:"message"} run function action_framework:internal/exec_message
execute if data storage action_framework:temp current_action{type:"summon"} run function action_framework:internal/exec_summon
execute if data storage action_framework:temp current_action{type:"particle"} run function action_framework:internal/exec_particle
execute if data storage action_framework:temp current_action{type:"chain"} run function action_framework:internal/exec_chain
execute if data storage action_framework:temp current_action{type:"delay"} run function action_framework:internal/exec_delay
execute if data storage action_framework:temp current_action{type:"conditional"} run function action_framework:internal/exec_conditional

# Mark as completed
data modify storage action_framework:actions completed append from storage action_framework:temp current_action
data remove storage action_framework:actions active[0]

# Cleanup temp
data remove storage action_framework:temp current_action
""",

            "queue_overflow.mcfunction": """# Queue overflow handler

tellraw @a[tag=af.admin] ["",\\
    {"text":"[AF Warning] ","color":"yellow","bold":true},\\
    {"text":"Action queue overflow! Clearing old actions...","color":"red"}\\
]

# Keep only last 50 items
data modify storage action_framework:temp queue_backup set from storage action_framework:actions queue
data modify storage action_framework:actions queue set value []

# This would need a recursive function to copy last 50 items
# For now, just clear
function action_framework:api/clear_queue

# Log error
scoreboard players add #queue_overflow af.system 1
""",

            "exec_command.mcfunction": """# Execute command action

# Validate command exists
execute unless data storage action_framework:temp current_action.command run return 0

# Execute via macro
function action_framework:internal/macro_command with storage action_framework:temp current_action

# Log
execute if data storage action_framework:main {config:{debug:1b}} run tellraw @a[tag=af.debug] ["",\\
    {"text":"[AF] ","color":"gold"},\\
    {"text":"Command executed: ","color":"gray"},\\
    {"storage":"action_framework:temp","nbt":"current_action.command","color":"white"}\\
]
""",

            "macro_command.mcfunction": """# Macro command executor
# Uses macros for dynamic command execution

$$(command)
""",

            "exec_sound.mcfunction": """# Execute sound action

# Default values if not specified
execute unless data storage action_framework:temp current_action.source run data modify storage action_framework:temp current_action.source set value "master"
execute unless data storage action_framework:temp current_action.target run data modify storage action_framework:temp current_action.target set value "@a"
execute unless data storage action_framework:temp current_action.volume run data modify storage action_framework:temp current_action.volume set value "1.0"
execute unless data storage action_framework:temp current_action.pitch run data modify storage action_framework:temp current_action.pitch set value "1.0"

# Execute via macro
function action_framework:internal/macro_sound with storage action_framework:temp current_action
""",

            "macro_sound.mcfunction": """# Macro sound player

$execute as $(target) at @s run playsound $(sound) $(source) @s ~ ~ ~ $(volume) $(pitch)
""",

            "exec_message.mcfunction": """# Execute message action

execute unless data storage action_framework:temp current_action.target run data modify storage action_framework:temp current_action.target set value "@a"

function action_framework:internal/macro_message with storage action_framework:temp current_action
""",

            "macro_message.mcfunction": """# Macro message sender

$tellraw $(target) $(message)
""",

            "exec_summon.mcfunction": """# Execute summon action

execute unless data storage action_framework:temp current_action.nbt run data modify storage action_framework:temp current_action.nbt set value "{}"

function action_framework:internal/macro_summon with storage action_framework:temp current_action
""",

            "macro_summon.mcfunction": """# Macro entity summoner

$summon $(entity) $(x) $(y) $(z) $(nbt)
""",

            "exec_particle.mcfunction": """# Execute particle action

function action_framework:internal/macro_particle with storage action_framework:temp current_action
""",

            "macro_particle.mcfunction": """# Macro particle spawner

$particle $(particle) $(x) $(y) $(z) $(dx) $(dy) $(dz) $(speed) $(count)
""",

            "exec_chain.mcfunction": """# Execute chain action

# Copy chain actions to temp storage
data modify storage action_framework:temp chain_actions set from storage action_framework:temp current_action.actions

# Process chain recursively
function action_framework:internal/chain_next
""",

            "chain_next.mcfunction": """# Process next action in chain

# Check if chain has more actions
execute unless data storage action_framework:temp chain_actions[0] run return 0

# Add first chain action to main queue
data modify storage action_framework:actions queue append from storage action_framework:temp chain_actions[0]

# Remove from chain temp
data remove storage action_framework:temp chain_actions[0]

# Continue with next (recursive)
execute if data storage action_framework:temp chain_actions[0] run function action_framework:internal/chain_next
""",

            "exec_delay.mcfunction": """# Execute delayed action

# Set timer on executing entity or use system timer
execute if data storage action_framework:temp current_action.timer store result score @s af.timer run data get storage action_framework:temp current_action.timer

# Store the action to execute after delay
# This would need more complex storage management
""",

            "exec_conditional.mcfunction": """# Execute conditional action

# Check condition via predicate or score
# If true, execute then_action
# If false, execute else_action

# This is a placeholder for conditional logic
# Would need predicate system integration
""",

            "process_chains.mcfunction": """# Process active chains

# Check each active chain for completion
# Move completed chains to completed list

# Placeholder for future chain state management
""",

            "process_timers.mcfunction": """# Process player timers

# Decrement timer
scoreboard players remove @s af.timer 1

# Check if timer reached 0
execute if score @s af.timer matches 0 run function action_framework:internal/timer_complete
""",

            "timer_complete.mcfunction": """# Timer completed callback

# Execute stored action if any
# This would reference stored action in player data

# Reset timer
scoreboard players reset @s af.timer

# Callback notification
execute if data storage action_framework:main {config:{debug:1b}} run tellraw @s ["",\\
    {"text":"[AF] ","color":"gold"},\\
    {"text":"Timer completed","color":"green"}\\
]
""",

            "player_actions.mcfunction": """# Player-specific actions

# Route to specific action by score value
execute if score @s af.action matches 1 run function action_framework:actions/action_1
execute if score @s af.action matches 2 run function action_framework:actions/action_2
execute if score @s af.action matches 3 run function action_framework:actions/action_3
execute if score @s af.action matches 4 run function action_framework:actions/action_4
execute if score @s af.action matches 5 run function action_framework:actions/action_5

# Reset action score
scoreboard players reset @s af.action
""",

            "trigger_handler.mcfunction": """# Handle trigger commands

# Route triggers
execute if score @s af.trigger matches 1 run function action_framework:api/debug_toggle
execute if score @s af.trigger matches 2 run function action_framework:api/info
execute if score @s af.trigger matches 99 run function action_framework:api/help

# Reset trigger
scoreboard players reset @s af.trigger
scoreboard players enable @s af.trigger
""",

            "second_tick.mcfunction": """# Runs every second (20 ticks)

# Update player count
execute store result score #players af.system if entity @a

# Cleanup old completed actions (keep last 10)
execute store result score #completed_count af.temp run data get storage action_framework:actions completed
execute if score #completed_count af.temp matches 10.. run function action_framework:internal/cleanup_completed

# Performance metrics
execute if data storage action_framework:main {config:{debug:1b}} run function action_framework:internal/metrics
""",

            "cleanup_completed.mcfunction": """# Cleanup completed actions list

# Keep only last 5 completed actions
data modify storage action_framework:temp completed_backup set from storage action_framework:actions completed
data modify storage action_framework:actions completed set value []

# Would need recursive function to copy last 5
# For now, just clear
""",

            "metrics.mcfunction": """# Display performance metrics

# Queue size
execute store result score #queue_size af.temp run data get storage action_framework:actions queue

# Active actions
execute store result score #active_size af.temp run data get storage action_framework:actions active

# Display to debug users
tellraw @a[tag=af.debug] ["",\\
    {"text":"[AF Metrics] ","color":"yellow"},\\
    {"text":"Queue: ","color":"gray"},\\
    {"score":{"name":"#queue_size","objective":"af.temp"},"color":"white"},\\
    {"text":" | Active: ","color":"gray"},\\
    {"score":{"name":"#active_size","objective":"af.temp"},"color":"white"},\\
    {"text":" | Players: ","color":"gray"},\\
    {"score":{"name":"#players","objective":"af.system"},"color":"white"}\\
]
""",

            "debug_tick.mcfunction": """# Debug information (runs every tick in debug mode)

# Display action bar info to debug users
title @a[tag=af.debug] actionbar ["",\\
    {"text":"AF Debug | ","color":"gold"},\\
    {"text":"Q:","color":"gray"},\\
    {"score":{"name":"#queue_size","objective":"af.temp"},"color":"yellow"},\\
    {"text":" A:","color":"gray"},\\
    {"score":{"name":"#active_size","objective":"af.temp"},"color":"yellow"}\\
]
""",

            "log_queue.mcfunction": """# Log queue processing

tellraw @a[tag=af.admin] ["",\\
    {"text":"[AF Log] ","color":"aqua"},\\
    {"text":"Processing action queue...","color":"white"}\\
]
"""
        }
        
        # Tüm internal fonksiyonları oluştur
        for filename, content in functions.items():
            (internal_dir / filename).write_text(content, encoding='utf-8')
            self.stats['functions_created'] += 1
            
        print(self.color.success(f"✅ {len(functions)} iç fonksiyon oluşturuldu"))
        
    def generate_action_functions(self):
        """Eylem fonksiyonlarını oluştur"""
        print(self.color.info("🎯 Eylem fonksiyonları oluşturuluyor..."))
        
        actions_dir = self.output_dir / self.datapack_name / "data" / "action_framework" / "function" / "actions"
        
        action_handler = ActionHandler(self.validator)
        
        created_count = 0
        error_count = 0
        
        for action in self.actions.get('actions', []):
            try:
                action_id = action.get('id')
                action_content = action_handler.generate_action(action)
                
                # Syntax kontrolü
                is_valid, errors = self.validator.validate_function(action_content)
                if not is_valid:
                    print(self.color.warning(f"⚠️  Uyarı: Action {action_id} syntax hatası:"))
                    for error in errors:
                        print(self.color.warning(f"    - {error}"))
                    self.stats['warnings'] += 1
                    
                output_file = actions_dir / f"action_{action_id}.mcfunction"
                output_file.write_text(action_content, encoding='utf-8')
                created_count += 1
                self.stats['actions_created'] += 1
                
            except Exception as e:
                logger.error(f"Action {action.get('id')} oluşturulamadı: {e}")
                error_count += 1
                self.stats['errors'] += 1
                
        print(self.color.success(f"✅ {created_count} eylem fonksiyonu oluşturuldu"))
        if error_count > 0:
            print(self.color.warning(f"⚠️  {error_count} eylem başarısız"))

    def generate_macro_functions(self):
        """Makro fonksiyonlarını oluştur"""
        print(self.color.info("🔄 Makro fonksiyonları oluşturuluyor..."))
        
        macros_dir = self.output_dir / self.datapack_name / "data" / "action_framework" / "function" / "macros"
        
        macro_processor = MacroProcessor()
        created_count = 0
        
        for macro in self.macros.get('macros', []):
            try:
                macro_content = macro_processor.generate_macro(macro)
                output_file = macros_dir / f"{macro['name']}.mcfunction"
                output_file.write_text(macro_content, encoding='utf-8')
                created_count += 1
                self.stats['macros_created'] += 1
                
            except Exception as e:
                logger.error(f"Macro {macro.get('name')} oluşturulamadı: {e}")
                self.stats['errors'] += 1
                
        print(self.color.success(f"✅ {created_count} makro fonksiyonu oluşturuldu"))
        
    def generate_api_functions(self):
        """API fonksiyonlarını oluştur - Geliştirilmiş"""
        print(self.color.info("🔌 API fonksiyonları oluşturuluyor..."))
        
        api_dir = self.output_dir / self.datapack_name / "data" / "action_framework" / "function" / "api"
        
        api_functions = {
            "add_action.mcfunction": """# Add action to queue
# Usage: data modify storage action_framework:temp api_input set value {type:"command", command:"say Hello"}
#        function action_framework:api/add_action

# Validate input exists
execute unless data storage action_framework:temp api_input run return run tellraw @s [\\
    {"text":"[AF Error] ","color":"red","bold":true},\\
    {"text":"No input data provided","color":"white"}\\
]

# Add to queue
data modify storage action_framework:actions queue append from storage action_framework:temp api_input

# Feedback
tellraw @s[tag=af.debug] ["",\\
    {"text":"[AF] ","color":"gold"},\\
    {"text":"Action queued","color":"green"}\\
]

# Clear input
data remove storage action_framework:temp api_input
""",

            "add_action_macro.mcfunction": """# Add action via macro
# Usage: function action_framework:api/add_action_macro {type:"command",command:"say test"}

$data modify storage action_framework:actions queue append value {type:"$(type)",command:"$(command)"}

tellraw @s[tag=af.debug] ["",\\
    {"text":"[AF] ","color":"gold"},\\
    {"text":"Action queued via macro","color":"green"}\\
]
""",

            "clear_queue.mcfunction": """# Clear action queue

data modify storage action_framework:actions queue set value []

tellraw @s ["",\\
    {"text":"[AF] ","color":"gold"},\\
    {"text":"Action queue cleared","color":"yellow"}\\
]
""",

            "pause_queue.mcfunction": """# Pause queue processing

data modify storage action_framework:main config.paused set value 1b

tellraw @s ["",\\
    {"text":"[AF] ","color":"gold"},\\
    {"text":"Queue processing paused","color":"yellow"}\\
]
""",

            "resume_queue.mcfunction": """# Resume queue processing

data modify storage action_framework:main config.paused set value 0b

tellraw @s ["",\\
    {"text":"[AF] ","color":"gold"},\\
    {"text":"Queue processing resumed","color":"green"}\\
]
""",

            "debug_toggle.mcfunction": """# Toggle debug mode

# Toggle tag
tag @s[tag=!af.debug] add af.debug
tag @s[tag=af.debug] remove af.debug

# Toggle storage
execute if entity @s[tag=af.debug] run data modify storage action_framework:main config.debug set value 1b
execute if entity @s[tag=!af.debug] run data modify storage action_framework:main config.debug set value 0b

# Feedback
tellraw @s[tag=af.debug] ["",\\
    {"text":"[AF] ","color":"gold"},\\
    {"text":"Debug mode: ","color":"white"},\\
    {"text":"✓ ON","color":"green","bold":true}\\
]
tellraw @s[tag=!af.debug] ["",\\
    {"text":"[AF] ","color":"gold"},\\
    {"text":"Debug mode: ","color":"white"},\\
    {"text":"✗ OFF","color":"red","bold":true}\\
]

# Play sound
execute at @s run playsound minecraft:block.note_block.hat master @s ~ ~ ~ 0.5 1
""",

            "info.mcfunction": """# Display framework info

# Header
tellraw @s ["",\\
    {"text":"\\n===== ","color":"gold","bold":true},\\
    {"text":"Action Framework Info","color":"yellow","bold":true},\\
    {"text":" =====\\n","color":"gold","bold":true}\\
]

# Version
tellraw @s ["",\\
    {"text":"  Version: ","color":"gray"},\\
    {"storage":"action_framework:main","nbt":"version","color":"yellow"}\\
]

# MC Version
tellraw @s ["",\\
    {"text":"  Minecraft: ","color":"gray"},\\
    {"storage":"action_framework:main","nbt":"mc_version","color":"aqua"}\\
]

# Build date
tellraw @s ["",\\
    {"text":"  Build Date: ","color":"gray"},\\
    {"storage":"action_framework:main","nbt":"build_date","color":"white"}\\
]

# Status
execute if score #initialized af.system matches 1 run tellraw @s ["",\\
    {"text":"  Status: ","color":"gray"},\\
    {"text":"✓ Active","color":"green","bold":true}\\
]

# Queue info
execute store result score #queue_size af.temp run data get storage action_framework:actions queue
tellraw @s ["",\\
    {"text":"  Queue Size: ","color":"gray"},\\
    {"score":{"name":"#queue_size","objective":"af.temp"},"color":"yellow"}\\
]

# Active actions
execute store result score #active_size af.temp run data get storage action_framework:actions active
tellraw @s ["",\\
    {"text":"  Active Actions: ","color":"gray"},\\
    {"score":{"name":"#active_size","objective":"af.temp"},"color":"yellow"}\\
]

# Links
tellraw @s ["",\\
    {"text":"\\n  "},\\
    {"text":"[Documentation]","color":"aqua","underlined":true,\\
        "clickEvent":{"action":"open_url","value":"https://github.com/runtoolkit"},\\
        "hoverEvent":{"action":"show_text","contents":"View documentation"}},\\
    {"text":" "},\\
    {"text":"[GitHub]","color":"white","underlined":true,\\
        "clickEvent":{"action":"open_url","value":"https://github.com/runtoolkit"},\\
        "hoverEvent":{"action":"show_text","contents":"View on GitHub"}}\\
]

# Footer
tellraw @s ["",\\
    {"text":"\\n==============================\\n","color":"gold"}\\
]
""",

            "help.mcfunction": """# Display help menu

tellraw @s ["",\\
    {"text":"\\n===== ","color":"gold","bold":true},\\
    {"text":"Action Framework Help","color":"yellow","bold":true},\\
    {"text":" =====\\n","color":"gold","bold":true}\\
]

tellraw @s ["",\\
    {"text":"  Commands:","color":"yellow","underlined":true}\\
]

tellraw @s ["",\\
    {"text":"  • ","color":"gray"},\\
    {"text":"/function action_framework:api/info","color":"aqua",\\
        "clickEvent":{"action":"suggest_command","value":"/function action_framework:api/info"},\\
        "hoverEvent":{"action":"show_text","contents":"Show framework info"}},\\
    {"text":"\\n    "},\\
    {"text":"Show framework information","color":"gray"}\\
]

tellraw @s ["",\\
    {"text":"  • ","color":"gray"},\\
    {"text":"/function action_framework:api/debug_toggle","color":"aqua",\\
        "clickEvent":{"action":"suggest_command","value":"/function action_framework:api/debug_toggle"},\\
        "hoverEvent":{"action":"show_text","contents":"Toggle debug mode"}},\\
    {"text":"\\n    "},\\
    {"text":"Toggle debug mode","color":"gray"}\\
]

tellraw @s ["",\\
    {"text":"  • ","color":"gray"},\\
    {"text":"/function action_framework:api/clear_queue","color":"aqua",\\
        "clickEvent":{"action":"suggest_command","value":"/function action_framework:api/clear_queue"},\\
        "hoverEvent":{"action":"show_text","contents":"Clear action queue"}},\\
    {"text":"\\n    "},\\
    {"text":"Clear action queue","color":"gray"}\\
]

tellraw @s ["",\\
    {"text":"  • ","color":"gray"},\\
    {"text":"/function action_framework:examples/basic","color":"aqua",\\
        "clickEvent":{"action":"suggest_command","value":"/function action_framework:examples/basic"},\\
        "hoverEvent":{"action":"show_text","contents":"Run basic example"}},\\
    {"text":"\\n    "},\\
    {"text":"Run basic example","color":"gray"}\\
]

tellraw @s ["",\\
    {"text":"\\n  For more help, visit: ","color":"gray"},\\
    {"text":"github.com/runtoolkit","color":"aqua","underlined":true,\\
        "clickEvent":{"action":"open_url","value":"https://github.com/runtoolkit"},\\
        "hoverEvent":{"action":"show_text","contents":"Open documentation"}}\\
]

tellraw @s ["",\\
    {"text":"\\n==============================\\n","color":"gold"}\\
]
""",

            "reload.mcfunction": """# Reload framework

tellraw @s ["",\\
    {"text":"[AF] ","color":"gold"},\\
    {"text":"Reloading framework...","color":"yellow"}\\
]

# Reload datapacks
reload

tellraw @s ["",\\
    {"text":"[AF] ","color":"gold"},\\
    {"text":"Framework reloaded","color":"green"}\\
]
""",

            "reset.mcfunction": """# Reset framework to default state

tellraw @s ["",\\
    {"text":"[AF] ","color":"gold"},\\
    {"text":"Resetting framework...","color":"yellow"}\\
]

# Clear all data
function action_framework:api/clear_queue
data modify storage action_framework:actions active set value []
data modify storage action_framework:actions completed set value []
data modify storage action_framework:actions failed set value []

# Reset scoreboards
scoreboard players reset * af.action
scoreboard players reset * af.chain
scoreboard players reset * af.timer
scoreboard players reset * af.temp

# Reload
function action_framework:load

tellraw @s ["",\\
    {"text":"[AF] ","color":"gold"},\\
    {"text":"Framework reset complete","color":"green"}\\
]
""",

            "queue_status.mcfunction": """# Show queue status

# Calculate sizes
execute store result score #queue_size af.temp run data get storage action_framework:actions queue
execute store result score #active_size af.temp run data get storage action_framework:actions active
execute store result score #completed_size af.temp run data get storage action_framework:actions completed

tellraw @s ["",\\
    {"text":"\\n===== ","color":"gold"},\\
    {"text":"Queue Status","color":"yellow","bold":true},\\
    {"text":" =====\\n","color":"gold"}\\
]

tellraw @s ["",\\
    {"text":"  Queued: ","color":"gray"},\\
    {"score":{"name":"#queue_size","objective":"af.temp"},"color":"yellow"}\\
]

tellraw @s ["",\\
    {"text":"  Active: ","color":"gray"},\\
    {"score":{"name":"#active_size","objective":"af.temp"},"color":"green"}\\
]

tellraw @s ["",\\
    {"text":"  Completed: ","color":"gray"},\\
    {"score":{"name":"#completed_size","objective":"af.temp"},"color":"aqua"}\\
]

execute if data storage action_framework:main {config:{paused:1b}} run tellraw @s ["",\\
    {"text":"  Status: ","color":"gray"},\\
    {"text":"PAUSED","color":"red","bold":true}\\
]

execute unless data storage action_framework:main {config:{paused:1b}} run tellraw @s ["",\\
    {"text":"  Status: ","color":"gray"},\\
    {"text":"RUNNING","color":"green","bold":true}\\
]

tellraw @s ["",\\
    {"text":"\\n====================\\n","color":"gold"}\\
]
"""
        }
        
        # API fonksiyonlarını oluştur
        for filename, content in api_functions.items():
            (api_dir / filename).write_text(content, encoding='utf-8')
            self.stats['functions_created'] += 1
            
        print(self.color.success(f"✅ {len(api_functions)} API fonksiyonu oluşturuldu"))

    def generate_utility_functions(self):
        """Yardımcı fonksiyonları oluştur"""
        print(self.color.info("🛠️  Yardımcı fonksiyonlar oluşturuluyor..."))
        
        utils_dir = self.output_dir / self.datapack_name / "data" / "action_framework" / "function" / "utils"
        
        utils = {
            "random.mcfunction": """# Generate random number
# Returns random number in af.temp score

# Use world time and player count for randomness
execute store result score #random af.temp run time query gametime
execute store result score #players af.temp if entity @a
scoreboard players operation #random af.temp += #players af.temp

# Modulo operation if needed (example: random 0-99)
scoreboard players operation #random af.temp %= #100 af.system
""",

            "broadcast.mcfunction": """# Broadcast message to all players
# Input: storage action_framework:temp message

function action_framework:utils/macro_broadcast with storage action_framework:temp
""",

            "macro_broadcast.mcfunction": """# Macro broadcast

$tellraw @a ["",\\
    {"text":"[Broadcast] ","color":"gold","bold":true},\\
    {"text":"$(message)","color":"white"}\\
]

$execute as @a at @s run playsound minecraft:block.note_block.pling master @s ~ ~ ~ 0.5 2
""",

            "tp_spawn.mcfunction": """# Teleport player to world spawn

execute at @s run tp @s ~ ~ ~ 
execute at @s run spawnpoint @s ~ ~ ~

tellraw @s ["",\\
    {"text":"[AF] ","color":"gold"},\\
    {"text":"Teleported to spawn","color":"green"}\\
]
""",

            "heal.mcfunction": """# Heal player to full health

effect give @s instant_health 1 10 true
effect give @s saturation 1 10 true

execute at @s run particle minecraft:heart ~ ~1 ~ 0.5 0.5 0.5 0 10
execute at @s run playsound minecraft:entity.player.levelup master @s ~ ~ ~ 0.3 2

tellraw @s ["",\\
    {"text":"[AF] ","color":"gold"},\\
    {"text":"Healed to full health","color":"green"}\\
]
""",

            "clear_effects.mcfunction": """# Clear all effects from player

effect clear @s

execute at @s run particle minecraft:cloud ~ ~1 ~ 0.5 0.5 0.5 0.1 20

tellraw @s ["",\\
    {"text":"[AF] ","color":"gold"},\\
    {"text":"All effects cleared","color":"yellow"}\\
]
""",

            "countdown.mcfunction": """# Start a countdown
# Sets af.timer score

scoreboard players set @s af.timer 100

tellraw @s ["",\\
    {"text":"[AF] ","color":"gold"},\\
    {"text":"Countdown started: 5 seconds","color":"yellow"}\\
]
""",

            "particle_circle.mcfunction": """# Create particle circle around player

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
""",

            "give_kit.mcfunction": """# Give starter kit to player

give @s minecraft:diamond_sword{Enchantments:[{id:"sharpness",lvl:3}],display:{Name:'{"text":"Starter Sword","color":"aqua","italic":false}'}} 1
give @s minecraft:bow{Enchantments:[{id:"power",lvl:2}]} 1
give @s minecraft:arrow 64
give @s minecraft:cooked_beef 32
give @s minecraft:golden_apple 5

tellraw @s ["",\\
    {"text":"[AF] ","color":"gold"},\\
    {"text":"Starter kit received!","color":"green"}\\
]

execute at @s run playsound minecraft:entity.player.levelup master @s ~ ~ ~ 0.5 1
"""
        }
        
        for filename, content in utils.items():
            (utils_dir / filename).write_text(content, encoding='utf-8')
            self.stats['functions_created'] += 1
            
        print(self.color.success(f"✅ {len(utils)} yardımcı fonksiyon oluşturuldu"))

    def generate_example_functions(self):
        """Örnek kullanım fonksiyonları oluştur"""
        print(self.color.info("📚 Örnek fonksiyonlar oluşturuluyor..."))
        
        examples_dir = self.output_dir / self.datapack_name / "data" / "action_framework" / "function" / "examples"
        
        examples = {
            "basic.mcfunction": """# Basic Example
# Demonstrates simple action queue usage

tellraw @a ["",\\
    {"text":"[Example] ","color":"aqua","bold":true},\\
    {"text":"Running basic example...","color":"white"}\\
]

# Add a message action
data modify storage action_framework:temp api_input set value {\\
    type:"message",\\
    target:"@a",\\
    message:'{"text":"Hello from Action Framework!","color":"gold"}'\\
}
function action_framework:api/add_action

# Add a sound action
data modify storage action_framework:temp api_input set value {\\
    type:"sound",\\
    sound:"minecraft:entity.player.levelup",\\
    source:"master",\\
    target:"@a",\\
    volume:"1.0",\\
    pitch:"1.5"\\
}
function action_framework:api/add_action

# Add a command action
data modify storage action_framework:temp api_input set value {\\
    type:"command",\\
    command:"particle minecraft:heart ~ ~2 ~ 1 1 1 0 50"\\
}
function action_framework:api/add_action
""",

            "chain_example.mcfunction": """# Chain Example
# Demonstrates chained actions

tellraw @a ["",\\
    {"text":"[Example] ","color":"aqua","bold":true},\\
    {"text":"Running chain example...","color":"white"}\\
]

# Create a chain of actions
data modify storage action_framework:temp api_input set value {\\
    type:"chain",\\
    actions:[\\
        {type:"message",target:"@a",message:'{"text":"Step 1: Starting...","color":"yellow"}'},\\
        {type:"sound",sound:"minecraft:block.note_block.hat",source:"master",target:"@a",volume:"1",pitch:"1"},\\
        {type:"message",target:"@a",message:'{"text":"Step 2: Processing...","color":"yellow"}'},\\
        {type:"sound",sound:"minecraft:block.note_block.hat",source:"master",target:"@a",volume:"1",pitch:"1.2"},\\
        {type:"message",target:"@a",message:'{"text":"Step 3: Complete!","color":"green"}'},\\
        {type:"sound",sound:"minecraft:entity.player.levelup",source:"master",target:"@a",volume:"1",pitch:"2"}\\
    ]\\
}
function action_framework:api/add_action
""",

            "particle_show.mcfunction": """# Particle Show Example
# Create a visual particle display

tellraw @a ["",\\
    {"text":"[Example] ","color":"aqua","bold":true},\\
    {"text":"Particle show starting...","color":"white"}\\
]

# Multiple particle effects
execute as @a at @s run particle minecraft:firework ~ ~2 ~ 1 1 1 0.1 50
execute as @a at @s run particle minecraft:end_rod ~ ~1 ~ 0.5 0.5 0.5 0.1 30
execute as @a at @s run particle minecraft:dragon_breath ~ ~0.5 ~ 0.3 0.3 0.3 0.05 20

execute as @a at @s run playsound minecraft:entity.firework_rocket.large_blast master @s ~ ~ ~ 1 1

tellraw @a ["",\\
    {"text":"[Example] ","color":"aqua"},\\
    {"text":"Particle show complete!","color":"green"}\\
]
""",

            "welcome_player.mcfunction": """# Welcome Player Example
# Full welcome sequence for new players

# Title
title @s times 20 60 20
title @s subtitle {"text":"Welcome to the server!","color":"yellow"}
title @s title {"text":"Action Framework","color":"gold","bold":true}

# Message
tellraw @s ["",\\
    {"text":"\\n================================\\n","color":"dark_gray"},\\
    {"text":"  Welcome! ","color":"gold","bold":true},\\
    {"text":"\\n"},\\
    {"text":"  This server uses Action Framework\\n","color":"gray"},\\
    {"text":"  for enhanced gameplay.\\n","color":"gray"},\\
    {"text":"\\n"},\\
    {"text":"  [Get Started]","color":"green","underlined":true,\\
        "clickEvent":{"action":"run_command","value":"/function action_framework:api/help"},\\
        "hoverEvent":{"action":"show_text","contents":"View help"}},\\
    {"text":"\\n================================\\n","color":"dark_gray"}\\
]

# Effects
effect give @s speed 10 0
effect give @s saturation 10 0

# Particles
execute at @s run particle minecraft:totem_of_undying ~ ~1 ~ 0.5 1 0.5 0.1 50

# Sound
execute at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1

# Kit
function action_framework:utils/give_kit
""",

            "boss_intro.mcfunction": """# Boss Introduction Example
# Dramatic boss spawn sequence

# Warning message
tellraw @a ["",\\
    {"text":"\\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\\n","color":"dark_red","bold":true},\\
    {"text":"  ⚠ WARNING ⚠  \\n","color":"red","bold":true},\\
    {"text":"  A boss is approaching!\\n","color":"yellow"},\\
    {"text":"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\\n","color":"dark_red","bold":true}\\
]

# Sounds
execute as @a at @s run playsound minecraft:entity.wither.spawn hostile @s ~ ~ ~ 1 0.5
execute as @a at @s run playsound minecraft:entity.ender_dragon.growl hostile @s ~ ~ ~ 1 0.8

# Effects
execute as @a run effect give @s darkness 5 0
execute as @a run effect give @s blindness 3 0

# Particles at spawn location
particle minecraft:large_smoke 0 70 0 5 5 5 0.1 200
particle minecraft:soul_fire_flame 0 70 0 5 5 5 0.1 100
particle minecraft:dragon_breath 0 70 0 5 5 5 0.2 150

# Title
title @a times 20 80 20
title @a subtitle {"text":"Prepare for battle!","color":"red"}
title @a title {"text":"⚔ BOSS FIGHT ⚔","color":"dark_red","bold":true}

# Summon boss (example)
# summon minecraft:wither 0 70 0 {CustomName:'{"text":"The Destroyer","color":"dark_red","bold":true}',Health:500f,Attributes:[{Name:"generic.max_health",Base:500}]}
""",

            "minigame_start.mcfunction": """# Minigame Start Example
# Start a minigame with countdown

# Countdown
title @a times 5 30 5

title @a title {"text":"3","color":"red","bold":true}
execute as @a at @s run playsound minecraft:block.note_block.hat master @s ~ ~ ~ 1 1
# Wait 1 second (would need delay system)

title @a title {"text":"2","color":"yellow","bold":true}
execute as @a at @s run playsound minecraft:block.note_block.hat master @s ~ ~ ~ 1 1.2
# Wait 1 second

title @a title {"text":"1","color":"green","bold":true}
execute as @a at @s run playsound minecraft:block.note_block.hat master @s ~ ~ ~ 1 1.5
# Wait 1 second

title @a title {"text":"GO!","color":"gold","bold":true}
execute as @a at @s run playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 2

# Start effects
effect give @a speed 30 1
effect give @a jump_boost 30 0

tellraw @a ["",\\
    {"text":"[Minigame] ","color":"gold","bold":true},\\
    {"text":"Game started!","color":"green"}\\
]

# Fireworks
execute as @a at @s run particle minecraft:firework ~ ~1 ~ 1 1 1 0.2 50
"""
        }
        
        for filename, content in examples.items():
            (examples_dir / filename).write_text(content, encoding='utf-8')
            self.stats['functions_created'] += 1
            
        print(self.color.success(f"✅ {len(examples)} örnek fonksiyon oluşturuldu"))

    def create_documentation(self):
        """Dokümantasyon oluştur - Tamamlanmış"""
        print(self.color.info("📚 Dokümantasyon oluşturuluyor..."))
        
        docs_dir = self.output_dir / "docs"
        docs_dir.mkdir(exist_ok=True)
        
        usage_guide = """# Action Framework Kullanım Kılavuzu

## 🚀 Başlangıç

Framework otomatik olarak yüklenir. `/reload` komutu ile yeniden yükleyebilirsiniz.

## 📋 Temel Komutlar

### Bilgi Görüntüleme
```mcfunction
function action_framework:api/info
```
Framework hakkında bilgi gösterir.

### Debug Modu
```mcfunction
function action_framework:api/debug_toggle
```
Debug modunu açar/kapatır. Debug modunda ek bilgiler görüntülenir.

### Yardım Menüsü
```mcfunction
function action_framework:api/help
```
Komutların listesini gösterir.

### Kuyruk Durumu
```mcfunction
function action_framework:api/queue_status
```
Action kuyruğunun durumunu gösterir.

## 🎯 Action Sistemi

### Action Ekleme

#### Yöntem 1: Storage ile
```mcfunction
data modify storage action_framework:temp api_input set value {{\\
    type:"message",\\
    target:"@a",\\
    message:'{{"text":"Hello!","color":"gold"}}'\\
}}
function action_framework:api/add_action
```

#### Yöntem 2: Macro ile
```mcfunction
function action_framework:api/add_action_macro {{\\
    type:"command",\\
    command:"say Hello World"\\
}}
```

### Action Türleri

#### 1. Command Action
```mcfunction
{{
    type:"command",
    command:"say Hello World"
}}
```

#### 2. Message Action
```mcfunction
{{
    type:"message",
    target:"@a",
    message:'{{"text":"Welcome!","color":"gold"}}'
}}
```

#### 3. Sound Action
```mcfunction
{{
    type:"sound",
    sound:"minecraft:entity.player.levelup",
    source:"master",
    target:"@a",
    volume:"1.0",
    pitch:"1.5"
}}
```

#### 4. Particle Action
```mcfunction
{{
    type:"particle",
    particle:"minecraft:heart",
    x:"~ ",
    y:"~2",
    z:"~ ",
    dx:"0.5",
    dy:"0.5",
    dz:"0.5",
    speed:"0",
    count:"10"
}}
```

#### 5. Summon Action
```mcfunction
{{
    type:"summon",
    entity:"minecraft:zombie",
    x:"~ ",
    y:"~ ",
    z:"~ ",
    nbt:'{{"CustomName":"{\\"text\\":\\"Test Zombie\\"}"}}'
}}
```

#### 6. Chain Action
```mcfunction
{{
    type:"chain",
    actions:[
        {{type:"message",target:"@a",message:'{{"text":"Step 1"}}'}},
        {{type:"sound",sound:"minecraft:block.note_block.hat",source:"master",target:"@a"}},
        {{type:"message",target:"@a",message:'{{"text":"Step 2"}}'}}
    ]
}}
```

## 🔄 Macro Sistemi

Macrolar parametreli fonksiyon çağrılarını kolaylaştırır.

### Kullanılabilir Macrolar

#### damage_player
```mcfunction
function action_framework:macros/damage_player {{amount:"5.0"}}
```

#### give_item
```mcfunction
function action_framework:macros/give_item {{\\
    target:"@s",\\
    item:"minecraft:diamond",\\
    count:"5"\\
}}
```

#### tp_coords
```mcfunction
function action_framework:macros/tp_coords {{\\
    target:"@s",\\
    x:"0",\\
    y:"64",\\
    z:"0"\\
}}
```

#### effect_apply
```mcfunction
function action_framework:macros/effect_apply {{\\
    target:"@s",\\
    effect:"minecraft:speed",\\
    duration:"30",\\
    amplifier:"1"\\
}}
```

## 🛠️ Yardımcı Fonksiyonlar

### Random Sayı
```mcfunction
function action_framework:utils/random
# Sonuç: #random af.temp scoreboard'ında
```

### Oyuncu İyileştirme
```mcfunction
execute as @a run function action_framework:utils/heal
```

### Efekt Temizleme
```mcfunction
execute as @a run function action_framework:utils/clear_effects
```

### Parçacık Çemberi
```mcfunction
execute as @a at @s run function action_framework:utils/particle_circle
```

### Başlangıç Kiti
```mcfunction
execute as @a run function action_framework:utils/give_kit
```

## 📖 Örnekler

### Basit Örnek
```mcfunction
function action_framework:examples/basic
```

### Chain Örneği
```mcfunction
function action_framework:examples/chain_example
```

### Parçacık Gösterisi
```mcfunction
function action_framework:examples/particle_show
```

### Oyuncu Karşılama
```mcfunction
execute as @a run function action_framework:examples/welcome_player
```

### Boss Tanıtımı
```mcfunction
function action_framework:examples/boss_intro
```

### Minigame Başlangıcı
```mcfunction
function action_framework:examples/minigame_start
```

## ⚙️ Konfigürasyon

Framework ayarları `action_framework:main` storage'ında tutulur:

```mcfunction
data modify storage action_framework:main config set value {{\\
    debug:0b,
    log_actions:1b,
    max_queue_size:100,
    tick_rate:20,
    paused:0b\\
}}
```

### Debug Modu Açma
```mcfunction
data modify storage action_framework:main config.debug set value 1b
```

### Action Logging Kapatma
```mcfunction
data modify storage action_framework:main config.log_actions set value 0b
```

### Kuyruğu Duraklama
```mcfunction
function action_framework:api/pause_queue
```

### Kuyruğu Devam Ettirme
```mcfunction
function action_framework:api/resume_queue
```

## 🔧 İleri Seviye

### Custom Action Handler

Kendi action type'ınızı oluşturmak için:

1. `data/action_framework/function/internal/` içinde handler oluşturun
2. `queue_next.mcfunction` içine routing ekleyin
3. Macro kullanarak dinamik parametreler ekleyin

### Event Sistemi

Event listener'lar oluşturabilirsiniz:

```mcfunction
# data/action_framework/function/events/on_death.mcfunction
scoreboard players reset @s af.death

# Custom death handling
tellraw @s {{"text":"You died!","color":"red"}}
# Add respawn action
```

### Storage Yapısı

#### Main Storage
```
action_framework:main
├── initialized: 1b
├── version: "2.0.0"
├── mc_version: "1.21.4"
├── build_date: "2024-01-15T..."
├── config
│   ├── debug: 0b
│   ├── log_actions: 1b
│   ├── max_queue_size: 100
│   └── paused: 0b
└── system_ready: 1b
```

#### Actions Storage
```
action_framework:actions
├── queue: []        # Bekleyen actionlar
├── active: []       # Çalışan actionlar
├── completed: []    # Tamamlananlar
└── failed: []       # Başarısızlar
```

## 🐛 Hata Ayıklama

### Debug Modu Kullanımı
1. Debug modunu açın: `/function action_framework:api/debug_toggle`
2. `af.debug` tag'i size eklenecek
3. Action bar'da queue bilgileri görünür
4. Chat'te detaylı loglar görünür

### Yaygın Sorunlar

#### Action çalışmıyor
- Debug modu açık mı kontrol edin
- Queue'nun dolu olmadığından emin olun
- Storage syntax'ını kontrol edin

#### Performance sorunları
- Queue size'ı azaltın
- Log_actions'ı kapatın
- Chain action sayısını sınırlayın

## 📚 Kaynaklar

- GitHub: https://github.com/runtoolkit
- Documentation: https://github.com/runtoolkit/minecraft-action-framework
- Issues: https://github.com/runtoolkit/minecraft-action-framework/issues

## 📄 Lisans

MIT License - https://opensource.org/licenses/MIT

## 👥 Katkıda Bulunanlar

- asn44nb (https://github.com/asn44nb)
- RunToolkit Team

## 🔄 Versiyon: {self.version}
## 🎮 Minecraft: {self.mc_version}

---
*Bu dokümantasyon Framework Builder v{self.version} tarafından otomatik oluşturulmuştur.*
"""
        usage_guide = usage_guide.replace("{{", "{").replace("}}", "}")
        usage_guide = usage_guide.replace("{self.version}", self.version).replace("{self.mc_version}", self.mc_version)
        (docs_dir / "USAGE.md").write_text(usage_guide, encoding='utf-8')
        
        # API Referansı
        api_reference = """# API Referansı

## Fonksiyon Listesi

### API Fonksiyonları
- `action_framework:api/add_action` - Action ekle
- `action_framework:api/add_action_macro` - Macro ile action ekle
- `action_framework:api/clear_queue` - Kuyruğu temizle
- `action_framework:api/pause_queue` - Kuyruğu duraklat
- `action_framework:api/resume_queue` - Kuyruğu devam ettir
- `action_framework:api/debug_toggle` - Debug modu
- `action_framework:api/info` - Bilgi göster
- `action_framework:api/help` - Yardım menüsü
- `action_framework:api/queue_status` - Kuyruk durumu
- `action_framework:api/reload` - Framework'ü yeniden yükle
- `action_framework:api/reset` - Framework'ü sıfırla

### Yardımcı Fonksiyonlar
- `action_framework:utils/random` - Random sayı üret
- `action_framework:utils/broadcast` - Mesaj yayını
- `action_framework:utils/tp_spawn` - Spawn'a ışınla
- `action_framework:utils/heal` - İyileştir
- `action_framework:utils/clear_effects` - Efektleri temizle
- `action_framework:utils/countdown` - Geri sayım başlat
- `action_framework:utils/particle_circle` - Parçacık çemberi
- `action_framework:utils/give_kit` - Başlangıç kiti ver

### Örnek Fonksiyonlar
- `action_framework:examples/basic` - Basit örnek
- `action_framework:examples/chain_example` - Chain örneği
- `action_framework:examples/particle_show` - Parçacık gösterisi
- `action_framework:examples/welcome_player` - Oyuncu karşılama
- `action_framework:examples/boss_intro` - Boss tanıtımı
- `action_framework:examples/minigame_start` - Minigame başlangıcı

## Scoreboard Objectives

- `af.system` - Sistem değişkenleri
- `af.action` - Action ID'leri
- `af.chain` - Chain durumu
- `af.timer` - Timer değerleri
- `af.player` - Oyuncu verileri
- `af.temp` - Geçici değerler
- `af.config` - Konfigürasyon
- `af.trigger` - Trigger komutları
- `af.event` - Event flagleri
- `af.health` - Sağlık göstergesi
- `af.death` - Ölüm sayacı

## Storage Namespaces

### action_framework:main
Ana sistem konfigürasyonu ve durum bilgisi

### action_framework:actions
Action queue ve işlem durumları

### action_framework:macros
Macro template'leri ve cache

### action_framework:temp
Geçici veri depolama

### action_framework:events
Event listener'lar ve queue

### action_framework:players
Oyuncu spesifik veriler

## Tags

### Teams
- `af.admin` - Admin yetkilileri
- `af.debug` - Debug kullanıcıları

## Sistem Sabitleri

Scoreboard `af.system` üzerinde:
- `#-1` = -1
- `#0` = 0
- `#1` = 1
- `#2` = 2
- `#5` = 5
- `#10` = 10
- `#20` = 20
- `#50` = 50
- `#100` = 100
- `#1000` = 1000

## Data Formatları

### Action Object
```json
{
    "type": "command|message|sound|particle|summon|chain|delay|conditional",
    // Type-specific fields
}
```

### Chain Action
```json
{
    "type": "chain",
    "actions": [
        {...},
        {...}
    ]
}
```

## Return Codes

Fonksiyonlar genellikle şu return code'ları kullanır:
- `0` - Başarısız/Hata
- `1` - Başarılı

## Events

Framework şu event'leri trigger eder:
- `on_death` - Oyuncu öldüğünde
- `on_join` - Oyuncu katıldığında (player_init)
- `timer_complete` - Timer tamamlandığında

---
*v{self.version}*
"""
        
        (docs_dir / "API.md").write_text(api_reference, encoding='utf-8')
        
        print(self.color.success("✅ Dokümantasyon oluşturuldu"))

    def create_readme(self):
        """README.md oluştur"""
        print(self.color.info("📄 README oluşturuluyor..."))
        
        readme = """# 🎮 Minecraft Action Framework

![Version](https://img.shields.io/badge/version-{self.version}-blue)
![Minecraft](https://img.shields.io/badge/minecraft-{self.mc_version}-green)
![License](https://img.shields.io/badge/license-MIT-orange)

Advanced action management system for Minecraft {self.mc_version} datapacks.

## ✨ Özellikler

- 🎯 **Action Queue System** - Eylemlerinizi sıraya koyun ve otomatik işleyin
- 🔗 **Chain Actions** - Birden fazla eylemi zincirleme olarak çalıştırın
- ⏱️ **Timer System** - Zamanlı eylemler oluşturun
- 🎵 **Sound & Particle Management** - Ses ve parçacık efektlerini kolayca yönetin
- 📝 **Macro Support** - Parametreli fonksiyonlar ile dinamik komutlar
- 🐛 **Debug Mode** - Gelişmiş hata ayıklama araçları
- 📊 **Performance Optimized** - Verimli tick işleme
- 📚 **Rich API** - Kolay entegrasyon için kapsamlı API

## 📦 Kurulum

1. Release sayfasından en son versiyonu indirin
2. Datapack'i `.minecraft/saves/[World Name]/datapacks/` klasörüne kopyalayın
3. Oyuna girin ve `/reload` komutunu çalıştırın
4. Framework otomatik olarak yüklenecektir

## 🚀 Hızlı Başlangıç

### Basit Kullanım

```mcfunction
# Bir mesaj gönder
data modify storage action_framework:temp api_input set value {{\\
    type:"message",\\
    target:"@a",\\
    message:'{{"text":"Hello World!","color":"gold"}}'\\
}}
function action_framework:api/add_action
```

### Chain Action

```mcfunction
# Zincirleme eylemler
function action_framework:examples/chain_example
```

### Macro Kullanımı

```mcfunction
# Oyuncuya eşya ver
function action_framework:macros/give_item {{\\
    target:"@s",\\
    item:"minecraft:diamond",\\
    count:"5"\\
}}
```

## 📖 Dokümantasyon

- [Kullanım Kılavuzu](docs/USAGE.md) - Detaylı kullanım talimatları
- [API Referansı](docs/API.md) - Fonksiyon ve veri yapıları
- [Örnekler](docs/EXAMPLES.md) - Kod örnekleri

## 🎯 Action Türleri

| Tür | Açıklama |
|-----|----------|
| `command` | Minecraft komutu çalıştır |
| `message` | Oyunculara mesaj gönder |
| `sound` | Ses efekti çal |
| `particle` | Parçacık efekti oluştur |
| `summon` | Entity spawn et |
| `chain` | Zincirleme eylemler |
| `delay` | Geciktirilmiş eylem |
| `conditional` | Koşullu eylem |

## 🛠️ API Fonksiyonları

```mcfunction
# Bilgi görüntüle
function action_framework:api/info

# Debug modu
function action_framework:api/debug_toggle

# Kuyruğu temizle
function action_framework:api/clear_queue

# Yardım menüsü
function action_framework:api/help
```

## 🧪 Örnekler

Framework, kullanımı göstermek için birçok örnek içerir:

```mcfunction
# Basit örnek
function action_framework:examples/basic

# Boss tanıtımı
function action_framework:examples/boss_intro

# Minigame başlangıcı
function action_framework:examples/minigame_start
```

## ⚙️ Konfigürasyon

```mcfunction
# Debug modu aç
data modify storage action_framework:main config.debug set value 1b

# Maximum queue boyutu ayarla
data modify storage action_framework:main config.max_queue_size set value 200

# Action logging kapat
data modify storage action_framework:main config.log_actions set value 0b
```

## 🔧 Geliştirme

### Gereksinimler
- Python 3.8+
- Minecraft {self.mc_version}

### Build

```bash
python build.py
```

### Test

```bash
python -m pytest tests/
```

## 📊 Performans

- ✅ Minimal tick impact
- ✅ Efficient queue processing
- ✅ Optimized storage operations
- ✅ Smart caching system

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen:

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Changelog

Detaylı değişiklikler için [CHANGELOG.md](CHANGELOG.md) dosyasına bakın.

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 👥 Yazarlar

- **asn44nb** - *Initial work* - [GitHub](https://github.com/asn44nb)
- **RunToolkit Team** - [Organization](https://github.com/runtoolkit)

## 🙏 Teşekkürler

- Minecraft community
- Datapack creators
- Contributors

## 🔗 Bağlantılar

- [GitHub Repository](https://github.com/runtoolkit/minecraft-action-framework)
- [Issue Tracker](https://github.com/runtoolkit/minecraft-action-framework/issues)
- [Discussions](https://github.com/runtoolkit/minecraft-action-framework/discussions)

## 📞 İletişim

Sorularınız için:
- GitHub Issues açın
- Discussions kullanın
- asn44nb @ GitHub

---

<div align="center">

**Made with ❤️ by RunToolkit**

[⭐ Star](https://github.com/runtoolkit/minecraft-action-framework) · [🐛 Report Bug](https://github.com/runtoolkit/minecraft-action-framework/issues) · [💡 Request Feature](https://github.com/runtoolkit/minecraft-action-framework/issues)

</div>
"""
        readme = readme.replace("{{", "{").replace("}}", "}")
        readme = readme.replace("{self.version}", self.version).replace("{self.mc_version}", self.mc_version)
        (self.output_dir / "README.md").write_text(readme, encoding='utf-8')
        print(self.color.success("✅ README oluşturuldu"))

    def create_changelog(self):
        """CHANGELOG.md oluştur"""
        print(self.color.info("📝 CHANGELOG oluşturuluyor..."))
        
        changelog = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [{self.version}] - {datetime.now().strftime('%Y-%m-%d')}

### Added
- ✨ Initial release
- 🎯 Action queue system with multiple action types
- 🔗 Chain action support for sequential execution
- ⏱️ Timer system for delayed actions
- 🎵 Sound and particle management
- 📝 Macro system for dynamic commands
- 🐛 Debug mode with detailed logging
- 📊 Performance metrics and monitoring
- 📚 Comprehensive API with 10+ functions
- 🛠️ Utility functions (heal, teleport, effects, etc.)
- 📖 Example functions demonstrating usage
- 🎨 Rich tellraw formatting with click events
- 🏷️ Team system for visual organization
- 💾 Advanced storage management
- 🔄 Event system infrastructure
- ⚡ Optimized tick processing
- 📝 Full documentation (USAGE.md, API.md)
- 🧪 Example scenarios (boss intro, minigames, etc.)

### Features
- **Action Types**:
  - Command execution
  - Message broadcasting
  - Sound playback
  - Particle effects
  - Entity summoning
  - Chained actions
  - Delayed execution
  - Conditional logic

- **API Functions**:
  - add_action - Add actions to queue
  - add_action_macro - Add via macro
  - clear_queue - Clear action queue
  - pause_queue - Pause processing
  - resume_queue - Resume processing
  - debug_toggle - Toggle debug mode
  - info - Display framework info
  - help - Show help menu
  - queue_status - Show queue status
  - reload - Reload framework
  - reset - Reset to defaults

- **Utilities**:
  - Random number generation
  - Message broadcasting
  - Player healing
  - Effect management
  - Particle effects
  - Starter kit distribution

- **Examples**:
  - Basic usage
  - Chain actions
  - Particle shows
  - Player welcome sequences
  - Boss introductions
  - Minigame starters

### Technical
- Pack format: {self.pack_format} (MC {self.mc_version})
- Optimized for minimal performance impact
- Smart queue management with overflow protection
- Efficient storage operations
- Modular function organization
- Comprehensive error handling

### Documentation
- Complete usage guide
- API reference
- Code examples
- Installation instructions
- Configuration guide
- Troubleshooting section

## [Unreleased]

### Planned
- 🔮 Predicate system integration
- 🎲 Advanced conditional actions
- 📡 Event listener system expansion
- 🗄️ Database-style player data storage
- 🔐 Permission system
- 🌐 Multi-language support
- 📊 Statistics tracking
- 🎪 More example scenarios
- 🧩 Plugin system for extensions
- ⚙️ Config GUI via book items

### Under Consideration
- NBT-based action templates
- Visual action builder
- Performance profiling tools
- Action scheduling system
- Backup/restore functionality

---

## Version History

### v2.0.0 - Major Rewrite
- Complete framework overhaul
- New builder system
- Enhanced documentation

### v1.0.0 - Initial Release
- Basic action system
- Core functionality

---

**Legend:**
- ✨ New Feature
- 🔧 Improvement
- 🐛 Bug Fix
- 🚀 Performance
- 📝 Documentation
- ⚠️ Breaking Change
- 🗑️ Deprecated

---

*For detailed changes, see the [commit history](https://github.com/runtoolkit/minecraft-action-framework/commits).*
"""
        changelog = changelog.replace("{{", "{").replace("}}", "}")
        changelog = changelog.replace("{self.version}", self.version).replace("{self.mc_version}", self.mc_version).replace("{self.pack_format}", str(self.pack_format))
        changelog = changelog.replace("{datetime.now().strftime('%Y-%m-%d')}", datetime.now().strftime('%Y-%m-%d'))
        (self.output_dir / "CHANGELOG.md").write_text(changelog, encoding='utf-8')
        print(self.color.success("✅ CHANGELOG oluşturuldu"))

    def validate_output(self):
        """Çıktıyı doğrula"""
        print(self.color.info("🔍 Çıktı doğrulanıyor..."))
        
        # Zorunlu dosyaları kontrol et
        required_files = [
            self.output_dir / self.datapack_name / "pack.mcmeta",
            self.output_dir / self.datapack_name / "data" / "action_framework" / "function" / "load.mcfunction",
            self.output_dir / self.datapack_name / "data" / "action_framework" / "function" / "tick.mcfunction",
            self.output_dir / "README.md",
            self.output_dir / "CHANGELOG.md",
        ]
        
        missing_files = []
        for file_path in required_files:
            if not file_path.exists():
                missing_files.append(file_path)
                
        if missing_files:
            print(self.color.warning("⚠️  Eksik dosyalar bulundu:"))
            for file_path in missing_files:
                print(self.color.warning(f"    - {file_path}"))
            self.stats['warnings'] += len(missing_files)
        else:
            print(self.color.success("✅ Tüm zorunlu dosyalar mevcut"))
            
        # Syntax validation
        print(self.color.info("🔍 Syntax kontrolü yapılıyor..."))
        function_dir = self.output_dir / self.datapack_name / "data" / "action_framework" / "function"
        
        for mcfunction_file in function_dir.rglob("*.mcfunction"):
            content = mcfunction_file.read_text(encoding='utf-8')
            is_valid, errors = self.validator.validate_function(content)
            
            if not is_valid:
                print(self.color.warning(f"⚠️  Syntax hatası: {mcfunction_file.name}"))
                for error in errors[:3]:  # İlk 3 hatayı göster
                    print(self.color.warning(f"    - {error}"))
                self.stats['warnings'] += 1
                
        print(self.color.success("✅ Doğrulama tamamlandı"))

    def create_archive(self):
        """Datapack'i zipleyerek arşivle"""
        print(self.color.info("📦 Arşiv oluşturuluyor..."))
        
        import zipfile
        
        datapack_path = self.output_dir / self.datapack_name
        archive_name = f"{self.datapack_name}_v{self.version}_MC{self.mc_version}.zip"
        archive_path = self.output_dir / archive_name
        
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in datapack_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(datapack_path.parent)
                    zipf.write(file_path, arcname)
                    
        file_size = archive_path.stat().st_size / 1024  # KB
        print(self.color.success(f"✅ Arşiv oluşturuldu: {archive_name} ({file_size:.1f} KB)"))

    def print_statistics(self, duration: float):
        """İstatistikleri yazdır"""
        print()
        print(self.color.header("=" * 60))
        print(self.color.header("📊 BUILD İSTATİSTİKLERİ"))
        print(self.color.header("=" * 60))
        print()
        print(f"  ⏱️  Süre: {self.color.success(f'{duration:.2f} saniye')}")
        print(f"  📁 Fonksiyonlar: {self.color.success(str(self.stats['functions_created']))}")
        print(f"  🎯 Eylemler: {self.color.success(str(self.stats['actions_created']))}")
        print(f"  🔄 Makrolar: {self.color.success(str(self.stats['macros_created']))}")
        print(f"  ⚠️  Uyarılar: {self.color.warning(str(self.stats['warnings']))}")
        print(f"  ❌ Hatalar: {self.color.error(str(self.stats['errors']))}")
        print()
        print(self.color.header("=" * 60))
        print()
        print(self.color.success("✅ Build başarıyla tamamlandı!"))
        print()
        print(f"📦 Çıktı: {self.color.info(str(self.output_dir / self.datapack_name))}")
        print()


def main():
    """Ana program"""
    parser = argparse.ArgumentParser(
        description='Minecraft Action Framework Builder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build.py                    # Normal build
  python build.py --verbose          # Detaylı çıktı ile build
  python build.py --config custom.json  # Özel config ile build
  
Author: asn44nb (https://github.com/asn44nb)
Organization: RunToolkit (https://github.com/runtoolkit)
        """
    )
    
    parser.add_argument('--config', '-c', type=Path, help='Custom config file path')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--version', action='version', version='%(prog)s 2.0.0')
    
    args = parser.parse_args()
    
    # Builder oluştur ve çalıştır
    builder = FrameworkBuilder(
        config_path=args.config,
        verbose=args.verbose
    )
    
    success = builder.build()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
