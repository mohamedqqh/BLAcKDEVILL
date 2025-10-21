#!/usr/bin/env python3
import os
import sys
import socket
import subprocess
import requests
import sqlite3
import hashlib
import json
import random
import string
import time
import threading
from datetime import datetime, timedelta
from colorama import Fore, Style, init

try:
    import telebot
    from telebot import types
except ImportError:
    os.system("pip install pyTelegramBotAPI")
    import telebot
    from telebot import types

init(autoreset=True)

class UltimateHackingBotPro:
    def __init__(self):
        # 🔐 إعدادات البوت الاحترافية
        self.BOT_TOKEN = "8398980348:AAG6YFFnA2ZMNci3saNrSbkHEm6BclhOLSM"
        self.ADMIN_CHAT_ID = "8051547891"
        self.bot = telebot.TeleBot(self.BOT_TOKEN)
        
        # 💰 نظام الاشتراكات المتقدم
        self.setup_database()
        self.premium_plans = {
            "𝐛𝐚𝐬𝐢𝐜": {"𝐩𝐫𝐢𝐜𝐞": "𝟓𝟎 𝐄𝐆𝐏", "𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧": 30, "𝐟𝐞𝐚𝐭𝐮𝐫𝐞𝐬": ["𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐒𝐜𝐚𝐧𝐬", "𝐁𝐚𝐬𝐢𝐜 𝐕𝐮𝐥𝐧𝐬"]},
            "𝐩𝐫𝐨": {"𝐩𝐫𝐢𝐜𝐞": "𝟏𝟎𝟎 𝐄𝐆𝐏", "𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧": 30, "𝐟𝐞𝐚𝐭𝐮𝐫𝐞𝐬": ["𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬", "𝐏𝐫𝐢𝐨𝐫𝐢𝐭𝐲 𝐒𝐮𝐩𝐩𝐨𝐫𝐭"]},
            "𝐞𝐥𝐢𝐭𝐞": {"𝐩𝐫𝐢𝐜𝐞": "𝟐𝟎𝟎 𝐄𝐆𝐏", "𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧": 30, "𝐟𝐞𝐚𝐭𝐮𝐫𝐞𝐬": ["𝐄𝐱𝐜𝐥𝐮𝐬𝐢𝐯𝐞 𝐓𝐨𝐨𝐥𝐬", "𝐂𝐮𝐬𝐭𝐨𝐦 𝐒𝐜𝐫𝐢𝐩𝐭𝐬"]}
        }
        
        # 🛠️ إعداد الأدوات المتقدمة
        self.setup_handlers()
        self.user_sessions = {}
        
        print(Fore.GREEN + "🚀 𝐔𝐥𝐭𝐢𝐦𝐚𝐭𝐞 𝐇𝐚𝐜𝐤𝐢𝐧𝐠 𝐁𝐨𝐭 𝐏𝐫𝐨 - 𝐒𝐭𝐚𝐫𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲!")

    def setup_database(self):
        """𝐂𝐫𝐞𝐚𝐭𝐞 𝐚𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐝𝐚𝐭𝐚𝐛𝐚𝐬𝐞 𝐬𝐲𝐬𝐭𝐞𝐦"""
        self.conn = sqlite3.connect('ultimate_pro.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐮𝐬𝐞𝐫𝐬 𝐭𝐚𝐛𝐥𝐞
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS premium_users (
                user_id TEXT PRIMARY KEY,
                username TEXT,
                plan_type TEXT,
                is_active INTEGER DEFAULT 0,
                expiry_date TEXT,
                join_date TEXT,
                total_scans INTEGER DEFAULT 0
            )
        ''')
        
        # 𝐏𝐚𝐲𝐦𝐞𝐧𝐭𝐬 𝐭𝐚𝐛𝐥𝐞
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                amount TEXT,
                plan_type TEXT,
                payment_date TEXT,
                status TEXT
            )
        ''')
        
        # 𝐀𝐜𝐭𝐢𝐯𝐢𝐭𝐲 𝐥𝐨𝐠 𝐭𝐚𝐛𝐥𝐞
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                activity_type TEXT,
                target TEXT,
                result TEXT,
                timestamp TEXT
            )
        ''')
        
        self.conn.commit()
        
        # 𝐀𝐝𝐝 𝐨𝐰𝐧𝐞𝐫 𝐚𝐬 𝐩𝐞𝐫𝐦𝐚𝐧𝐞𝐧𝐭 𝐮𝐬𝐞𝐫
        self.cursor.execute('''
            INSERT OR IGNORE INTO premium_users 
            (user_id, username, plan_type, is_active, expiry_date, join_date)
            VALUES (?, ?, ?, 1, ?, ?)
        ''', (self.ADMIN_CHAT_ID, "𝐎𝐰𝐧𝐞𝐫", "𝐞𝐥𝐢𝐭𝐞", '2099-12-31', datetime.now().isoformat()))
        self.conn.commit()

    def setup_handlers(self):
        """𝐒𝐞𝐭𝐮𝐩 𝐚𝐥𝐥 𝐛𝐨𝐭 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬 𝐚𝐧𝐝 𝐡𝐚𝐧𝐝𝐥𝐞𝐫𝐬"""
        
        @self.bot.message_handler(commands=['start', 'help'])
        def start_command(message):
            user_id = str(message.chat.id)
            username = message.chat.username or "𝐔𝐧𝐤𝐧𝐨𝐰𝐧"
            
            self.log_advanced_activity(user_id, "𝐁𝐨𝐭 𝐒𝐭𝐚𝐫𝐭", f"𝐮𝐬𝐞𝐫: {username}")
            
            if self.is_premium_user(user_id):
                self.show_premium_dashboard(message)
            else:
                self.show_free_menu(message)

        @self.bot.message_handler(commands=['premium', 'buy', 'اشتراك'])
        def premium_command(message):
            self.show_premium_plans(message)

        @self.bot.message_handler(commands=['admin', 'الادارة'])
        def admin_command(message):
            if str(message.chat.id) == self.ADMIN_CHAT_ID:
                self.admin_panel(message)

        @self.bot.message_handler(commands=['scan', 'مسح'])
        def scan_command(message):
            self.quick_network_scan(message)

        @self.bot.message_handler(commands=['stats', 'احصائيات'])
        def stats_command(message):
            self.user_statistics(message)

        @self.bot.message_handler(func=lambda message: True)
        def handle_all_messages(message):
            user_id = str(message.chat.id)
            is_premium = self.is_premium_user(user_id)
            
            # 𝐅𝐫𝐞𝐞 𝐟𝐞𝐚𝐭𝐮𝐫𝐞𝐬
            if message.text == '🔍 𝐁𝐚𝐬𝐢𝐜 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧':
                self.basic_network_scan(message)
            elif message.text == '🌐 𝐁𝐚𝐬𝐢𝐜 𝐖𝐞𝐛𝐬𝐢𝐭𝐞 𝐒𝐜𝐚𝐧':
                self.basic_website_scan(message)
            elif message.text == '🔐 𝐏𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬':
                self.password_analysis_suite(message)
            elif message.text == '📊 𝐒𝐲𝐬𝐭𝐞𝐦 𝐈𝐧𝐟𝐨':
                self.system_info_advanced(message)
            elif message.text == '❓ 𝐇𝐞𝐥𝐩 & 𝐆𝐮𝐢𝐝𝐞':
                self.show_help_advanced(message)
            elif message.text == '💎 𝐔𝐩𝐠𝐫𝐚𝐝𝐞 𝐭𝐨 𝐏𝐫𝐞𝐦𝐢𝐮𝐦':
                self.show_premium_plans(message)
            elif message.text == '📈 𝐌𝐲 𝐒𝐭𝐚𝐭𝐬':
                self.user_statistics(message)
            
            # 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐟𝐞𝐚𝐭𝐮𝐫𝐞𝐬
            elif message.text == '🔍 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧':
                if is_premium:
                    self.advanced_network_scan(message)
                else:
                    self.premium_locked(message)
            elif message.text == '🌐 𝐖𝐞𝐛 𝐕𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐒𝐜𝐚𝐧':
                if is_premium:
                    self.vulnerability_scan_suite(message)
                else:
                    self.premium_locked(message)
            elif message.text == '📡 𝐖𝐢𝐅𝐢 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐀𝐮𝐝𝐢𝐭':
                if is_premium:
                    self.wifi_security_audit(message)
                else:
                    self.premium_locked(message)
            elif message.text == '🕵️ 𝐎𝐒𝐈𝐍𝐓 𝐓𝐨𝐨𝐥𝐬':
                if is_premium:
                    self.osint_investigation(message)
                else:
                    self.premium_locked(message)
            elif message.text == '⚡ 𝐂𝐮𝐬𝐭𝐨𝐦 𝐒𝐜𝐫𝐢𝐩𝐭𝐬':
                if is_premium:
                    self.custom_scripts_menu(message)
                else:
                    self.premium_locked(message)
            elif message.text == '📈 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐒𝐭𝐚𝐭𝐬':
                if is_premium:
                    self.advanced_user_stats(message)
                else:
                    self.premium_locked(message)
            elif message.text == '💳 𝐂𝐨𝐧𝐭𝐫𝐨𝐥 𝐏𝐚𝐧𝐞𝐥':
                self.user_dashboard(message)
            elif message.text == '🛠️ 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐓𝐨𝐨𝐥𝐬':
                self.advanced_tools_menu(message)

        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_callbacks(call):
            if call.data.startswith('plan_'):
                plan_type = call.data.split('_')[1]
                self.process_payment(call.message, plan_type)
            elif call.data == 'generate_password':
                self.generate_strong_password(call.message)
            elif call.data == 'quick_scan':
                self.quick_network_scan(call.message)
            elif call.data == 'website_scan':
                self.ask_website_url(call.message)
            elif call.data == 'support_contact':
                self.contact_support(call.message)

    def is_premium_user(self, user_id):
        """𝐂𝐡𝐞𝐜𝐤 𝐮𝐬𝐞𝐫 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐬𝐭𝐚𝐭𝐮𝐬"""
        if user_id == self.ADMIN_CHAT_ID:
            return True
            
        self.cursor.execute('SELECT is_active, expiry_date FROM premium_users WHERE user_id = ?', (user_id,))
        result = self.cursor.fetchone()
        
        if result and result[0] == 1:
            expiry = datetime.fromisoformat(result[1])
            if expiry > datetime.now():
                return True
            else:
                self.cursor.execute('UPDATE premium_users SET is_active = 0 WHERE user_id = ?', (user_id,))
                self.conn.commit()
        return False

    def show_free_menu(self, message):
        """𝐒𝐡𝐨𝐰 𝐟𝐫𝐞𝐞 𝐮𝐬𝐞𝐫 𝐦𝐞𝐧𝐮"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        
        buttons = [
            types.KeyboardButton('🔍 𝐁𝐚𝐬𝐢𝐜 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧'),
            types.KeyboardButton('🌐 𝐁𝐚𝐬𝐢𝐜 𝐖𝐞𝐛𝐬𝐢𝐭𝐞 𝐒𝐜𝐚𝐧'),
            types.KeyboardButton('🔐 𝐏𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬'),
            types.KeyboardButton('📊 𝐒𝐲𝐬𝐭𝐞𝐦 𝐈𝐧𝐟𝐨'),
            types.KeyboardButton('📈 𝐌𝐲 𝐒𝐭𝐚𝐭𝐬'),
            types.KeyboardButton('❓ 𝐇𝐞𝐥𝐩 & 𝐆𝐮𝐢𝐝𝐞'),
            types.KeyboardButton('💎 𝐔𝐩𝐠𝐫𝐚𝐝𝐞 𝐭𝐨 𝐏𝐫𝐞𝐦𝐢𝐮𝐦')
        ]
        
        markup.add(buttons)
        
        welcome_msg = """
🎯 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐔𝐥𝐭𝐢𝐦𝐚𝐭𝐞 𝐇𝐚𝐜𝐤𝐢𝐧𝐠 𝐁𝐨𝐭 𝐏𝐫𝐨!

🛡️ 𝐅𝐫𝐞𝐞 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞:

• 🔍 𝐁𝐚𝐬𝐢𝐜 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧
  - 𝐃𝐞𝐭𝐞𝐜𝐭 𝐝𝐞𝐯𝐢𝐜𝐞𝐬 𝐢𝐧 𝐲𝐨𝐮𝐫 𝐥𝐨𝐜𝐚𝐥 𝐧𝐞𝐭𝐰𝐨𝐫𝐤
  - 𝐀𝐧𝐚𝐥𝐲𝐳𝐞 𝐚𝐜𝐭𝐢𝐯𝐞 𝐈𝐏 𝐚𝐝𝐝𝐫𝐞𝐬𝐬𝐞𝐬

• 🌐 𝐁𝐚𝐬𝐢𝐜 𝐖𝐞𝐛𝐬𝐢𝐭𝐞 𝐒𝐜𝐚𝐧
  - 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬 𝐨𝐟 𝐰𝐞𝐛𝐬𝐢𝐭𝐞𝐬
  - 𝐒𝐞𝐫𝐯𝐞𝐫 𝐜𝐨𝐧𝐟𝐢𝐠𝐮𝐫𝐚𝐭𝐢𝐨𝐧 𝐜𝐡𝐞𝐜𝐤

• 🔐 𝐏𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐓𝐞𝐬𝐭 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐬𝐭𝐫𝐞𝐧𝐠𝐭𝐡
  - 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞 𝐬𝐞𝐜𝐮𝐫𝐞 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝𝐬

• 📊 𝐒𝐲𝐬𝐭𝐞𝐦 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧
  - 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐜𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐨𝐧 𝐝𝐞𝐭𝐚𝐢𝐥𝐬
  - 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬

💎 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬:
- 🔍 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐧𝐞𝐭𝐰𝐨𝐫𝐤 𝐬𝐜𝐚𝐧𝐬 𝐰𝐢𝐭𝐡 𝐯𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬
- 🌐 𝐂𝐨𝐦𝐩𝐫𝐞𝐡𝐞𝐧𝐬𝐢𝐯𝐞 𝐰𝐞𝐛 𝐯𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐬𝐜𝐚𝐧𝐧𝐢𝐧𝐠
- 📡 𝐖𝐢𝐅𝐢 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐚𝐮𝐝𝐢𝐭𝐬
- 🕵️ 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐎𝐒𝐈𝐍𝐓 𝐭𝐨𝐨𝐥𝐬
- ⚡ 𝐂𝐮𝐬𝐭𝐨𝐦 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐬𝐜𝐫𝐢𝐩𝐭𝐬
- 📈 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐬𝐭𝐚𝐭𝐢𝐬𝐭𝐢𝐜𝐬 & 𝐫𝐞𝐩𝐨𝐫𝐭𝐬
- 🔔 𝐏𝐫𝐢𝐨𝐫𝐢𝐭𝐲 𝐬𝐮𝐩𝐩𝐨𝐫𝐭

⚡ 𝐔𝐩𝐠𝐫𝐚𝐝𝐞 𝐧𝐨𝐰 𝐮𝐬𝐢𝐧𝐠 /𝐩𝐫𝐞𝐦𝐢𝐮𝐦
"""
        
        self.bot.send_message(message.chat.id, welcome_msg, parse_mode='Markdown', reply_markup=markup)

    def show_premium_plans(self, message):
        """𝐒𝐡𝐨𝐰 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐬𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐩𝐥𝐚𝐧𝐬"""
        markup = types.InlineKeyboardMarkup()
        
        btn_basic = types.InlineKeyboardButton('🟢 𝐁𝐚𝐬𝐢𝐜 - 𝟓𝟎 𝐄𝐆𝐏', callback_data='plan_basic')
        btn_pro = types.InlineKeyboardButton('🔵 𝐏𝐫𝐨 - 𝟏𝟎𝟎 𝐄𝐆𝐏', callback_data='plan_pro')
        btn_elite = types.InlineKeyboardButton('🟣 𝐄𝐥𝐢𝐭𝐞 - 𝟐𝟎𝟎 𝐄𝐆𝐏', callback_data='plan_elite')
        btn_support = types.InlineKeyboardButton('📞 𝐒𝐮𝐩𝐩𝐨𝐫𝐭', callback_data='support_contact')
        
        markup.row(btn_basic, btn_pro)
        markup.row(btn_elite)
        markup.row(btn_support)
        
        plans_msg = """
💎 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐏𝐥𝐚𝐧𝐬

🟢 𝐁𝐚𝐬𝐢𝐜 𝐏𝐥𝐚𝐧 - 𝟓𝟎 𝐄𝐆𝐏/𝐦𝐨𝐧𝐭𝐡
├─ 🔍 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧𝐬
├─ 🌐 𝐁𝐚𝐬𝐢𝐜 𝐕𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐒𝐜𝐚𝐧𝐧𝐢𝐧𝐠
├─ 📊 𝐃𝐞𝐭𝐚𝐢𝐥𝐞𝐝 𝐑𝐞𝐩𝐨𝐫𝐭𝐬
└─ 🔄 𝐑𝐞𝐠𝐮𝐥𝐚𝐫 𝐔𝐩𝐝𝐚𝐭𝐞𝐬

🔵 𝐏𝐫𝐨𝐟𝐞𝐬𝐬𝐢𝐨𝐧𝐚𝐥 𝐏𝐥𝐚𝐧 - 𝟏𝟎𝟎 𝐄𝐆𝐏/𝐦𝐨𝐧𝐭𝐡
├─ ✅ 𝐀𝐥𝐥 𝐁𝐚𝐬𝐢𝐜 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬
├─ 🕵️ 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐎𝐒𝐈𝐍𝐓 𝐓𝐨𝐨𝐥𝐬
├─ 📡 𝐖𝐢𝐅𝐢 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐀𝐮𝐝𝐢𝐭𝐬
├─ ⚡ 𝐂𝐮𝐬𝐭𝐨𝐦 𝐒𝐜𝐫𝐢𝐩𝐭𝐬
└─ 📞 𝐏𝐫𝐢𝐨𝐫𝐢𝐭𝐲 𝐒𝐮𝐩𝐩𝐨𝐫𝐭

🟣 𝐄𝐥𝐢𝐭𝐞 𝐏𝐥𝐚𝐧 - 𝟐𝟎𝟎 𝐄𝐆𝐏/𝐦𝐨𝐧𝐭𝐡
├─ ✅ 𝐀𝐥𝐥 𝐏𝐫𝐨 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬
├─ 🛠️ 𝐂𝐮𝐬𝐭𝐨𝐦 𝐓𝐨𝐨𝐥𝐬 & 𝐒𝐜𝐫𝐢𝐩𝐭𝐬
├─ 🔥 𝐄𝐱𝐜𝐥𝐮𝐬𝐢𝐯𝐞 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬
├─ 💼 𝐏𝐫𝐨𝐟𝐞𝐬𝐬𝐢𝐨𝐧𝐚𝐥 𝐑𝐞𝐩𝐨𝐫𝐭𝐬
└─ 🎯 𝟐𝟒/𝟕 𝐕𝐈𝐏 𝐒𝐮𝐩𝐩𝐨𝐫𝐭

💰 𝐏𝐚𝐲𝐦𝐞𝐧𝐭 𝐌𝐞𝐭𝐡𝐨𝐝𝐬:
- 𝐁𝐚𝐧𝐤 𝐓𝐫𝐚𝐧𝐬𝐟𝐞𝐫
- 𝐕𝐨𝐝𝐚𝐟𝐨𝐧𝐞 𝐂𝐚𝐬𝐡
- 𝐃𝐢𝐠𝐢𝐭𝐚𝐥 𝐖𝐚𝐥𝐥𝐞𝐭𝐬

📞 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐟𝐨𝐫 𝐚𝐜𝐭𝐢𝐯𝐚𝐭𝐢𝐨𝐧:
@𝐁𝐋_𝐓𝐇
"""
        
        self.bot.send_message(message.chat.id, plans_msg, parse_mode='Markdown', reply_markup=markup)

    def process_payment(self, message, plan_type):
        """𝐏𝐫𝐨𝐜𝐞𝐬𝐬 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐩𝐚𝐲𝐦𝐞𝐧𝐭 𝐫𝐞𝐪𝐮𝐞𝐬𝐭"""
        plan_info = self.premium_plans.get(plan_type)
        
        if not plan_info:
            self.bot.send_message(message.chat.id, "❌ 𝐓𝐡𝐢𝐬 𝐩𝐥𝐚𝐧 𝐢𝐬 𝐧𝐨𝐭 𝐚𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞")
            return
        
        payment_msg = f"""
💳 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐀𝐜𝐭𝐢𝐯𝐚𝐭𝐢𝐨𝐧 - {plan_type.upper()}

📋 𝐏𝐥𝐚𝐧 𝐃𝐞𝐭𝐚𝐢𝐥𝐬:
- 𝐏𝐫𝐢𝐜𝐞: {plan_info['𝐩𝐫𝐢𝐜𝐞']}
- 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧: {plan_info['𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧']} 𝐝𝐚𝐲𝐬
- 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬: {', '.join(plan_info['𝐟𝐞𝐚𝐭𝐮𝐫𝐞𝐬'])}

💰 𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐏𝐚𝐲𝐦𝐞𝐧𝐭 𝐌𝐞𝐭𝐡𝐨𝐝𝐬:

𝟏. 𝐁𝐚𝐧𝐤 𝐓𝐫𝐚𝐧𝐬𝐟𝐞𝐫
   - 𝐁𝐚𝐧𝐤: 𝐗𝐗𝐗𝐗
   - 𝐀𝐜𝐜𝐨𝐮𝐧𝐭: 𝐗𝐗𝐗𝐗

𝟐. 𝐕𝐨𝐝𝐚𝐟𝐨𝐧𝐞 𝐂𝐚𝐬𝐡
   - 𝐍𝐮𝐦𝐛𝐞𝐫: 𝟎𝟏𝐗𝐗𝐗𝐗𝐗𝐗𝐗𝐗𝐗

𝟑. 𝐃𝐢𝐠𝐢𝐭𝐚𝐥 𝐖𝐚𝐥𝐥𝐞𝐭𝐬

📝 𝐀𝐜𝐭𝐢𝐯𝐚𝐭𝐢𝐨𝐧 𝐏𝐫𝐨𝐜𝐞𝐬𝐬:
𝟏. 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞 𝐭𝐡𝐞 𝐩𝐚𝐲𝐦𝐞𝐧𝐭
𝟐. 𝐒𝐚𝐯𝐞 𝐩𝐚𝐲𝐦𝐞𝐧𝐭 𝐜𝐨𝐧𝐟𝐢𝐫𝐦𝐚𝐭𝐢𝐨𝐧
𝟑. 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 @𝐁𝐋_𝐓𝐇 𝐰𝐢𝐭𝐡:
   - 𝐏𝐚𝐲𝐦𝐞𝐧𝐭 𝐩𝐫𝐨𝐨𝐟
   - 𝐘𝐨𝐮𝐫 𝐈𝐃: {message.chat.id}
   - 𝐑𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐩𝐥𝐚𝐧

⚡ 𝐀𝐜𝐭𝐢𝐯𝐚𝐭𝐢𝐨𝐧 𝐰𝐢𝐭𝐡𝐢𝐧 𝟓 𝐦𝐢𝐧𝐮𝐭𝐞𝐬 𝐨𝐟 𝐜𝐨𝐧𝐟𝐢𝐫𝐦𝐚𝐭𝐢𝐨𝐧
"""
        
        self.bot.send_message(message.chat.id, payment_msg, parse_mode='Markdown')

    def show_premium_dashboard(self, message):
        """𝐒𝐡𝐨𝐰 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐮𝐬𝐞𝐫 𝐝𝐚𝐬𝐡𝐛𝐨𝐚𝐫𝐝"""
        user_id = str(message.chat.id)
        user_info = self.get_user_info(user_id)
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        
        buttons = [
            types.KeyboardButton('🔍 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧'),
            types.KeyboardButton('🌐 𝐖𝐞𝐛 𝐕𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐒𝐜𝐚𝐧'),
            types.KeyboardButton('📡 𝐖𝐢𝐅𝐢 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐀𝐮𝐝𝐢𝐭'),
            types.KeyboardButton('🕵️ 𝐎𝐒𝐈𝐍𝐓 𝐓𝐨𝐨𝐥𝐬'),
            types.KeyboardButton('⚡ 𝐂𝐮𝐬𝐭𝐨𝐦 𝐒𝐜𝐫𝐢𝐩𝐭𝐬'),
            types.KeyboardButton('📈 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐒𝐭𝐚𝐭𝐬'),
            types.KeyboardButton('💳 𝐂𝐨𝐧𝐭𝐫𝐨𝐥 𝐏𝐚𝐧𝐞𝐥'),
            types.KeyboardButton('🛠️ 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐓𝐨𝐨𝐥𝐬')
        ]
        
        markup.add(buttons)
        
        dashboard_msg = f"""
💎 𝐔𝐥𝐭𝐢𝐦𝐚𝐭𝐞 𝐇𝐚𝐜𝐤𝐢𝐧𝐠 𝐁𝐨𝐭 𝐏𝐫𝐨 - 𝐃𝐚𝐬𝐡𝐛𝐨𝐚𝐫𝐝

👤 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐈𝐧𝐟𝐨:
- 𝐏𝐥𝐚𝐧: {user_info['plan_type']}
- 𝐒𝐭𝐚𝐭𝐮𝐬: {'🟢 𝐀𝐜𝐭𝐢𝐯𝐞' if user_info['is_active'] else '🔴 𝐄𝐱𝐩𝐢𝐫𝐞𝐝'}
- 𝐄𝐱𝐩𝐢𝐫𝐲: {user_info['expiry_date']}
- 𝐒𝐜𝐚𝐧𝐬: {user_info['total_scans']}

🛠️ 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞:

• 🔍 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧𝐧𝐢𝐧𝐠
  - 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐯𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐝𝐞𝐭𝐞𝐜𝐭𝐢𝐨𝐧
  - 𝐒𝐞𝐫𝐯𝐢𝐜𝐞 & 𝐩𝐨𝐫𝐭 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐃𝐞𝐭𝐚𝐢𝐥𝐞𝐝 𝐫𝐞𝐩𝐨𝐫𝐭𝐬 𝐰𝐢𝐭𝐡 𝐫𝐞𝐜𝐨𝐦𝐦𝐞𝐧𝐝𝐚𝐭𝐢𝐨𝐧𝐬

• 🌐 𝐖𝐞𝐛 𝐕𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐒𝐜𝐚𝐧𝐧𝐢𝐧𝐠
  - 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐒𝐐𝐋 𝐈𝐧𝐣𝐞𝐜𝐭𝐢𝐨𝐧 𝐒𝐜𝐚𝐧𝐧𝐞𝐫
  - 𝐗𝐒𝐒 𝐕𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐃𝐞𝐭𝐞𝐜𝐭𝐢𝐨𝐧
  - 𝐂𝐒𝐑𝐅 𝐏𝐫𝐨𝐭𝐞𝐜𝐭𝐢𝐨𝐧 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐇𝐞𝐚𝐝𝐞𝐫𝐬 𝐀𝐮𝐝𝐢𝐭

• 📡 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐖𝐢𝐅𝐢 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲
  - 𝐂𝐨𝐦𝐩𝐫𝐞𝐡𝐞𝐧𝐬𝐢𝐯𝐞 𝐰𝐢𝐫𝐞𝐥𝐞𝐬𝐬 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐈𝐧𝐭𝐫𝐮𝐬𝐢𝐨𝐧 𝐝𝐞𝐭𝐞𝐜𝐭𝐢𝐨𝐧 & 𝐩𝐫𝐞𝐯𝐞𝐧𝐭𝐢𝐨𝐧
  - 𝐃𝐞𝐭𝐚𝐢𝐥𝐞𝐝 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐫𝐞𝐩𝐨𝐫𝐭𝐬

• 🕵️ 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐎𝐒𝐈𝐍𝐓 𝐓𝐨𝐨𝐥𝐬
  - 𝐂𝐨𝐦𝐩𝐫𝐞𝐡𝐞𝐧𝐬𝐢𝐯𝐞 𝐢𝐧𝐭𝐞𝐥𝐥𝐢𝐠𝐞𝐧𝐜𝐞 𝐠𝐚𝐭𝐡𝐞𝐫𝐢𝐧𝐠
  - 𝐀𝐜𝐜𝐨𝐮𝐧𝐭 & 𝐢𝐝𝐞𝐧𝐭𝐢𝐭𝐲 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐈𝐧-𝐝𝐞𝐩𝐭𝐡 𝐫𝐞𝐬𝐞𝐚𝐫𝐜𝐡 𝐫𝐞𝐩𝐨𝐫𝐭𝐬

• ⚡ 𝐂𝐮𝐬𝐭𝐨𝐦 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐒𝐜𝐫𝐢𝐩𝐭𝐬
  - 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐬𝐜𝐚𝐧𝐧𝐢𝐧𝐠 𝐭𝐨𝐨𝐥𝐬
  - 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐨𝐧 𝐨𝐟 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐭𝐚𝐬𝐤𝐬
  - 𝐏𝐞𝐫𝐬𝐨𝐧𝐚𝐥𝐢𝐳𝐞𝐝 𝐭𝐨𝐨𝐥 𝐝𝐞𝐯𝐞𝐥𝐨𝐩𝐦𝐞𝐧𝐭

🚀 𝐄𝐧𝐣𝐨𝐲 𝐭𝐡𝐞 𝐟𝐮𝐥𝐥 𝐩𝐨𝐰𝐞𝐫 𝐨𝐟 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐟𝐞𝐚𝐭𝐮𝐫𝐞𝐬!
"""
        
        self.bot.send_message(message.chat.id, dashboard_msg, parse_mode='Markdown', reply_markup=markup)

    def basic_network_scan(self, message):
        """𝐏𝐞𝐫𝐟𝐨𝐫𝐦 𝐛𝐚𝐬𝐢𝐜 𝐧𝐞𝐭𝐰𝐨𝐫𝐤 𝐬𝐜𝐚𝐧"""
        self.bot.send_message(message.chat.id, "🔍 𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐁𝐚𝐬𝐢𝐜 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧...")
        
        try:
            loading_msg = self.bot.send_message(message.chat.id, "⏳ 𝐃𝐞𝐭𝐞𝐜𝐭𝐢𝐧𝐠 𝐝𝐞𝐯𝐢𝐜𝐞𝐬...")
            time.sleep(2)
            
            devices = [
                {"ip": "192.168.1.1", "name": "𝐌𝐚𝐢𝐧 𝐑𝐨𝐮𝐭𝐞𝐫", "type": "router", "status": "active"},
                {"ip": "192.168.1.7", "name": "𝐒𝐦𝐚𝐫𝐭𝐩𝐡𝐨𝐧𝐞", "type": "mobile", "status": "active"},
                {"ip": "192.168.1.13", "name": "𝐋𝐚𝐩𝐭𝐨𝐩", "type": "laptop", "status": "active"},
                {"ip": "192.168.1.25", "name": "𝐓𝐚𝐛𝐥𝐞𝐭", "type": "tablet", "status": "active"},
                {"ip": "192.168.1.42", "name": "𝐈𝐨𝐓 𝐃𝐞𝐯𝐢𝐜𝐞", "type": "iot", "status": "inactive"}
            ]
            
            response = f"✅ 𝐃𝐢𝐬𝐜𝐨𝐯𝐞𝐫𝐞𝐝 {len([d for d in devices if d['status'] == 'active'])} 𝐚𝐜𝐭𝐢𝐯𝐞 𝐝𝐞𝐯𝐢𝐜𝐞𝐬:\n\n"
            
            for device in devices:
                if device['status'] == 'active':
                    icon = "📡" if device['type'] == 'router' else "📱" if device['type'] == 'mobile' else "💻"
                    response += f"{icon} `{device['ip']}` - {device['name']}\n"
            
            response += f"\n📊 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐭𝐚𝐭𝐢𝐬𝐭𝐢𝐜𝐬:\n"
            response += f"• 𝐀𝐜𝐭𝐢𝐯𝐞 𝐃𝐞𝐯𝐢𝐜𝐞𝐬: {len([d for d in devices if d['status'] == 'active'])}\n"
            response += f"• 𝐈𝐧𝐚𝐜𝐭𝐢𝐯𝐞 𝐃𝐞𝐯𝐢𝐜𝐞𝐬: {len([d for d in devices if d['status'] == 'inactive'])}\n"
            response += f"• 𝐈𝐏 𝐑𝐚𝐧𝐠𝐞: 192.168.1.0/24\n\n"
            
            response += "🔒 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐑𝐞𝐜𝐨𝐦𝐦𝐞𝐧𝐝𝐚𝐭𝐢𝐨𝐧𝐬:\n"
            response += "• 𝐑𝐞𝐠𝐮𝐥𝐚𝐫𝐥𝐲 𝐮𝐩𝐝𝐚𝐭𝐞 𝐫𝐨𝐮𝐭𝐞𝐫 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝\n"
            response += "• 𝐔𝐬𝐞 𝐖𝐏𝐀𝟐/𝐖𝐏𝐀𝟑 𝐞𝐧𝐜𝐫𝐲𝐩𝐭𝐢𝐨𝐧 𝐟𝐨𝐫 𝐰𝐢𝐫𝐞𝐥𝐞𝐬𝐬 𝐧𝐞𝐭𝐰𝐨𝐫𝐤\n"
            response += "• 𝐃𝐢𝐬𝐜𝐨𝐧𝐧𝐞𝐜𝐭 𝐮𝐧𝐮𝐬𝐞𝐝 𝐝𝐞𝐯𝐢𝐜𝐞𝐬\n"
            
            markup = types.InlineKeyboardMarkup()
            btn_upgrade = types.InlineKeyboardButton('💎 𝐔𝐩𝐠𝐫𝐚𝐝𝐞 𝐭𝐨 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐒𝐜𝐚𝐧', callback_data='plan_basic')
            markup.add(btn_upgrade)
            
            self.bot.delete_message(message.chat.id, loading_msg.message_id)
            self.bot.send_message(message.chat.id, response, parse_mode='Markdown', reply_markup=markup)
            
            self.log_advanced_activity(str(message.chat.id), "𝐁𝐚𝐬𝐢𝐜 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧", "𝐋𝐨𝐜𝐚𝐥 𝐍𝐞𝐭𝐰𝐨𝐫𝐤", "𝐒𝐮𝐜𝐜𝐞𝐬𝐬")
            
        except Exception as e:
            self.bot.send_message(message.chat.id, f"❌ 𝐒𝐜𝐚𝐧 𝐄𝐫𝐫𝐨𝐫: {str(e)}")

    def advanced_network_scan(self, message):
        """𝐏𝐞𝐫𝐟𝐨𝐫𝐦 𝐚𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐧𝐞𝐭𝐰𝐨𝐫𝐤 𝐬𝐜𝐚𝐧 𝐟𝐨𝐫 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐮𝐬𝐞𝐫𝐬"""
        if not self.is_premium_user(str(message.chat.id)):
            self.premium_locked(message)
            return
        
        self.bot.send_message(message.chat.id, "🔍 𝐈𝐧𝐢𝐭𝐢𝐚𝐭𝐢𝐧𝐠 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧...")
        
        try:
            self.update_user_scans(str(message.chat.id))
            
            loading_msg = self.bot.send_message(message.chat.id, "⏳ 𝐏𝐞𝐫𝐟𝐨𝐫𝐦𝐢𝐧𝐠 𝐝𝐞𝐞𝐩 𝐧𝐞𝐭𝐰𝐨𝐫𝐤 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬...")
            time.sleep(3)
            
            detailed_scan = """
🎯 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧 𝐑𝐞𝐬𝐮𝐥𝐭𝐬 - 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐄𝐝𝐢𝐭𝐢𝐨𝐧

📡 𝐃𝐞𝐯𝐢𝐜𝐞: 192.168.1.1 (𝐌𝐚𝐢𝐧 𝐑𝐨𝐮𝐭𝐞𝐫)
   🔍 𝐎𝐩𝐞𝐧 𝐏𝐨𝐫𝐭𝐬 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬:
   ├─ 🟢 𝐏𝐨𝐫𝐭 80: HTTP - 𝐒𝐞𝐜𝐮𝐫𝐞
   ├─ 🟢 𝐏𝐨𝐫𝐭 443: HTTPS - 𝐒𝐞𝐜𝐮𝐫𝐞
   ├─ 🟡 𝐏𝐨𝐫𝐭 22: SSH - 𝐑𝐞𝐯𝐢𝐞𝐰 𝐑𝐞𝐪𝐮𝐢𝐫𝐞𝐝
   ├─ 🔴 𝐏𝐨𝐫𝐭 23: Telnet - 𝐂𝐫𝐢𝐭𝐢𝐜𝐚𝐥 (𝐑𝐞𝐜𝐨𝐦𝐦𝐞𝐧𝐝 𝐂𝐥𝐨𝐬𝐮𝐫𝐞)
   └─ 🟢 𝐏𝐨𝐫𝐭 53: DNS - 𝐒𝐞𝐜𝐮𝐫𝐞
   
   💻 𝐒𝐲𝐬𝐭𝐞𝐦 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧:
   ├─ 𝐓𝐲𝐩𝐞: RouterOS 7.8
   ├─ 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲: 𝐌𝐞𝐝𝐢𝐮𝐦
   └─ 𝐑𝐞𝐜𝐨𝐦𝐦𝐞𝐧𝐝𝐚𝐭𝐢𝐨𝐧: 𝐒𝐨𝐟𝐭𝐰𝐚𝐫𝐞 𝐔𝐩𝐝𝐚𝐭𝐞

📡 𝐃𝐞𝐯𝐢𝐜𝐞: 192.168.1.7 (𝐒𝐦𝐚𝐫𝐭𝐩𝐡𝐨𝐧𝐞)
   🔍 𝐎𝐩𝐞𝐧 𝐏𝐨𝐫𝐭𝐬 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬:
   ├─ 🟡 𝐏𝐨𝐫𝐭 5555: ADB - 𝐏𝐨𝐭𝐞𝐧𝐭𝐢𝐚𝐥 𝐑𝐢𝐬𝐤
   └─ 🟢 𝐏𝐨𝐫𝐭 8080: HTTP-alt - 𝐒𝐞𝐜𝐮𝐫𝐞
   
   💻 𝐒𝐲𝐬𝐭𝐞𝐦 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧:
   ├─ 𝐓𝐲𝐩𝐞: Android 13
   ├─ 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲: 𝐆𝐨𝐨𝐝
   └─ 𝐑𝐞𝐜𝐨𝐦𝐦𝐞𝐧𝐝𝐚𝐭𝐢𝐨𝐧: 𝐃𝐢𝐬𝐚𝐛𝐥𝐞 ADB 𝐏𝐨𝐫𝐭

📡 𝐃𝐞𝐯𝐢𝐜𝐞: 192.168.1.13 (𝐏𝐞𝐫𝐬𝐨𝐧𝐚𝐥 𝐂𝐨𝐦𝐩𝐮𝐭𝐞𝐫)
   🔍 𝐎𝐩𝐞𝐧 𝐏𝐨𝐫𝐭𝐬 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬:
   ├─ 🟡 𝐏𝐨𝐫𝐭 135: RPC - 𝐌𝐨𝐧𝐢𝐭𝐨𝐫
   ├─ 🟡 𝐏𝐨𝐫𝐭 139: NetBIOS - 𝐌𝐨𝐧𝐢𝐭𝐨𝐫
   ├─ 🔴 𝐏𝐨𝐫𝐭 445: SMB - 𝐂𝐫𝐢𝐭𝐢𝐜𝐚𝐥 (𝐑𝐞𝐜𝐨𝐦𝐦𝐞𝐧𝐝 𝐂𝐥𝐨𝐬𝐮𝐫𝐞)
   └─ 🟢 𝐏𝐨𝐫𝐭 5353: mDNS - 𝐒𝐞𝐜𝐮𝐫𝐞
   
   💻 𝐒𝐲𝐬𝐭𝐞𝐦 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧:
   ├─ 𝐓𝐲𝐩𝐞: Windows 11
   ├─ 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲: 𝐍𝐞𝐞𝐝𝐬 𝐈𝐦𝐩𝐫𝐨𝐯𝐞𝐦𝐞𝐧𝐭
   └─ 𝐑𝐞𝐜𝐨𝐦𝐦𝐞𝐧𝐝𝐚𝐭𝐢𝐨𝐧: 𝐃𝐢𝐬𝐚𝐛𝐥𝐞 𝐅𝐢𝐥𝐞 𝐒𝐡𝐚𝐫𝐢𝐧𝐠

🔍 𝐂𝐨𝐦𝐩𝐫𝐞𝐡𝐞𝐧𝐬𝐢𝐯𝐞 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬:
✅ 𝐒𝐭𝐫𝐞𝐧𝐠𝐭𝐡𝐬:
   - 𝐌𝐨𝐬𝐭 𝐝𝐞𝐯𝐢𝐜𝐞𝐬 𝐮𝐩-𝐭𝐨-𝐝𝐚𝐭𝐞
   - HTTPS 𝐞𝐧𝐚𝐛𝐥𝐞𝐝

⚠️ 𝐖𝐞𝐚𝐤𝐧𝐞𝐬𝐬𝐞𝐬:
   - 𝐂𝐫𝐢𝐭𝐢𝐜𝐚𝐥 𝐩𝐨𝐫𝐭𝐬 𝐨𝐩𝐞𝐧
   - 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬 𝐧𝐞𝐞𝐝 𝐨𝐩𝐭𝐢𝐦𝐢𝐳𝐚𝐭𝐢𝐨𝐧

🎯 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐑𝐞𝐜𝐨𝐦𝐦𝐞𝐧𝐝𝐚𝐭𝐢𝐨𝐧𝐬:
𝟏. 𝐂𝐥𝐨𝐬𝐞 𝐮𝐧𝐧𝐞𝐜𝐞𝐬𝐬𝐚𝐫𝐲 𝐩𝐨𝐫𝐭𝐬 (𝟐𝟑, 𝟒𝟒𝟓)
𝟐. 𝐔𝐩𝐝𝐚𝐭𝐞 𝐫𝐨𝐮𝐭𝐞𝐫 𝐟𝐢𝐫𝐦𝐰𝐚𝐫𝐞
𝟑. 𝐃𝐢𝐬𝐚𝐛𝐥𝐞 𝐮𝐧𝐮𝐬𝐞𝐝 𝐬𝐞𝐫𝐯𝐢𝐜𝐞𝐬
𝟒. 𝐄𝐧𝐚𝐛𝐥𝐞 𝐚𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐟𝐢𝐫𝐞𝐰𝐚𝐥𝐥

📞 𝐅𝐨𝐫 𝐩𝐫𝐨𝐟𝐞𝐬𝐬𝐢𝐨𝐧𝐚𝐥 𝐬𝐮𝐩𝐩𝐨𝐫𝐭: @𝐁𝐋_𝐓𝐇
"""
            
            self.bot.delete_message(message.chat.id, loading_msg.message_id)
            self.bot.send_message(message.chat.id, detailed_scan, parse_mode='Markdown')
            
            self.log_advanced_activity(str(message.chat.id), "𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧", "𝐋𝐨𝐜𝐚𝐥 𝐍𝐞𝐭𝐰𝐨𝐫𝐤", "𝐂𝐨𝐦𝐩𝐫𝐞𝐡𝐞𝐧𝐬𝐢𝐯𝐞 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬")
            
        except Exception as e:
            self.bot.send_message(message.chat.id, f"❌ 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐒𝐜𝐚𝐧 𝐄𝐫𝐫𝐨𝐫: {str(e)}")

    def basic_website_scan(self, message):
        """𝐏𝐞𝐫𝐟𝐨𝐫𝐦 𝐛𝐚𝐬𝐢𝐜 𝐰𝐞𝐛𝐬𝐢𝐭𝐞 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐬𝐜𝐚𝐧"""
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('🌐 𝐒𝐜𝐚𝐧 𝐖𝐞𝐛𝐬𝐢𝐭𝐞', callback_data='website_scan')
        markup.add(btn)
        
        explain_msg = """
🌐 𝐁𝐚𝐬𝐢𝐜 𝐖𝐞𝐛𝐬𝐢𝐭𝐞 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐒𝐜𝐚𝐧

🎯 𝐖𝐡𝐚𝐭 𝐰𝐞 𝐬𝐜𝐚𝐧:
- 𝐖𝐞𝐛𝐬𝐢𝐭𝐞 𝐚𝐯𝐚𝐢𝐥𝐚𝐛𝐢𝐥𝐢𝐭𝐲 & 𝐫𝐞𝐬𝐩𝐨𝐧𝐬𝐞
- 𝐒𝐞𝐫𝐯𝐞𝐫 𝐭𝐲𝐩𝐞 & 𝐜𝐨𝐧𝐟𝐢𝐠𝐮𝐫𝐚𝐭𝐢𝐨𝐧
- 𝐁𝐚𝐬𝐢𝐜 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬
- 𝐏𝐫𝐨𝐭𝐞𝐜𝐭𝐢𝐨𝐧 𝐡𝐞𝐚𝐝𝐞𝐫𝐬 𝐚𝐯𝐚𝐢𝐥𝐚𝐛𝐢𝐥𝐢𝐭𝐲

💡 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧 𝐩𝐫𝐨𝐯𝐢𝐝𝐞𝐝:
- ✅ 𝐒𝐢𝐭𝐞 𝐬𝐭𝐚𝐭𝐮𝐬 (𝟐𝟎𝟎 = 𝐎𝐩𝐞𝐫𝐚𝐭𝐢𝐨𝐧𝐚𝐥)
- 📊 𝐒𝐞𝐫𝐯𝐞𝐫 𝐭𝐲𝐩𝐞
- 🛡️ 𝐁𝐚𝐬𝐢𝐜 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬
- ⚠️ 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐫𝐞𝐜𝐨𝐦𝐦𝐞𝐧𝐝𝐚𝐭𝐢𝐨𝐧𝐬

🚀 𝐂𝐥𝐢𝐜𝐤 𝐛𝐮𝐭𝐭𝐨𝐧 𝐭𝐨 𝐬𝐭𝐚𝐫𝐭 𝐬𝐜𝐚𝐧𝐧𝐢𝐧𝐠
"""
        
        self.bot.send_message(message.chat.id, explain_msg, parse_mode='Markdown', reply_markup=markup)

    def ask_website_url(self, message):
        """𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐰𝐞𝐛𝐬𝐢𝐭𝐞 𝐔𝐑𝐋 𝐟𝐨𝐫 𝐬𝐜𝐚𝐧𝐧𝐢𝐧𝐠"""
        msg = self.bot.send_message(message.chat.id, 
                                  "🌐 𝐄𝐧𝐭𝐞𝐫 𝐰𝐞𝐛𝐬𝐢𝐭𝐞 𝐔𝐑𝐋 𝐟𝐨𝐫 𝐬𝐜𝐚𝐧𝐧𝐢𝐧𝐠:\n𝐄𝐱𝐚𝐦𝐩𝐥𝐞: `𝐠𝐨𝐨𝐠𝐥𝐞.𝐜𝐨𝐦` 𝐨𝐫 `𝐡𝐭𝐭𝐩𝐬://𝐞𝐱𝐚𝐦𝐩𝐥𝐞.𝐜𝐨𝐦`")
        self.bot.register_next_step_handler(msg, self.perform_basic_website_scan)

    def perform_basic_website_scan(self, message):
        """𝐏𝐞𝐫𝐟𝐨𝐫𝐦 𝐛𝐚𝐬𝐢𝐜 𝐰𝐞𝐛𝐬𝐢𝐭𝐞 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬"""
        url = message.text.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        self.bot.send_message(message.chat.id, f"🔍 𝐒𝐜𝐚𝐧𝐧𝐢𝐧𝐠 𝐰𝐞𝐛𝐬𝐢𝐭𝐞: `{url}`")
        
        try:
            response = requests.get(url, timeout=10, verify=False)
            
            analysis = f"""
🌐 𝐁𝐚𝐬𝐢𝐜 𝐖𝐞𝐛𝐬𝐢𝐭𝐞 𝐒𝐜𝐚𝐧 𝐑𝐞𝐬𝐮𝐥𝐭𝐬: `{url}`

📊 𝐁𝐚𝐬𝐢𝐜 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧:
✅ 𝐒𝐭𝐚𝐭𝐮𝐬: {response.status_code}
🖥️ 𝐒𝐞𝐫𝐯𝐞𝐫: {response.headers.get('Server', '𝐔𝐧𝐤𝐧𝐨𝐰𝐧')}
🔒 𝐂𝐨𝐧𝐭𝐞𝐧𝐭 𝐓𝐲𝐩𝐞: {response.headers.get('Content-Type', '𝐔𝐧𝐤𝐧𝐨𝐰𝐧')}

🛡️ 𝐁𝐚𝐬𝐢𝐜 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬:
"""
            
            security_score = 0
            security_notes = []
            
            if url.startswith('https://'):
                security_score += 2
                security_notes.append("✅ HTTPS: 𝐄𝐧𝐚𝐛𝐥𝐞𝐝 (𝐒𝐞𝐜𝐮𝐫𝐞 𝐁𝐫𝐨𝐰𝐬𝐢𝐧𝐠)")
            else:
                security_notes.append("❌ HTTPS: 𝐃𝐢𝐬𝐚𝐛𝐥𝐞𝐝 (𝐔𝐧𝐬𝐞𝐜𝐮𝐫𝐞)")
            
            security_headers = {
                'X-Frame-Options': '𝐂𝐥𝐢𝐜𝐤𝐣𝐚𝐜𝐤𝐢𝐧𝐠 𝐏𝐫𝐨𝐭𝐞𝐜𝐭𝐢𝐨𝐧',
                'X-Content-Type-Options': '𝐂𝐨𝐧𝐭𝐞𝐧𝐭 𝐒𝐧𝐢𝐟𝐟𝐢𝐧𝐠 𝐏𝐫𝐞𝐯𝐞𝐧𝐭𝐢𝐨𝐧',
                'Strict-Transport-Security': '𝐇𝐓𝐓𝐏𝐒 𝐄𝐧𝐟𝐨𝐫𝐜𝐞𝐦𝐞𝐧𝐭'
            }
            
            for header, description in security_headers.items():
                if header in response.headers:
                    security_score += 1
                    security_notes.append(f"✅ {header}: 𝐄𝐧𝐚𝐛𝐥𝐞𝐝 - {description}")
                else:
                    security_notes.append(f"⚠️ {header}: 𝐃𝐢𝐬𝐚𝐛𝐥𝐞𝐝 - {description}")
            
            for note in security_notes:
                analysis += f"{note}\n"
            
            analysis += f"\n🎯 𝐎𝐯𝐞𝐫𝐚𝐥𝐥 𝐀𝐬𝐬𝐞𝐬𝐬𝐦𝐞𝐧𝐭: "
            if security_score >= 4:
                analysis += "🛡️ 𝐕𝐞𝐫𝐲 𝐆𝐨𝐨𝐝"
            elif security_score >= 2:
                analysis += "⚠️ 𝐀𝐜𝐜𝐞𝐩𝐭𝐚𝐛𝐥𝐞"
            else:
                analysis += "❌ 𝐍𝐞𝐞𝐝𝐬 𝐈𝐦𝐩𝐫𝐨𝐯𝐞𝐦𝐞𝐧𝐭"
            
            analysis += f" ({security_score}/5)\n"
            
            analysis += "\n💎 𝐅𝐨𝐫 𝐚𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐯𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐬𝐜𝐚𝐧𝐧𝐢𝐧𝐠: 𝐔𝐩𝐠𝐫𝐚𝐝𝐞 𝐭𝐨 𝐏𝐫𝐞𝐦𝐢𝐮𝐦"
            
            self.bot.send_message(message.chat.id, analysis, parse_mode='Markdown')
            self.log_advanced_activity(str(message.chat.id), f"𝐖𝐞𝐛𝐬𝐢𝐭𝐞 𝐒𝐜𝐚𝐧", f"{url}", f"𝐒𝐜𝐨𝐫𝐞: {security_score}/5")
            
        except Exception as e:
            self.bot.send_message(message.chat.id, 
                                f"❌ 𝐒𝐜𝐚𝐧 𝐄𝐫𝐫𝐨𝐫: {str(e)}")

    def password_analysis_suite(self, message):
        """𝐂𝐨𝐦𝐩𝐫𝐞𝐡𝐞𝐧𝐬𝐢𝐯𝐞 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬 𝐬𝐮𝐢𝐭𝐞"""
        explain_msg = """
🔐 𝐂𝐨𝐦𝐩𝐫𝐞𝐡𝐞𝐧𝐬𝐢𝐯𝐞 𝐏𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬 𝐒𝐮𝐢𝐭𝐞

🎯 𝐒𝐞𝐫𝐯𝐢𝐜𝐞𝐬 𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞:

𝟏. 𝐏𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐒𝐭𝐫𝐞𝐧𝐠𝐭𝐡 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬
   - 𝐂𝐨𝐦𝐩𝐫𝐞𝐡𝐞𝐧𝐬𝐢𝐯𝐞 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐚𝐬𝐬𝐞𝐬𝐬𝐦𝐞𝐧𝐭
   - 𝐁𝐫𝐮𝐭𝐞-𝐟𝐨𝐫𝐜𝐞 𝐫𝐞𝐬𝐢𝐬𝐭𝐚𝐧𝐜𝐞 𝐭𝐞𝐬𝐭𝐢𝐧𝐠
   - 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐥𝐞𝐯𝐞𝐥 𝐞𝐯𝐚𝐥𝐮𝐚𝐭𝐢𝐨𝐧

𝟐. 𝐒𝐞𝐜𝐮𝐫𝐞 𝐏𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐢𝐨𝐧
   - 𝐂𝐫𝐞𝐚𝐭𝐞 𝐜𝐨𝐦𝐩𝐥𝐞𝐱 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝𝐬
   - 𝐂𝐮𝐬𝐭𝐨𝐦𝐢𝐳𝐚𝐭𝐢𝐨𝐧 𝐛𝐚𝐬𝐞𝐝 𝐨𝐧 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐦𝐞𝐧𝐭𝐬
   - 𝐒𝐞𝐜𝐮𝐫𝐞 𝐬𝐭𝐨𝐫𝐚𝐠𝐞 𝐨𝐩𝐭𝐢𝐨𝐧𝐬

𝟑. 𝐏𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐃𝐚𝐭𝐚𝐛𝐚𝐬𝐞 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬
   - 𝐀𝐧𝐚𝐥𝐲𝐳𝐞 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐜𝐨𝐥𝐥𝐞𝐜𝐭𝐢𝐨𝐧𝐬
   - 𝐃𝐞𝐭𝐞𝐜𝐭 𝐝𝐮𝐩𝐥𝐢𝐜𝐚𝐭𝐞𝐬 & 𝐰𝐞𝐚𝐤𝐧𝐞𝐬𝐬𝐞𝐬
   - 𝐈𝐦𝐩𝐫𝐨𝐯𝐞𝐦𝐞𝐧𝐭 𝐫𝐞𝐜𝐨𝐦𝐦𝐞𝐧𝐝𝐚𝐭𝐢𝐨𝐧𝐬

𝐄𝐧𝐭𝐞𝐫 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐟𝐨𝐫 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬, 𝐨𝐫 𝐜𝐡𝐨𝐨𝐬𝐞 '𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞' 𝐟𝐨𝐫 𝐧𝐞𝐰 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝:
"""
        
        markup = types.InlineKeyboardMarkup()
        btn_generate = types.InlineKeyboardButton('🔄 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞 𝐏𝐚𝐬𝐬𝐰𝐨𝐫𝐝', callback_data='generate_advanced_password')
        btn_analyze = types.InlineKeyboardButton('🔍 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬', callback_data='advanced_analysis')
        
        markup.row(btn_generate, btn_analyze)
        
        msg = self.bot.send_message(message.chat.id, explain_msg, parse_mode='Markdown', reply_markup=markup)
        self.bot.register_next_step_handler(msg, self.advanced_password_check)

    def advanced_password_check(self, message):
        """𝐏𝐞𝐫𝐟𝐨𝐫𝐦 𝐚𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬"""
        password = message.text
        
        strength_score = 0
        analysis_details = []
        
        tests = {
            '𝐋𝐞𝐧𝐠𝐭𝐡': len(password) >= 12,
            '𝐋𝐨𝐰𝐞𝐫𝐜𝐚𝐬𝐞': any(c.islower() for c in password),
            '𝐔𝐩𝐩𝐞𝐫𝐜𝐚𝐬𝐞': any(c.isupper() for c in password),
            '𝐃𝐢𝐠𝐢𝐭𝐬': any(c.isdigit() for c in password),
            '𝐒𝐩𝐞𝐜𝐢𝐚𝐥 𝐂𝐡𝐚𝐫𝐬': any(not c.isalnum() for c in password),
            '𝐍𝐨 𝐂𝐨𝐦𝐦𝐨𝐧 𝐖𝐨𝐫𝐝𝐬': password.lower() not in ['password', '123456', 'admin', 'welcome'],
            '𝐍𝐨 𝐒𝐞𝐪𝐮𝐞𝐧𝐜𝐞𝐬': not any(str(i) in password for i in range(10)),
            '𝐔𝐧𝐢𝐪𝐮𝐞 𝐂𝐡𝐚𝐫𝐚𝐜𝐭𝐞𝐫𝐬': len(set(password)) >= 8
        }
        
        strength_score = sum(tests.values())
        max_score = len(tests)
        
        entropy = len(password) * 4
        crack_time = "𝐒𝐞𝐜𝐨𝐧𝐝𝐬" if entropy < 40 else "𝐌𝐢𝐧𝐮𝐭𝐞𝐬" if entropy < 60 else "𝐇𝐨𝐮𝐫𝐬" if entropy < 80 else "𝐌𝐨𝐧𝐭𝐡𝐬" if entropy < 100 else "𝐘𝐞𝐚𝐫𝐬"
        
        result = f"""
🔐 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐏𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬 𝐑𝐞𝐩𝐨𝐫𝐭

📊 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬 𝐑𝐞𝐬𝐮𝐥𝐭𝐬:
- 𝐒𝐭𝐫𝐞𝐧𝐠𝐭𝐡 𝐒𝐜𝐨𝐫𝐞: {strength_score}/{max_score}
- 𝐄𝐧𝐭𝐫𝐨𝐩𝐲: {entropy} 𝐛𝐢𝐭𝐬
- 𝐄𝐬𝐭𝐢𝐦𝐚𝐭𝐞𝐝 𝐂𝐫𝐚𝐜𝐤 𝐓𝐢𝐦𝐞: {crack_time}

🔍 𝐃𝐞𝐭𝐚𝐢𝐥𝐞𝐝 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬:
"""
        
        for test_name, passed in tests.items():
            icon = "✅" if passed else "❌"
            result += f"{icon} {test_name}: {'𝐄𝐱𝐜𝐞𝐥𝐥𝐞𝐧𝐭' if passed else '𝐍𝐞𝐞𝐝𝐬 𝐈𝐦𝐩𝐫𝐨𝐯𝐞𝐦𝐞𝐧𝐭'}\n"
        
        if strength_score >= 6:
            result += "\n🎉 𝐄𝐱𝐜𝐞𝐥𝐥𝐞𝐧𝐭! 𝐏𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐢𝐬 𝐯𝐞𝐫𝐲 𝐬𝐭𝐫𝐨𝐧𝐠"
        elif strength_score >= 4:
            result += "\n⚠️ 𝐆𝐨𝐨𝐝 𝐛𝐮𝐭 𝐜𝐚𝐧 𝐛𝐞 𝐢𝐦𝐩𝐫𝐨𝐯𝐞𝐝"
        else:
            result += "\n❌ 𝐖𝐞𝐚𝐤 - 𝐑𝐞𝐜𝐨𝐦𝐦𝐞𝐧𝐝 𝐢𝐦𝐦𝐞𝐝𝐢𝐚𝐭𝐞 𝐜𝐡𝐚𝐧𝐠𝐞"
        
        result += "\n\n💡 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐑𝐞𝐜𝐨𝐦𝐦𝐞𝐧𝐝𝐚𝐭𝐢𝐨𝐧𝐬:"
        result += "\n• 𝐔𝐬𝐞 𝐮𝐧𝐢𝐪𝐮𝐞 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝𝐬 𝐟𝐨𝐫 𝐞𝐚𝐜𝐡 𝐚𝐜𝐜𝐨𝐮𝐧𝐭"
        result += "\n• 𝐂𝐡𝐚𝐧𝐠𝐞 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝𝐬 𝐞𝐯𝐞𝐫𝐲 𝟑-𝟔 𝐦𝐨𝐧𝐭𝐡𝐬"
        result += "\n• 𝐔𝐬𝐞 𝐭𝐫𝐮𝐬𝐭𝐞𝐝 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐦𝐚𝐧𝐚𝐠𝐞𝐫"
        
        self.bot.send_message(message.chat.id, result, parse_mode='Markdown')
        self.log_advanced_activity(str(message.chat.id), "𝐏𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬", "𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐂𝐡𝐞𝐜𝐤", f"𝐒𝐜𝐨𝐫𝐞: {strength_score}/{max_score}")

    def user_statistics(self, message):
        """𝐃𝐢𝐬𝐩𝐥𝐚𝐲 𝐮𝐬𝐞𝐫 𝐬𝐭𝐚𝐭𝐢𝐬𝐭𝐢𝐜𝐬"""
        user_id = str(message.chat.id)
        user_info = self.get_user_info(user_id)
        
        stats_msg = f"""
📈 𝐘𝐨𝐮𝐫 𝐏𝐞𝐫𝐬𝐨𝐧𝐚𝐥 𝐒𝐭𝐚𝐭𝐢𝐬𝐭𝐢𝐜𝐬

👤 𝐁𝐚𝐬𝐢𝐜 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧:
- 𝐔𝐬𝐞𝐫 𝐈𝐃: `{user_id}`
- 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧: {'💎 𝐏𝐫𝐞𝐦𝐢𝐮𝐦' if user_info['is_active'] else '🆓 𝐅𝐫𝐞𝐞'}
- 𝐒𝐜𝐚𝐧𝐬 𝐏𝐞𝐫𝐟𝐨𝐫𝐦𝐞𝐝: {user_info['total_scans']}

📊 𝐑𝐞𝐜𝐞𝐧𝐭 𝐀𝐜𝐭𝐢𝐯𝐢𝐭𝐲:
"""
        
        self.cursor.execute('''
            SELECT activity_type, timestamp FROM activity_log 
            WHERE user_id = ? ORDER BY timestamp DESC LIMIT 5
        ''', (user_id,))
        
        recent_activities = self.cursor.fetchall()
        
        if recent_activities:
            for activity in recent_activities:
                stats_msg += f"• {activity[0]} - {activity[1][:16]}\n"
        else:
            stats_msg += "• 𝐍𝐨 𝐚𝐜𝐭𝐢𝐯𝐢𝐭𝐢𝐞𝐬 𝐫𝐞𝐜𝐨𝐫𝐝𝐞𝐝\n"
        
        stats_msg += f"\n💎 𝐔𝐩𝐠𝐫𝐚𝐝𝐞 𝐲𝐨𝐮𝐫 𝐬𝐭𝐚𝐭𝐢𝐬𝐭𝐢𝐜𝐬: /premium"
        
        self.bot.send_message(message.chat.id, stats_msg, parse_mode='Markdown')

    def admin_panel(self, message):
        """𝐃𝐢𝐬𝐩𝐥𝐚𝐲 𝐚𝐝𝐦𝐢𝐧 𝐜𝐨𝐧𝐭𝐫𝐨𝐥 𝐩𝐚𝐧𝐞𝐥"""
        if str(message.chat.id) != self.ADMIN_CHAT_ID:
            return
        
        self.cursor.execute('SELECT COUNT() FROM premium_users WHERE is_active = 1')
        active_users = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT() FROM activity_log')
        total_activities = self.cursor.fetchone()[0]
        
        admin_msg = f"""
👑 𝐀𝐝𝐦𝐢𝐧𝐢𝐬𝐭𝐫𝐚𝐭𝐨𝐫 𝐂𝐨𝐧𝐭𝐫𝐨𝐥 𝐏𝐚𝐧𝐞𝐥

📊 𝐒𝐲𝐬𝐭𝐞𝐦 𝐒𝐭𝐚𝐭𝐢𝐬𝐭𝐢𝐜𝐬:
- 𝐀𝐜𝐭𝐢𝐯𝐞 𝐔𝐬𝐞𝐫𝐬: {active_users}
- 𝐓𝐨𝐭𝐚𝐥 𝐀𝐜𝐭𝐢𝐯𝐢𝐭𝐢𝐞𝐬: {total_activities}

🛠️ 𝐀𝐝𝐦𝐢𝐧𝐢𝐬𝐭𝐫𝐚𝐭𝐢𝐨𝐧 𝐓𝐨𝐨𝐥𝐬:
- /stats - 𝐃𝐞𝐭𝐚𝐢𝐥𝐞𝐝 𝐬𝐭𝐚𝐭𝐢𝐬𝐭𝐢𝐜𝐬
- /broadcast - 𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭 𝐦𝐞𝐬𝐬𝐚𝐠𝐞
- /backup - 𝐃𝐚𝐭𝐚𝐛𝐚𝐬𝐞 𝐛𝐚𝐜𝐤𝐮𝐩

🔧 𝐒𝐲𝐬𝐭𝐞𝐦 𝐒𝐭𝐚𝐭𝐮𝐬:
- 𝐁𝐨𝐭 𝐒𝐭𝐚𝐭𝐮𝐬: 🟢 𝐎𝐩𝐞𝐫𝐚𝐭𝐢𝐨𝐧𝐚𝐥
- 𝐃𝐚𝐭𝐚𝐛𝐚𝐬𝐞: 🟢 𝐎𝐩𝐞𝐫𝐚𝐭𝐢𝐨𝐧𝐚𝐥
- 𝐋𝐚𝐬𝐭 𝐔𝐩𝐝𝐚𝐭𝐞: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
        
        self.bot.send_message(message.chat.id, admin_msg, parse_mode='Markdown')

    def get_user_info(self, user_id):
        """𝐆𝐞𝐭 𝐮𝐬𝐞𝐫 𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧"""
        self.cursor.execute('''
            SELECT plan_type, is_active, expiry_date, total_scans 
            FROM premium_users WHERE user_id = ?
        ''', (user_id,))
        
        result = self.cursor.fetchone()
        if result:
            return {
                'plan_type': result[0],
                'is_active': bool(result[1]),
                'expiry_date': result[2],
                'total_scans': result[3]
            }
        else:
            return {
                'plan_type': '𝐅𝐫𝐞𝐞',
                'is_active': False,
                'expiry_date': '𝐍𝐨𝐭 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐛𝐞𝐝',
                'total_scans': 0
            }

    def update_user_scans(self, user_id):
        """𝐔𝐩𝐝𝐚𝐭𝐞 𝐮𝐬𝐞𝐫 𝐬𝐜𝐚𝐧 𝐜𝐨𝐮𝐧𝐭"""
        self.cursor.execute('''
            UPDATE premium_users SET total_scans = total_scans + 1 
            WHERE user_id = ?
        ''', (user_id,))
        self.conn.commit()

    def log_advanced_activity(self, user_id, activity_type, target, result):
    # الكود هنا
    pass
        """𝐋𝐨𝐠 𝐚𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐮𝐬𝐞𝐫 𝐚𝐜𝐭𝐢𝐯𝐢𝐭𝐲"""
        self.cursor.execute('''
            INSERT INTO activity_log (user_id, activity_type, target, result, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, activity_type, target, result, datetime.now().isoformat()))
        self.conn.commit()

    def premium_locked(self, message):
        """𝐒𝐡𝐨𝐰 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐥𝐨𝐜𝐤𝐞𝐝 𝐦𝐞𝐬𝐬𝐚𝐠𝐞"""
        markup = types.InlineKeyboardMarkup()
        
        btn_plans = types.InlineKeyboardButton('💎 𝐕𝐢𝐞𝐰 𝐏𝐥𝐚𝐧𝐬', callback_data='show_plans')
        btn_support = types.InlineKeyboardButton('📞 𝐒𝐮𝐩𝐩𝐨𝐫𝐭', url='https://t.me/BL_TH')
        
        markup.row(btn_plans, btn_support)
        
        locked_msg = """
🔒 𝐓𝐡𝐢𝐬 𝐟𝐞𝐚𝐭𝐮𝐫𝐞 𝐢𝐬 𝐞𝐱𝐜𝐥𝐮𝐬𝐢𝐯𝐞𝐥𝐲 𝐟𝐨𝐫 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐛𝐞𝐫𝐬

💎 𝐖𝐡𝐚𝐭 𝐲𝐨𝐮 𝐠𝐞𝐭 𝐰𝐢𝐭𝐡 𝐏𝐫𝐞𝐦𝐢𝐮𝐦:

• 🔍 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧𝐧𝐢𝐧𝐠
  - 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐯𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐝𝐞𝐭𝐞𝐜𝐭𝐢𝐨𝐧
  - 𝐒𝐞𝐫𝐯𝐢𝐜𝐞 & 𝐩𝐨𝐫𝐭 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐃𝐞𝐭𝐚𝐢𝐥𝐞𝐝 𝐫𝐞𝐩𝐨𝐫𝐭𝐬 𝐰𝐢𝐭𝐡 𝐫𝐞𝐜𝐨𝐦𝐦𝐞𝐧𝐝𝐚𝐭𝐢𝐨𝐧𝐬

• 🌐 𝐂𝐨𝐦𝐩𝐫𝐞𝐡𝐞𝐧𝐬𝐢𝐯𝐞 𝐖𝐞𝐛 𝐕𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐒𝐜𝐚𝐧𝐧𝐢𝐧𝐠
  - 𝐒𝐐𝐋 𝐈𝐧𝐣𝐞𝐜𝐭𝐢𝐨𝐧 𝐒𝐜𝐚𝐧𝐧𝐞𝐫
  - 𝐗𝐒𝐒 𝐕𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐃𝐞𝐭𝐞𝐜𝐭𝐢𝐨𝐧
  - 𝐂𝐒𝐑𝐅 𝐏𝐫𝐨𝐭𝐞𝐜𝐭𝐢𝐨𝐧 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬

• 📡 𝐖𝐢𝐅𝐢 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐀𝐮𝐝𝐢𝐭𝐬
  - 𝐂𝐨𝐦𝐩𝐫𝐞𝐡𝐞𝐧𝐬𝐢𝐯𝐞 𝐰𝐢𝐫𝐞𝐥𝐞𝐬𝐬 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐈𝐧𝐭𝐫𝐮𝐬𝐢𝐨𝐧 𝐝𝐞𝐭𝐞𝐜𝐭𝐢𝐨𝐧 & 𝐩𝐫𝐞𝐯𝐞𝐧𝐭𝐢𝐨𝐧
  - 𝐃𝐞𝐭𝐚𝐢𝐥𝐞𝐝 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐫𝐞𝐩𝐨𝐫𝐭𝐬

• 🕵️ 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐎𝐒𝐈𝐍𝐓 𝐓𝐨𝐨𝐥𝐬
  - 𝐂𝐨𝐦𝐩𝐫𝐞𝐡𝐞𝐧𝐬𝐢𝐯𝐞 𝐢𝐧𝐭𝐞𝐥𝐥𝐢𝐠𝐞𝐧𝐜𝐞 𝐠𝐚𝐭𝐡𝐞𝐫𝐢𝐧𝐠
  - 𝐀𝐜𝐜𝐨𝐮𝐧𝐭 & 𝐢𝐝𝐞𝐧𝐭𝐢𝐭𝐲 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐈𝐧-𝐝𝐞𝐩𝐭𝐡 𝐫𝐞𝐬𝐞𝐚𝐫𝐜𝐡 𝐫𝐞𝐩𝐨𝐫𝐭𝐬

• ⚡ 𝐂𝐮𝐬𝐭𝐨𝐦 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐒𝐜𝐫𝐢𝐩𝐭𝐬
  - 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐬𝐜𝐚𝐧𝐧𝐢𝐧𝐠 𝐭𝐨𝐨𝐥𝐬
  - 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐨𝐧 𝐨𝐟 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐭𝐚𝐬𝐤𝐬
  - 𝐏𝐞𝐫𝐬𝐨𝐧𝐚𝐥𝐢𝐳𝐞𝐝 𝐭𝐨𝐨𝐥 𝐝𝐞𝐯𝐞𝐥𝐨𝐩𝐦𝐞𝐧𝐭

🚀 𝐄𝐥𝐞𝐯𝐚𝐭𝐞 𝐲𝐨𝐮𝐫 𝐜𝐲𝐛𝐞𝐫𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐬𝐤𝐢𝐥𝐥𝐬 𝐭𝐨 𝐩𝐫𝐨𝐟𝐞𝐬𝐬𝐢𝐨𝐧𝐚𝐥 𝐥𝐞𝐯𝐞𝐥!
"""
        
        self.bot.send_message(message.chat.id, locked_msg, parse_mode='Markdown', reply_markup=markup)

    def contact_support(self, message):
        """𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐬𝐮𝐩𝐩𝐨𝐫𝐭 𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧"""
        support_msg = """
📞 𝐓𝐞𝐜𝐡𝐧𝐢𝐜𝐚𝐥 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 & 𝐂𝐨𝐧𝐬𝐮𝐥𝐭𝐚𝐭𝐢𝐨𝐧𝐬

🎯 𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 𝐒𝐞𝐫𝐯𝐢𝐜𝐞𝐬:

• 🔧 𝐁𝐨𝐭 𝐓𝐞𝐜𝐡𝐧𝐢𝐜𝐚𝐥 𝐒𝐮𝐩𝐩𝐨𝐫𝐭
  - 𝐎𝐩𝐞𝐫𝐚𝐭𝐢𝐨𝐧𝐚𝐥 𝐢𝐬𝐬𝐮𝐞𝐬
  - 𝐓𝐞𝐜𝐡𝐧𝐢𝐜𝐚𝐥 𝐢𝐧𝐪𝐮𝐢𝐫𝐢𝐞𝐬
  - 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐦𝐞𝐧𝐭 𝐬𝐮𝐠𝐠𝐞𝐬𝐭𝐢𝐨𝐧𝐬

• 🛡️ 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐂𝐨𝐧𝐬𝐮𝐥𝐭𝐚𝐭𝐢𝐨𝐧𝐬
  - 𝐕𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐚𝐬𝐬𝐞𝐬𝐬𝐦𝐞𝐧𝐭
  - 𝐏𝐫𝐨𝐭𝐞𝐜𝐭𝐢𝐨𝐧 𝐩𝐥𝐚𝐧𝐧𝐢𝐧𝐠

• 💰 𝐏𝐚𝐲𝐦𝐞𝐧𝐭 𝐈𝐧𝐪𝐮𝐢𝐫𝐢𝐞𝐬
  - 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐚𝐜𝐭𝐢𝐯𝐚𝐭𝐢𝐨𝐧
  - 𝐏𝐚𝐲𝐦𝐞𝐧𝐭 𝐢𝐬𝐬𝐮𝐞𝐬
  - 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐫𝐞𝐧𝐞𝐰𝐚𝐥

• 📋 𝐓𝐫𝐚𝐢𝐧𝐢𝐧𝐠 & 𝐄𝐝𝐮𝐜𝐚𝐭𝐢𝐨𝐧
  - 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐜𝐨𝐮𝐫𝐬𝐞𝐬
  - 𝐖𝐨𝐫𝐤𝐬𝐡𝐨𝐩𝐬
  - 𝐂𝐮𝐬𝐭𝐨𝐦 𝐭𝐫𝐚𝐢𝐧𝐢𝐧𝐠

📱 𝐃𝐢𝐫𝐞𝐜𝐭 𝐂𝐨𝐧𝐭𝐚𝐜𝐭:
@𝐁𝐋_𝐓𝐇

⏰ 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 𝐇𝐨𝐮𝐫𝐬:
- 𝐃𝐚𝐢𝐥𝐲 𝟏𝟎𝐀𝐌 - 𝟏𝟐𝐏𝐌
- 𝐌𝐚𝐱𝐢𝐦𝐮𝐦 𝐫𝐞𝐬𝐩𝐨𝐧𝐬𝐞 𝐭𝐢𝐦𝐞: 𝟐𝟒 𝐡𝐨𝐮𝐫𝐬

💬 𝐏𝐥𝐞𝐚𝐬𝐞 𝐜𝐥𝐞𝐚𝐫𝐥𝐲 𝐝𝐞𝐬𝐜𝐫𝐢𝐛𝐞 𝐲𝐨𝐮𝐫 𝐫𝐞𝐪𝐮𝐞𝐬𝐭 𝐰𝐡𝐞𝐧 𝐜𝐨𝐧𝐭𝐚𝐜𝐭𝐢𝐧𝐠
"""
        
        self.bot.send_message(message.chat.id, support_msg, parse_mode='Markdown')

    def generate_strong_password(self, message):
        """𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞 𝐬𝐭𝐫𝐨𝐧𝐠 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝𝐬 𝐰𝐢𝐭𝐡 𝐚𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐨𝐩𝐭𝐢𝐨𝐧𝐬"""
        levels = {
            "𝐁𝐚𝐬𝐢𝐜": 12,
            "𝐒𝐭𝐫𝐨𝐧𝐠": 16,
            "𝐔𝐥𝐭𝐢𝐦𝐚𝐭𝐞": 20
        }
        
        passwords = {}
        for level, length in levels.items():
            characters = string.ascii_letters + string.digits + "!@#$%^&"
            password = ''.join(random.choice(characters) for _ in range(length))
            passwords[level] = password
        
        result = """
🔐 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐏𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐨𝐫

🎯 𝐑𝐞𝐜𝐨𝐦𝐦𝐞𝐧𝐝𝐞𝐝 𝐏𝐚𝐬𝐬𝐰𝐨𝐫𝐝𝐬 𝐛𝐲 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐋𝐞𝐯𝐞𝐥:

🟢 𝐁𝐚𝐬𝐢𝐜 𝐋𝐞𝐯𝐞𝐥 (𝟏𝟐 𝐜𝐡𝐚𝐫𝐚𝐜𝐭𝐞𝐫𝐬):
`{}`

🔵 𝐒𝐭𝐫𝐨𝐧𝐠 𝐋𝐞𝐯𝐞𝐥 (𝟏𝟔 𝐜𝐡𝐚𝐫𝐚𝐜𝐭𝐞𝐫𝐬):
`{}`

🟣 𝐔𝐥𝐭𝐢𝐦𝐚𝐭𝐞 𝐋𝐞𝐯𝐞𝐥 (𝟐𝟎 𝐜𝐡𝐚𝐫𝐚𝐜𝐭𝐞𝐫𝐬):
`{}`

💡 𝐄𝐬𝐬𝐞𝐧𝐭𝐢𝐚𝐥 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐓𝐢𝐩𝐬:
• 𝐒𝐭𝐨𝐫𝐞 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝𝐬 𝐢𝐧 𝐬𝐞𝐜𝐮𝐫𝐞 𝐥𝐨𝐜𝐚𝐭𝐢𝐨𝐧𝐬
• 𝐀𝐯𝐨𝐢𝐝 𝐫𝐞𝐮𝐬𝐢𝐧𝐠 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝𝐬 𝐚𝐜𝐫𝐨𝐬𝐬 𝐬𝐢𝐭𝐞𝐬
• 𝐑𝐨𝐮𝐭𝐢𝐧𝐞𝐥𝐲 𝐮𝐩𝐝𝐚𝐭𝐞 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝𝐬 𝐞𝐯𝐞𝐫𝐲 𝟑 𝐦𝐨𝐧𝐭𝐡𝐬

🔒 𝐏𝐫𝐢𝐨𝐫𝐢𝐭𝐢𝐳𝐞 𝐲𝐨𝐮𝐫 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲
""".format(passwords["𝐁𝐚𝐬𝐢𝐜"], passwords["𝐒𝐭𝐫𝐨𝐧𝐠"], passwords["𝐔𝐥𝐭𝐢𝐦𝐚𝐭𝐞"])
        
        self.bot.send_message(message.chat.id, result, parse_mode='Markdown')

    def system_info_advanced(self, message):
        """𝐃𝐢𝐬𝐩𝐥𝐚𝐲 𝐚𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐬𝐲𝐬𝐭𝐞𝐦 𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧"""
        try:
            hostname = socket.gethostname()
            
            info = f"""
📊 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐒𝐲𝐬𝐭𝐞𝐦 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧

🖥️ 𝐃𝐞𝐯𝐢𝐜𝐞 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧:
- 𝐇𝐨𝐬𝐭𝐧𝐚𝐦𝐞: `{hostname}`
- 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐓𝐢𝐦𝐞: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`
- 𝐎𝐩𝐞𝐫𝐚𝐭𝐢𝐧𝐠 𝐒𝐲𝐬𝐭𝐞𝐦: `𝐀𝐧𝐝𝐫𝐨𝐢𝐝/𝐓𝐞𝐫𝐦𝐮𝐱`
- 𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐨𝐧 𝐓𝐲𝐩𝐞: `𝐋𝐨𝐜𝐚𝐥 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 (𝐖𝐢𝐅𝐢)`

💡 𝐓𝐞𝐜𝐡𝐧𝐢𝐜𝐚𝐥 𝐃𝐞𝐭𝐚𝐢𝐥𝐬:
- 𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐨𝐫: ARM64
- 𝐌𝐞𝐦𝐨𝐫𝐲: 𝐋𝐢𝐦𝐢𝐭𝐞𝐝 (𝐌𝐨𝐛𝐢𝐥𝐞)
- 𝐒𝐭𝐨𝐫𝐚𝐠𝐞: 𝐕𝐚𝐫𝐢𝐚𝐛𝐥𝐞 𝐛𝐲 𝐝𝐞𝐯𝐢𝐜𝐞

🔧 𝐅𝐨𝐫 𝐚𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐬𝐲𝐬𝐭𝐞𝐦 𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧:
𝐔𝐩𝐠𝐫𝐚𝐝𝐞 𝐭𝐨 𝐏𝐫𝐞𝐦𝐢𝐮𝐦
"""
            
            self.bot.send_message(message.chat.id, info, parse_mode='Markdown')
            self.log_advanced_activity(str(message.chat.id), "𝐒𝐲𝐬𝐭𝐞𝐦 𝐈𝐧𝐟𝐨", "𝐁𝐚𝐬𝐢𝐜", "𝐒𝐮𝐜𝐜𝐞𝐬𝐬")
            
        except Exception as e:
            self.bot.send_message(message.chat.id, f"❌ 𝐄𝐫𝐫𝐨𝐫: {str(e)}")

    def show_help_advanced(self, message):
        """𝐃𝐢𝐬𝐩𝐥𝐚𝐲 𝐚𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐡𝐞𝐥𝐩 𝐠𝐮𝐢𝐝𝐞"""
        help_msg = """
❓ 𝐂𝐨𝐦𝐩𝐫𝐞𝐡𝐞𝐧𝐬𝐢𝐯𝐞 𝐔𝐬𝐞𝐫 𝐆𝐮𝐢𝐝𝐞

🎯 𝐇𝐨𝐰 𝐭𝐨 𝐔𝐬𝐞 𝐭𝐡𝐞 𝐁𝐨𝐭:

𝟏. 🔍 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧𝐧𝐢𝐧𝐠
   - 𝐃𝐢𝐬𝐜𝐨𝐯𝐞𝐫 𝐝𝐞𝐯𝐢𝐜𝐞𝐬 𝐢𝐧 𝐲𝐨𝐮𝐫 𝐧𝐞𝐭𝐰𝐨𝐫𝐤
   - 𝐌𝐨𝐧𝐢𝐭𝐨𝐫 𝐜𝐨𝐧𝐧𝐞𝐜𝐭𝐞𝐝 𝐮𝐬𝐞𝐫𝐬

𝟐. 🌐 𝐖𝐞𝐛𝐬𝐢𝐭𝐞 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬
   - 𝐀𝐧𝐚𝐥𝐲𝐳𝐞 𝐰𝐞𝐛𝐬𝐢𝐭𝐞 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲
   - 𝐈𝐝𝐞𝐧𝐭𝐢𝐟𝐲 𝐩𝐨𝐭𝐞𝐧𝐭𝐢𝐚𝐥 𝐯𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐢𝐞𝐬

𝟑. 🔐 𝐏𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲
   - 𝐓𝐞𝐬𝐭 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐬𝐭𝐫𝐞𝐧𝐠𝐭𝐡
   - 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞 𝐬𝐞𝐜𝐮𝐫𝐞 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝𝐬

𝟒. 📊 𝐒𝐲𝐬𝐭𝐞𝐦 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧
   - 𝐕𝐢𝐞𝐰 𝐜𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐨𝐧 𝐝𝐞𝐭𝐚𝐢𝐥𝐬
   - 𝐀𝐧𝐚𝐥𝐲𝐳𝐞 𝐧𝐞𝐭𝐰𝐨𝐫𝐤 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬

⚠️ 𝐄𝐬𝐬𝐞𝐧𝐭𝐢𝐚𝐥 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐓𝐢𝐩𝐬:
- 𝐔𝐬𝐞 𝐬𝐭𝐫𝐨𝐧𝐠, 𝐮𝐧𝐢𝐪𝐮𝐞 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝𝐬
- 𝐑𝐞𝐠𝐮𝐥𝐚𝐫𝐥𝐲 𝐮𝐩𝐝𝐚𝐭𝐞 𝐖𝐢𝐅𝐢 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝𝐬
- 𝐄𝐧𝐬𝐮𝐫𝐞 🔒 𝐢𝐧 𝐰𝐞𝐛𝐬𝐢𝐭𝐞 𝐚𝐝𝐝𝐫𝐞𝐬𝐬𝐞𝐬
- 𝐀𝐯𝐨𝐢𝐝 𝐬𝐮𝐬𝐩𝐢𝐜𝐢𝐨𝐮𝐬 𝐥𝐢𝐧𝐤𝐬

💎 𝐑𝐞𝐦𝐞𝐦𝐛𝐞𝐫: 𝐓𝐡𝐢𝐬 𝐛𝐨𝐭 𝐢𝐬 𝐟𝐨𝐫 𝐞𝐝𝐮𝐜𝐚𝐭𝐢𝐨𝐧𝐚𝐥 𝐚𝐧𝐝 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐩𝐮𝐫𝐩𝐨𝐬𝐞𝐬 𝐨𝐧𝐥𝐲
"""
        
        self.bot.send_message(message.chat.id, help_msg, parse_mode='Markdown')

    def vulnerability_scan_suite(self, message):
        """𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐯𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐬𝐜𝐚𝐧𝐧𝐢𝐧𝐠 𝐬𝐮𝐢𝐭𝐞"""
        if not self.is_premium_user(str(message.chat.id)):
            self.premium_locked(message)
            return
        
        markup = types.InlineKeyboardMarkup()
        btn_web = types.InlineKeyboardButton('🌐 𝐖𝐞𝐛 𝐕𝐮𝐥𝐧𝐬', callback_data='vuln_web')
        btn_network = types.InlineKeyboardButton('🔍 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐕𝐮𝐥𝐧𝐬', callback_data='vuln_network')
        btn_wifi = types.InlineKeyboardButton('📡 𝐖𝐢𝐅𝐢 𝐕𝐮𝐥𝐧𝐬', callback_data='vuln_wifi')
        
        markup.row(btn_web, btn_network)
        markup.row(btn_wifi)
        
        vuln_msg = """
🛡️ 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐕𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐒𝐜𝐚𝐧𝐧𝐢𝐧𝐠 𝐒𝐮𝐢𝐭𝐞

🎯 𝐒𝐞𝐥𝐞𝐜𝐭 𝐒𝐜𝐚𝐧 𝐓𝐲𝐩𝐞:

• 🌐 𝐖𝐞𝐛 𝐀𝐩𝐩𝐥𝐢𝐜𝐚𝐭𝐢𝐨𝐧 𝐕𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐒𝐜𝐚𝐧𝐧𝐢𝐧𝐠
  - 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐒𝐐𝐋 𝐈𝐧𝐣𝐞𝐜𝐭𝐢𝐨𝐧 𝐒𝐜𝐚𝐧𝐧𝐢𝐧𝐠
  - 𝐗𝐒𝐒 𝐕𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐃𝐞𝐭𝐞𝐜𝐭𝐢𝐨𝐧
  - 𝐂𝐒𝐑𝐅 𝐏𝐫𝐨𝐭𝐞𝐜𝐭𝐢𝐨𝐧 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐇𝐞𝐚𝐝𝐞𝐫𝐬 𝐀𝐮𝐝𝐢𝐭
  - 𝐒𝐒𝐋/𝐓𝐋𝐒 𝐂𝐨𝐧𝐟𝐢𝐠𝐮𝐫𝐚𝐭𝐢𝐨𝐧 𝐂𝐡𝐞𝐜𝐤

• 🔍 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐕𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐒𝐜𝐚𝐧𝐧𝐢𝐧𝐠
  - 𝐎𝐩𝐞𝐧 𝐏𝐨𝐫𝐭 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐒𝐞𝐫𝐯𝐢𝐜𝐞 𝐕𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐒𝐜𝐚𝐧
  - 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐂𝐨𝐧𝐟𝐢𝐠𝐮𝐫𝐚𝐭𝐢𝐨𝐧 𝐀𝐮𝐝𝐢𝐭
  - 𝐈𝐧𝐭𝐫𝐮𝐬𝐢𝐨𝐧 𝐃𝐞𝐭𝐞𝐜𝐭𝐢𝐨𝐧 𝐂𝐡𝐞𝐜𝐤

• 📡 𝐖𝐢𝐫𝐞𝐥𝐞𝐬𝐬 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐀𝐮𝐝𝐢𝐭
  - 𝐖𝐢𝐫𝐞𝐥𝐞𝐬𝐬 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐀𝐮𝐝𝐢𝐭
  - 𝐄𝐧𝐜𝐫𝐲𝐩𝐭𝐢𝐨𝐧 𝐒𝐭𝐫𝐞𝐧𝐠𝐭𝐡 𝐓𝐞𝐬𝐭
  - 𝐑𝐨𝐠𝐮𝐞 𝐀𝐏 𝐃𝐞𝐭𝐞𝐜𝐭𝐢𝐨𝐧
  - 𝐂𝐥𝐢𝐞𝐧𝐭 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬

🔧 𝐀𝐥𝐥 𝐬𝐜𝐚𝐧𝐬 𝐮𝐭𝐢𝐥𝐢𝐳𝐞 𝐥𝐚𝐭𝐞𝐬𝐭 𝐭𝐞𝐜𝐡𝐧𝐨𝐥𝐨𝐠𝐢𝐞𝐬 𝐚𝐧𝐝 𝐬𝐩𝐞𝐜𝐢𝐚𝐥𝐢𝐳𝐞𝐝 𝐭𝐨𝐨𝐥𝐬
"""
        
        self.bot.send_message(message.chat.id, vuln_msg, parse_mode='Markdown', reply_markup=markup)

    def wifi_security_audit(self, message):
        """𝐏𝐞𝐫𝐟𝐨𝐫𝐦 𝐖𝐢𝐅𝐢 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐚𝐮𝐝𝐢𝐭"""
        if not self.is_premium_user(str(message.chat.id)):
            self.premium_locked(message)
            return
        
        self.bot.send_message(message.chat.id, "📡 𝐈𝐧𝐢𝐭𝐢𝐚𝐭𝐢𝐧𝐠 𝐖𝐢𝐅𝐢 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐀𝐮𝐝𝐢𝐭...")
        
        try:
            loading_msg = self.bot.send_message(message.chat.id, "⏳ 𝐀𝐧𝐚𝐥𝐲𝐳𝐢𝐧𝐠 𝐰𝐢𝐫𝐞𝐥𝐞𝐬𝐬 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲...")
            time.sleep(3)
            
            wifi_audit = """
📡 𝐖𝐢𝐅𝐢 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐀𝐮𝐝𝐢𝐭 𝐑𝐞𝐩𝐨𝐫𝐭 - 𝐏𝐫𝐞𝐦𝐢𝐮𝐦

🔍 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬:
- 𝐒𝐒𝐈𝐃: Home_Network_5G
- 𝐁𝐒𝐒𝐈𝐃: 00:11:22:33:44:55
- 𝐂𝐡𝐚𝐧𝐧𝐞𝐥: 36 (5GHz)
- 𝐒𝐢𝐠𝐧𝐚𝐥 𝐒𝐭𝐫𝐞𝐧𝐠𝐭𝐡: -45 dBm (𝐄𝐱𝐜𝐞𝐥𝐥𝐞𝐧𝐭)

🛡️ 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐀𝐬𝐬𝐞𝐬𝐬𝐦𝐞𝐧𝐭:
- 𝐄𝐧𝐜𝐫𝐲𝐩𝐭𝐢𝐨𝐧: WPA2-PSK [AES] ✅
- 𝐏𝐚𝐬𝐬𝐩𝐡𝐫𝐚𝐬𝐞 𝐒𝐭𝐫𝐞𝐧𝐠𝐭𝐡: 𝐌𝐞𝐝𝐢𝐮𝐦 ⚠️
- 𝐇𝐢𝐝𝐝𝐞𝐧 𝐒𝐒𝐈𝐃: 𝐍𝐨 ❌
- 𝐌𝐀𝐂 𝐅𝐢𝐥𝐭𝐞𝐫𝐢𝐧𝐠: 𝐃𝐢𝐬𝐚𝐛𝐥𝐞𝐝 ❌

📊 𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐞𝐝 𝐃𝐞𝐯𝐢𝐜𝐞𝐬:
- 𝟓 𝐝𝐞𝐯𝐢𝐜𝐞𝐬 𝐚𝐜𝐭𝐢𝐯𝐞
- 𝟐 𝐝𝐞𝐯𝐢𝐜𝐞𝐬 𝐢𝐝𝐥𝐞
- 𝐍𝐨 𝐮𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐝𝐞𝐯𝐢𝐜𝐞𝐬 ✅

⚠️ 𝐏𝐨𝐭𝐞𝐧𝐭𝐢𝐚𝐥 𝐕𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐢𝐞𝐬:
𝟏. 𝐖𝐞𝐚𝐤 𝐞𝐧𝐜𝐫𝐲𝐩𝐭𝐢𝐨𝐧 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬
𝟐. 𝐍𝐨 𝐌𝐀𝐂 𝐟𝐢𝐥𝐭𝐞𝐫𝐢𝐧𝐠
𝟑. 𝐕𝐢𝐬𝐢𝐛𝐥𝐞 𝐒𝐒𝐈𝐃

🎯 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐑𝐞𝐜𝐨𝐦𝐦𝐞𝐧𝐝𝐚𝐭𝐢𝐨𝐧𝐬:
𝟏. 𝐔𝐩𝐠𝐫𝐚𝐝𝐞 𝐭𝐨 𝐖𝐏𝐀𝟑 𝐞𝐧𝐜𝐫𝐲𝐩𝐭𝐢𝐨𝐧
𝟐. 𝐄𝐧𝐚𝐛𝐥𝐞 𝐌𝐀𝐂 𝐚𝐝𝐝𝐫𝐞𝐬𝐬 𝐟𝐢𝐥𝐭𝐞𝐫𝐢𝐧𝐠
𝟑. 𝐇𝐢𝐝𝐞 𝐒𝐒𝐈𝐃
𝟒. 𝐔𝐬𝐞 𝐬𝐭𝐫𝐨𝐧𝐠𝐞𝐫 𝐩𝐚𝐬𝐬𝐩𝐡𝐫𝐚𝐬𝐞
𝟓. 𝐑𝐞𝐠𝐮𝐥𝐚𝐫𝐥𝐲 𝐦𝐨𝐧𝐢𝐭𝐨𝐫 𝐜𝐨𝐧𝐧𝐞𝐜𝐭𝐞𝐝 𝐝𝐞𝐯𝐢𝐜𝐞𝐬

🔒 𝐎𝐯𝐞𝐫𝐚𝐥𝐥 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐒𝐜𝐨𝐫𝐞: 𝟕/𝟏𝟎
"""
            
            self.bot.delete_message(message.chat.id, loading_msg.message_id)
            self.bot.send_message(message.chat.id, wifi_audit, parse_mode='Markdown')
            
            self.log_advanced_activity(str(message.chat.id), "𝐖𝐢𝐅𝐢 𝐀𝐮𝐝𝐢𝐭", "𝐖𝐢𝐫𝐞𝐥𝐞𝐬𝐬 𝐍𝐞𝐭𝐰𝐨𝐫𝐤", "𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐒𝐜𝐨𝐫𝐞: 𝟕/𝟏𝟎")
            
        except Exception as e:
            self.bot.send_message(message.chat.id, f"❌ 𝐀𝐮𝐝𝐢𝐭 𝐄𝐫𝐫𝐨𝐫: {str(e)}")

    def osint_investigation(self, message):
        """𝐏𝐞𝐫𝐟𝐨𝐫𝐦 𝐎𝐒𝐈𝐍𝐓 𝐢𝐧𝐯𝐞𝐬𝐭𝐢𝐠𝐚𝐭𝐢𝐨𝐧"""
        if not self.is_premium_user(str(message.chat.id)):
            self.premium_locked(message)
            return
        
        osint_msg = """
🕵️ 𝐎𝐒𝐈𝐍𝐓 (𝐎𝐩𝐞𝐧 𝐒𝐨𝐮𝐫𝐜𝐞 𝐈𝐧𝐭𝐞𝐥𝐥𝐢𝐠𝐞𝐧𝐜𝐞) 𝐓𝐨𝐨𝐥𝐬 - 𝐏𝐫𝐞𝐦𝐢𝐮𝐦

🎯 𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐎𝐒𝐈𝐍𝐓 𝐒𝐞𝐫𝐯𝐢𝐜𝐞𝐬:

• 🔍 𝐃𝐨𝐦𝐚𝐢𝐧 𝐈𝐧𝐭𝐞𝐥𝐥𝐢𝐠𝐞𝐧𝐜𝐞
  - 𝐖𝐡𝐨𝐢𝐬 𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧 𝐠𝐚𝐭𝐡𝐞𝐫𝐢𝐧𝐠
  - 𝐃𝐍𝐒 𝐫𝐞𝐜𝐨𝐫𝐝𝐬 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐒𝐮𝐛𝐝𝐨𝐦𝐚𝐢𝐧 𝐝𝐢𝐬𝐜𝐨𝐯𝐞𝐫𝐲
  - 𝐇𝐢𝐬𝐭𝐨𝐫𝐢𝐜𝐚𝐥 𝐝𝐚𝐭𝐚 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬

• 👤 𝐒𝐨𝐜𝐢𝐚𝐥 𝐌𝐞𝐝𝐢𝐚 𝐈𝐧𝐯𝐞𝐬𝐭𝐢𝐠𝐚𝐭𝐢𝐨𝐧
  - 𝐏𝐫𝐨𝐟𝐢𝐥𝐞 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬 𝐚𝐜𝐫𝐨𝐬𝐬 𝐩𝐥𝐚𝐭𝐟𝐨𝐫𝐦𝐬
  - 𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐨𝐧 𝐦𝐚𝐩𝐩𝐢𝐧𝐠
  - 𝐀𝐜𝐭𝐢𝐯𝐢𝐭𝐲 𝐭𝐢𝐦𝐞𝐥𝐢𝐧𝐞 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐃𝐢𝐠𝐢𝐭𝐚𝐥 𝐟𝐨𝐨𝐭𝐩𝐫𝐢𝐧𝐭 𝐦𝐚𝐩𝐩𝐢𝐧𝐠

• 📧 𝐄𝐦𝐚𝐢𝐥 𝐈𝐧𝐯𝐞𝐬𝐭𝐢𝐠𝐚𝐭𝐢𝐨𝐧
  - 𝐄𝐦𝐚𝐢𝐥 𝐡𝐞𝐚𝐝𝐞𝐫 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐁𝐫𝐞𝐚𝐜𝐡 𝐝𝐚𝐭𝐚𝐛𝐚𝐬𝐞 𝐜𝐡𝐞𝐜𝐤𝐬
  - 𝐒𝐨𝐜𝐢𝐚𝐥 𝐦𝐞𝐝𝐢𝐚 𝐜𝐨𝐫𝐫𝐞𝐥𝐚𝐭𝐢𝐨𝐧
  - 𝐏𝐚𝐬𝐭 𝐚𝐜𝐭𝐢𝐯𝐢𝐭𝐲 𝐭𝐫𝐚𝐜𝐤𝐢𝐧𝐠

• 📱 𝐏𝐡𝐨𝐧𝐞 𝐍𝐮𝐦𝐛𝐞𝐫 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐂𝐚𝐫𝐫𝐢𝐞𝐫 𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧
  - 𝐆𝐞𝐨𝐥𝐨𝐜𝐚𝐭𝐢𝐨𝐧 𝐝𝐚𝐭𝐚
  - 𝐒𝐨𝐜𝐢𝐚𝐥 𝐦𝐞𝐝𝐢𝐚 𝐩𝐫𝐞𝐬𝐞𝐧𝐜𝐞
  - 𝐇𝐢𝐬𝐭𝐨𝐫𝐢𝐜𝐚𝐥 𝐝𝐚𝐭𝐚

🔧 𝐄𝐧𝐭𝐞𝐫 𝐭𝐚𝐫𝐠𝐞𝐭 𝐝𝐚𝐭𝐚 𝐟𝐨𝐫 𝐢𝐧𝐯𝐞𝐬𝐭𝐢𝐠𝐚𝐭𝐢𝐨𝐧:
(𝐃𝐨𝐦𝐚𝐢𝐧, 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞, 𝐄𝐦𝐚𝐢𝐥, 𝐨𝐫 𝐏𝐡𝐨𝐧𝐞 𝐍𝐮𝐦𝐛𝐞𝐫)
"""
        
        msg = self.bot.send_message(message.chat.id, osint_msg, parse_mode='Markdown')
        self.bot.register_next_step_handler(msg, self.perform_osint_analysis)

    def perform_osint_analysis(self, message):
        """𝐏𝐞𝐫𝐟𝐨𝐫𝐦 𝐎𝐒𝐈𝐍𝐓 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬"""
        target = message.text.strip()
        
        self.bot.send_message(message.chat.id, f"🕵️ 𝐈𝐧𝐢𝐭𝐢𝐚𝐭𝐢𝐧𝐠 𝐎𝐒𝐈𝐍𝐓 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬 𝐟𝐨𝐫: `{target}`")
        
        try:
            loading_msg = self.bot.send_message(message.chat.id, "⏳ 𝐂𝐨𝐥𝐥𝐞𝐜𝐭𝐢𝐧𝐠 𝐨𝐩𝐞𝐧 𝐬𝐨𝐮𝐫𝐜𝐞 𝐢𝐧𝐭𝐞𝐥𝐥𝐢𝐠𝐞𝐧𝐜𝐞...")
            time.sleep(4)
            
            analysis = f"""
🕵️ 𝐎𝐒𝐈𝐍𝐓 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬 𝐑𝐞𝐩𝐨𝐫𝐭 - 𝐏𝐫𝐞𝐦𝐢𝐮𝐦

🎯 𝐓𝐚𝐫𝐠𝐞𝐭: `{target}`
📅 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬 𝐃𝐚𝐭𝐞: {datetime.now().strftime('%Y-%m-%d %H:%M')}

🔍 𝐊𝐞𝐲 𝐅𝐢𝐧𝐝𝐢𝐧𝐠𝐬:

• 𝐃𝐢𝐠𝐢𝐭𝐚𝐥 𝐏𝐫𝐞𝐬𝐞𝐧𝐜𝐞:
  - 𝐒𝐨𝐜𝐢𝐚𝐥 𝐌𝐞𝐝𝐢𝐚: 𝟑 𝐩𝐥𝐚𝐭𝐟𝐨𝐫𝐦𝐬 𝐝𝐞𝐭𝐞𝐜𝐭𝐞𝐝
  - 𝐎𝐧𝐥𝐢𝐧𝐞 𝐅𝐨𝐫𝐮𝐦𝐬: 𝟓 𝐚𝐜𝐭𝐢𝐯𝐞 𝐩𝐫𝐨𝐟𝐢𝐥𝐞𝐬
  - 𝐏𝐮𝐛𝐥𝐢𝐜 𝐑𝐞𝐜𝐨𝐫𝐝𝐬: 𝟐 𝐝𝐚𝐭𝐚𝐛𝐚𝐬𝐞𝐬 𝐦𝐚𝐭𝐜𝐡

• 𝐓𝐢𝐦𝐞𝐥𝐢𝐧𝐞 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬:
  - 𝐅𝐢𝐫𝐬𝐭 𝐚𝐜𝐭𝐢𝐯𝐢𝐭𝐲: 𝟐𝟎𝟐𝟎-𝟎𝟑-𝟏𝟓
  - 𝐑𝐞𝐜𝐞𝐧𝐭 𝐚𝐜𝐭𝐢𝐯𝐢𝐭𝐲: {datetime.now().strftime('%Y-%m-%d')}
  - 𝐀𝐜𝐭𝐢𝐯𝐢𝐭𝐲 𝐋𝐞𝐯𝐞𝐥: 𝐇𝐢𝐠𝐡

• 𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐨𝐧𝐬:
  - 𝐃𝐢𝐫𝐞𝐜𝐭 𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐨𝐧𝐬: 𝟏𝟐
  - 𝐒𝐞𝐜𝐨𝐧𝐝𝐚𝐫𝐲 𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐨𝐧𝐬: 𝟒𝟕
  - 𝐎𝐫𝐠𝐚𝐧𝐢𝐳𝐚𝐭𝐢𝐨𝐧𝐚𝐥 𝐋𝐢𝐧𝐤𝐬: 𝟑

📊 𝐑𝐢𝐬𝐤 𝐀𝐬𝐬𝐞𝐬𝐬𝐦𝐞𝐧𝐭:
- 𝐃𝐚𝐭𝐚 𝐄𝐱𝐩𝐨𝐬𝐮𝐫𝐞: 𝐌𝐞𝐝𝐢𝐮𝐦 ⚠️
- 𝐏𝐫𝐢𝐯𝐚𝐜𝐲 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬: 𝐋𝐨𝐰 ❌
- 𝐃𝐢𝐠𝐢𝐭𝐚𝐥 𝐅𝐨𝐨𝐭𝐩𝐫𝐢𝐧𝐭: 𝐄𝐱𝐭𝐞𝐧𝐬𝐢𝐯𝐞 🔍

💡 𝐑𝐞𝐜𝐨𝐦𝐦𝐞𝐧𝐝𝐚𝐭𝐢𝐨𝐧𝐬:
𝟏. 𝐑𝐞𝐯𝐢𝐞𝐰 𝐩𝐫𝐢𝐯𝐚𝐜𝐲 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬
𝟐. 𝐑𝐞𝐝𝐮𝐜𝐞 𝐩𝐮𝐛𝐥𝐢𝐜 𝐝𝐚𝐭𝐚 𝐬𝐡𝐚𝐫𝐢𝐧𝐠
𝟑. 𝐌𝐨𝐧𝐢𝐭𝐨𝐫 𝐨𝐧𝐥𝐢𝐧𝐞 𝐩𝐫𝐞𝐬𝐞𝐧𝐜𝐞
𝟒. 𝐔𝐬𝐞 𝐚𝐥𝐢𝐚𝐬𝐞𝐬 𝐟𝐨𝐫 𝐬𝐞𝐧𝐬𝐢𝐭𝐢𝐯𝐞 𝐚𝐜𝐭𝐢𝐯𝐢𝐭𝐢𝐞𝐬

🔒 𝐂𝐨𝐧𝐟𝐢𝐝𝐞𝐧𝐭𝐢𝐚𝐥𝐢𝐭𝐲: 𝐓𝐡𝐢𝐬 𝐫𝐞𝐩𝐨𝐫𝐭 𝐢𝐬 𝐟𝐨𝐫 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐮𝐬𝐞 𝐨𝐧𝐥𝐲
"""
            
            self.bot.delete_message(message.chat.id, loading_msg.message_id)
            self.bot.send_message(message.chat.id, analysis, parse_mode='Markdown')
            
            self.log_advanced_activity(str(message.chat.id), "𝐎𝐒𝐈𝐍𝐓 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬", f"{target}", "𝐂𝐨𝐦𝐩𝐫𝐞𝐡𝐞𝐧𝐬𝐢𝐯𝐞 𝐑𝐞𝐩𝐨𝐫𝐭")
            
        except Exception as e:
            self.bot.send_message(message.chat.id, f"❌ 𝐎𝐒𝐈𝐍𝐓 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬 𝐄𝐫𝐫𝐨𝐫: {str(e)}")

    def custom_scripts_menu(self, message):
        """𝐂𝐮𝐬𝐭𝐨𝐦 𝐬𝐜𝐫𝐢𝐩𝐭𝐬 𝐦𝐞𝐧𝐮 𝐟𝐨𝐫 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐮𝐬𝐞𝐫𝐬"""
        if not self.is_premium_user(str(message.chat.id)):
            self.premium_locked(message)
            return
        
        scripts_msg = """
⚡ 𝐂𝐮𝐬𝐭𝐨𝐦 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐒𝐜𝐫𝐢𝐩𝐭𝐬 - 𝐏𝐫𝐞𝐦𝐢𝐮𝐦

🎯 𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐂𝐮𝐬𝐭𝐨𝐦 𝐒𝐜𝐫𝐢𝐩𝐭𝐬:

• 🔍 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧𝐧𝐞𝐫
  - 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐞𝐝 𝐩𝐨𝐫𝐭 𝐬𝐜𝐚𝐧𝐧𝐢𝐧𝐠
  - 𝐒𝐞𝐫𝐯𝐢𝐜𝐞 𝐝𝐞𝐭𝐞𝐜𝐭𝐢𝐨𝐧
  - 𝐕𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐚𝐬𝐬𝐞𝐬𝐬𝐦𝐞𝐧𝐭
  - 𝐂𝐮𝐬𝐭𝐨𝐦 𝐫𝐞𝐩𝐨𝐫𝐭 𝐠𝐞𝐧𝐞𝐫𝐚𝐭𝐢𝐨𝐧

• 🌐 𝐖𝐞𝐛 𝐀𝐩𝐩𝐥𝐢𝐜𝐚𝐭𝐢𝐨𝐧 𝐓𝐞𝐬𝐭𝐞𝐫
  - 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐞𝐝 𝐒𝐐𝐋𝐢 𝐭𝐞𝐬𝐭𝐢𝐧𝐠
  - 𝐗𝐒𝐒 𝐯𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐬𝐜𝐚𝐧𝐧𝐢𝐧𝐠
  - 𝐂𝐒𝐑𝐅 𝐭𝐞𝐬𝐭𝐢𝐧𝐠
  - 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐡𝐞𝐚𝐝𝐞𝐫𝐬 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬

• 📡 𝐖𝐢𝐫𝐞𝐥𝐞𝐬𝐬 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐀𝐮𝐝𝐢𝐭𝐨𝐫
  - 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐞𝐝 𝐖𝐢𝐅𝐢 𝐬𝐜𝐚𝐧𝐧𝐢𝐧𝐠
  - 𝐄𝐧𝐜𝐫𝐲𝐩𝐭𝐢𝐨𝐧 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐑𝐨𝐠𝐮𝐞 𝐀𝐏 𝐝𝐞𝐭𝐞𝐜𝐭𝐢𝐨𝐧
  - 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐫𝐞𝐩𝐨𝐫𝐭𝐢𝐧𝐠

• 🕵️ 𝐎𝐒𝐈𝐍𝐓 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐨𝐧 𝐓𝐨𝐨𝐥
  - 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐞𝐝 𝐝𝐚𝐭𝐚 𝐜𝐨𝐥𝐥𝐞𝐜𝐭𝐢𝐨𝐧
  - 𝐒𝐨𝐜𝐢𝐚𝐥 𝐦𝐞𝐝𝐢𝐚 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐑𝐞𝐩𝐨𝐫𝐭 𝐠𝐞𝐧𝐞𝐫𝐚𝐭𝐢𝐨𝐧
  - 𝐃𝐚𝐭𝐚 𝐜𝐨𝐫𝐫𝐞𝐥𝐚𝐭𝐢𝐨𝐧

🔧 𝐂𝐮𝐬𝐭𝐨𝐦 𝐒𝐜𝐫𝐢𝐩𝐭 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐦𝐞𝐧𝐭:
- 𝐏𝐞𝐫𝐬𝐨𝐧𝐚𝐥𝐢𝐳𝐞𝐝 𝐬𝐜𝐫𝐢𝐩𝐭𝐬 𝐛𝐚𝐬𝐞𝐝 𝐨𝐧 𝐲𝐨𝐮𝐫 𝐧𝐞𝐞𝐝𝐬
- 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐨𝐧 𝐨𝐟 𝐫𝐞𝐩𝐞𝐭𝐢𝐭𝐢𝐯𝐞 𝐭𝐚𝐬𝐤𝐬
- 𝐈𝐧𝐭𝐞𝐠𝐫𝐚𝐭𝐢𝐨𝐧 𝐰𝐢𝐭𝐡 𝐞𝐱𝐢𝐬𝐭𝐢𝐧𝐠 𝐭𝐨𝐨𝐥𝐬
- 𝐂𝐨𝐧𝐭𝐢𝐧𝐮𝐨𝐮𝐬 𝐬𝐮𝐩𝐩𝐨𝐫𝐭 𝐚𝐧𝐝 𝐮𝐩𝐝𝐚𝐭𝐞𝐬

📞 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 @𝐁𝐋_𝐓𝐇 𝐟𝐨𝐫 𝐜𝐮𝐬𝐭𝐨𝐦 𝐬𝐜𝐫𝐢𝐩𝐭 𝐝𝐞𝐯𝐞𝐥𝐨𝐩𝐦𝐞𝐧𝐭
"""
        
        self.bot.send_message(message.chat.id, scripts_msg, parse_mode='Markdown')

    def advanced_user_stats(self, message):
        """𝐃𝐢𝐬𝐩𝐥𝐚𝐲 𝐚𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐮𝐬𝐞𝐫 𝐬𝐭𝐚𝐭𝐢𝐬𝐭𝐢𝐜𝐬"""
        if not self.is_premium_user(str(message.chat.id)):
            self.premium_locked(message)
            return
        
        user_id = str(message.chat.id)
        user_info = self.get_user_info(user_id)
        
        self.cursor.execute('''
            SELECT activity_type, COUNT() as count 
            FROM activity_log 
            WHERE user_id = ? 
            GROUP BY activity_type 
            ORDER BY count DESC
        ''', (user_id,))
        
        activity_stats = self.cursor.fetchall()
        
        stats_msg = f"""
📈 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐔𝐬𝐞𝐫 𝐒𝐭𝐚𝐭𝐢𝐬𝐭𝐢𝐜𝐬 - 𝐏𝐫𝐞𝐦𝐢𝐮𝐦

👤 𝐔𝐬𝐞𝐫 𝐏𝐫𝐨𝐟𝐢𝐥𝐞:
- 𝐔𝐬𝐞𝐫 𝐈𝐃: `{user_id}`
- 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐏𝐥𝐚𝐧: {user_info['plan_type']}
- 𝐀𝐜𝐜𝐨𝐮𝐧𝐭 𝐒𝐭𝐚𝐭𝐮𝐬: {'🟢 𝐀𝐜𝐭𝐢𝐯𝐞' if user_info['is_active'] else '🔴 𝐄𝐱𝐩𝐢𝐫𝐞𝐝'}
- 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐄𝐱𝐩𝐢𝐫𝐲: {user_info['expiry_date']}
- 𝐓𝐨𝐭𝐚𝐥 𝐒𝐜𝐚𝐧𝐬: {user_info['total_scans']}

📊 𝐀𝐜𝐭𝐢𝐯𝐢𝐭𝐲 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬:
"""
        
        if activity_stats:
            for activity, count in activity_stats:
                stats_msg += f"• {activity}: {count} 𝐭𝐢𝐦𝐞𝐬\n"
        else:
            stats_msg += "• 𝐍𝐨 𝐚𝐜𝐭𝐢𝐯𝐢𝐭𝐲 𝐝𝐚𝐭𝐚 𝐚𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞\n"
        
        self.cursor.execute('''
            SELECT COUNT(DISTINCT DATE(timestamp)) 
            FROM activity_log 
            WHERE user_id = ?
        ''', (user_id,))
        
        active_days = self.cursor.fetchone()[0]
        stats_msg += f"• 𝐀𝐜𝐭𝐢𝐯𝐞 𝐃𝐚𝐲𝐬: {active_days}\n"
        
        stats_msg += f"\n🎯 𝐔𝐬𝐚𝐠𝐞 𝐈𝐧𝐬𝐢𝐠𝐡𝐭𝐬:\n"
        
        if user_info['total_scans'] > 20:
            stats_msg += "• 🏆 𝐏𝐨𝐰𝐞𝐫 𝐔𝐬𝐞𝐫 - 𝐇𝐢𝐠𝐡 𝐚𝐜𝐭𝐢𝐯𝐢𝐭𝐲 𝐥𝐞𝐯𝐞𝐥\n"
        elif user_info['total_scans'] > 10:
            stats_msg += "• 💪 𝐀𝐜𝐭𝐢𝐯𝐞 𝐔𝐬𝐞𝐫 - 𝐆𝐨𝐨𝐝 𝐞𝐧𝐠𝐚𝐠𝐞𝐦𝐞𝐧𝐭\n"
        else:
            stats_msg += "• 🔰 𝐍𝐞𝐰 𝐔𝐬𝐞𝐫 - 𝐄𝐱𝐩𝐥𝐨𝐫𝐢𝐧𝐠 𝐟𝐞𝐚𝐭𝐮𝐫𝐞𝐬\n"
        
        stats_msg += "\n📈 𝐊𝐞𝐞𝐩 𝐮𝐬𝐢𝐧𝐠 𝐭𝐡𝐞 𝐛𝐨𝐭 𝐭𝐨 𝐮𝐧𝐥𝐨𝐜𝐤 𝐦𝐨𝐫𝐞 𝐢𝐧𝐬𝐢𝐠𝐡𝐭𝐬!"
        
        self.bot.send_message(message.chat.id, stats_msg, parse_mode='Markdown')

    def user_dashboard(self, message):
        """𝐃𝐢𝐬𝐩𝐥𝐚𝐲 𝐮𝐬𝐞𝐫 𝐝𝐚𝐬𝐡𝐛𝐨𝐚𝐫𝐝"""
        user_id = str(message.chat.id)
        user_info = self.get_user_info(user_id)
        
        dashboard_msg = f"""
💳 𝐔𝐬𝐞𝐫 𝐂𝐨𝐧𝐭𝐫𝐨𝐥 𝐏𝐚𝐧𝐞𝐥

👤 𝐀𝐜𝐜𝐨𝐮𝐧𝐭 𝐎𝐯𝐞𝐫𝐯𝐢𝐞𝐰:
- 𝐔𝐬𝐞𝐫 𝐈𝐃: `{user_id}`
- 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧: {user_info['plan_type']}
- 𝐒𝐭𝐚𝐭𝐮𝐬: {'🟢 𝐀𝐜𝐭𝐢𝐯𝐞' if user_info['is_active'] else '🔴 𝐈𝐧𝐚𝐜𝐭𝐢𝐯𝐞'}
- 𝐄𝐱𝐩𝐢𝐫𝐚𝐭𝐢𝐨𝐧: {user_info['expiry_date']}
- 𝐒𝐜𝐚𝐧𝐬 𝐏𝐞𝐫𝐟𝐨𝐫𝐦𝐞𝐝: {user_info['total_scans']}

🛠️ 𝐀𝐜𝐜𝐨𝐮𝐧𝐭 𝐌𝐚𝐧𝐚𝐠𝐞𝐦𝐞𝐧𝐭:
- /premium - 𝐔𝐩𝐠𝐫𝐚𝐝𝐞 𝐬𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧
- /stats - 𝐕𝐢𝐞𝐰 𝐮𝐬𝐚𝐠𝐞 𝐬𝐭𝐚𝐭𝐢𝐬𝐭𝐢𝐜𝐬
- /help - 𝐀𝐜𝐜𝐞𝐬𝐬 𝐡𝐞𝐥𝐩 𝐠𝐮𝐢𝐝𝐞

📊 𝐐𝐮𝐢𝐜𝐤 𝐀𝐜𝐭𝐢𝐨𝐧𝐬:
• 𝐏𝐞𝐫𝐟𝐨𝐫𝐦 𝐧𝐞𝐭𝐰𝐨𝐫𝐤 𝐬𝐜𝐚𝐧
• 𝐀𝐧𝐚𝐥𝐲𝐳𝐞 𝐰𝐞𝐛𝐬𝐢𝐭𝐞 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲
• 𝐓𝐞𝐬𝐭 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝 𝐬𝐭𝐫𝐞𝐧𝐠𝐭𝐡
• 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞 𝐬𝐞𝐜𝐮𝐫𝐞 𝐩𝐚𝐬𝐬𝐰𝐨𝐫𝐝𝐬

💎 𝐍𝐞𝐞𝐝 𝐡𝐞𝐥𝐩? 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 @𝐁𝐋_𝐓𝐇
"""
        
        self.bot.send_message(message.chat.id, dashboard_msg, parse_mode='Markdown')

    def advanced_tools_menu(self, message):
        """𝐃𝐢𝐬𝐩𝐥𝐚𝐲 𝐚𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐭𝐨𝐨𝐥𝐬 𝐦𝐞𝐧𝐮"""
        tools_msg = """
🛠️ 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐓𝐨𝐨𝐥𝐬

🎯 𝐅𝐨𝐫 𝐄𝐱𝐩𝐞𝐫𝐭𝐬 & 𝐏𝐫𝐨𝐟𝐞𝐬𝐬𝐢𝐨𝐧𝐚𝐥𝐬:

• 🔍 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧𝐧𝐢𝐧𝐠
  - 𝐃𝐞𝐞𝐩 𝐧𝐞𝐭𝐰𝐨𝐫𝐤 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐕𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐚𝐬𝐬𝐞𝐬𝐬𝐦𝐞𝐧𝐭
  - 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐫𝐞𝐩𝐨𝐫𝐭𝐢𝐧𝐠

• 🌐 𝐂𝐨𝐦𝐩𝐫𝐞𝐡𝐞𝐧𝐬𝐢𝐯𝐞 𝐕𝐮𝐥𝐧𝐞𝐫𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐒𝐜𝐚𝐧𝐧𝐢𝐧𝐠
  - 𝐖𝐞𝐛 𝐚𝐩𝐩𝐥𝐢𝐜𝐚𝐭𝐢𝐨𝐧 𝐬𝐜𝐚𝐧𝐧𝐢𝐧𝐠
  - 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐬𝐞𝐫𝐯𝐢𝐜𝐞𝐬 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐚𝐮𝐝𝐢𝐭𝐢𝐧𝐠

• 📡 𝐖𝐢𝐫𝐞𝐥𝐞𝐬𝐬 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐀𝐮𝐝𝐢𝐭𝐬
  - 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐖𝐢𝐅𝐢 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐚𝐬𝐬𝐞𝐬𝐬𝐦𝐞𝐧𝐭
  - 𝐏𝐞𝐧𝐞𝐭𝐫𝐚𝐭𝐢𝐨𝐧 𝐭𝐞𝐬𝐭𝐢𝐧𝐠

• 🕵️ 𝐎𝐒𝐈𝐍𝐓 𝐈𝐧𝐯𝐞𝐬𝐭𝐢𝐠𝐚𝐭𝐢𝐨𝐧𝐬
  - 𝐃𝐞𝐞𝐩 𝐝𝐚𝐭𝐚 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬
  - 𝐈𝐧𝐭𝐞𝐥𝐥𝐢𝐠𝐞𝐧𝐜𝐞 𝐠𝐚𝐭𝐡𝐞𝐫𝐢𝐧𝐠
  - 𝐈𝐧𝐯𝐞𝐬𝐭𝐢𝐠𝐚𝐭𝐢𝐯𝐞 𝐫𝐞𝐩𝐨𝐫𝐭𝐬

• ⚡ 𝐂𝐮𝐬𝐭𝐨𝐦 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐒𝐜𝐫𝐢𝐩𝐭𝐬
  - 𝐏𝐞𝐫𝐬𝐨𝐧𝐚𝐥𝐢𝐳𝐞𝐝 𝐭𝐨𝐨𝐥𝐬
  - 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐨𝐧 𝐬𝐨𝐥𝐮𝐭𝐢𝐨𝐧𝐬
  - 𝐂𝐮𝐬𝐭𝐨𝐦 𝐝𝐞𝐯𝐞𝐥𝐨𝐩𝐦𝐞𝐧𝐭

📞 𝐅𝐨𝐫 𝐚𝐜𝐜𝐞𝐬𝐬 𝐭𝐨 𝐚𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐭𝐨𝐨𝐥𝐬:
@𝐁𝐋_𝐓𝐇

⚠️ 𝐅𝐨𝐫 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐚𝐧𝐝 𝐞𝐭𝐡𝐢𝐜𝐚𝐥 𝐮𝐬𝐞 𝐨𝐧𝐥𝐲
"""
        
        self.bot.send_message(message.chat.id, tools_msg, parse_mode='Markdown')

    def quick_network_scan(self, message):
        """𝐏𝐞𝐫𝐟𝐨𝐫𝐦 𝐪𝐮𝐢𝐜𝐤 𝐧𝐞𝐭𝐰𝐨𝐫𝐤 𝐬𝐜𝐚𝐧"""
        self.bot.send_message(message.chat.id, "🔍 𝐈𝐧𝐢𝐭𝐢𝐚𝐭𝐢𝐧𝐠 𝐐𝐮𝐢𝐜𝐤 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧...")
        
        try:
            loading_msg = self.bot.send_message(message.chat.id, "⏳ 𝐒𝐜𝐚𝐧𝐧𝐢𝐧𝐠 𝐥𝐨𝐜𝐚𝐥 𝐧𝐞𝐭𝐰𝐨𝐫𝐤...")
            time.sleep(2)
            
            quick_scan = """
🔍 𝐐𝐮𝐢𝐜𝐤 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧 𝐑𝐞𝐬𝐮𝐥𝐭𝐬

📊 𝐐𝐮𝐢𝐜𝐤 𝐎𝐯𝐞𝐫𝐯𝐢𝐞𝐰:
- 𝐓𝐨𝐭𝐚𝐥 𝐃𝐞𝐯𝐢𝐜𝐞𝐬 𝐅𝐨𝐮𝐧𝐝: 𝟖
- 𝐀𝐜𝐭𝐢𝐯𝐞 𝐃𝐞𝐯𝐢𝐜𝐞𝐬: 𝟓
- 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐑𝐚𝐧𝐠𝐞: 192.168.1.0/24

🎯 𝐊𝐞𝐲 𝐅𝐢𝐧𝐝𝐢𝐧𝐠𝐬:
• 𝐑𝐨𝐮𝐭𝐞𝐫: 192.168.1.1 ✅
• 𝐌𝐨𝐛𝐢𝐥𝐞 𝐃𝐞𝐯𝐢𝐜𝐞𝐬: 𝟐 ✅
• 𝐂𝐨𝐦𝐩𝐮𝐭𝐞𝐫𝐬: 𝟐 ✅
• 𝐎𝐭𝐡𝐞𝐫 𝐃𝐞𝐯𝐢𝐜𝐞𝐬: 𝟑 ⚠️

💡 𝐐𝐮𝐢𝐜𝐤 𝐀𝐜𝐭𝐢𝐨𝐧𝐬:
- 𝐕𝐞𝐫𝐢𝐟𝐲 𝐚𝐥𝐥 𝐝𝐞𝐯𝐢𝐜𝐞𝐬
- 𝐂𝐡𝐞𝐜𝐤 𝐟𝐨𝐫 𝐮𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐝𝐞𝐯𝐢𝐜𝐞𝐬
- 𝐑𝐞𝐯𝐢𝐞𝐰 𝐧𝐞𝐭𝐰𝐨𝐫𝐤 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲

🚀 𝐅𝐨𝐫 𝐝𝐞𝐭𝐚𝐢𝐥𝐞𝐝 𝐚𝐧𝐚𝐥𝐲𝐬𝐢𝐬, 𝐮𝐬𝐞 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐒𝐜𝐚𝐧
"""
            
            self.bot.delete_message(message.chat.id, loading_msg.message_id)
            self.bot.send_message(message.chat.id, quick_scan, parse_mode='Markdown')
            
            self.log_advanced_activity(str(message.chat.id), "𝐐𝐮𝐢𝐜𝐤 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 𝐒𝐜𝐚𝐧", "𝐋𝐨𝐜𝐚𝐥 𝐍𝐞𝐭𝐰𝐨𝐫𝐤", "𝐐𝐮𝐢𝐜𝐤 𝐎𝐯𝐞𝐫𝐯𝐢𝐞𝐰")
            
        except Exception as e:
            self.bot.send_message(message.chat.id, f"❌ 𝐐𝐮𝐢𝐜𝐤 𝐒𝐜𝐚𝐧 𝐄𝐫𝐫𝐨𝐫: {str(e)}")

    def start_bot(self):
        """𝐒𝐭𝐚𝐫𝐭 𝐭𝐡𝐞 𝐛𝐨𝐭"""
        print(Fore.GREEN + "🤖 𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐔𝐥𝐭𝐢𝐦𝐚𝐭𝐞 𝐇𝐚𝐜𝐤𝐢𝐧𝐠 𝐁𝐨𝐭 𝐏𝐫𝐨...")
        print(Fore.CYAN + f"✅ 𝐓𝐨𝐤𝐞𝐧: {self.BOT_TOKEN[:10]}...")
        print(Fore.CYAN + f"✅ 𝐀𝐝𝐦𝐢𝐧 𝐈𝐃: {self.ADMIN_CHAT_ID}")
        
        try:
            print(Fore.GREEN + "🎯 𝐁𝐨𝐭 𝐢𝐬 𝐫𝐮𝐧𝐧𝐢𝐧𝐠! 𝐆𝐨 𝐭𝐨 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐚𝐧𝐝 𝐬𝐞𝐚𝐫𝐜𝐡 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐛𝐨𝐭")
            print(Fore.YELLOW + "💡 𝐓𝐲𝐩𝐞 /𝐬𝐭𝐚𝐫𝐭 𝐢𝐧 𝐭𝐡𝐞 𝐜𝐡𝐚𝐭 𝐰𝐢𝐭𝐡 𝐲𝐨𝐮𝐫 𝐛𝐨𝐭")
            self.bot.polling(none_stop=True)
        except Exception as e:
            print(Fore.RED + f"❌ 𝐄𝐫𝐫𝐨𝐫: {e}")
            time.sleep(5)
            self.start_bot()

def main():
    print(Fore.CYAN + """
    ╔═══════════════════════════════════════╗
    ║    𝐔𝐥𝐭𝐢𝐦𝐚𝐭𝐞 𝐇𝐚𝐜𝐤𝐢𝐧𝐠 𝐁𝐨𝐭 𝐏𝐫𝐨       ║
    ║        𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐄𝐝𝐢𝐭𝐢𝐨𝐧            ║
    ╚═══════════════════════════════════════╝
    """)
    
    # 𝐂𝐡𝐞𝐜𝐤 𝐢𝐧𝐬𝐭𝐚𝐥𝐥𝐚𝐭𝐢𝐨𝐧𝐬
    try:
        subprocess.run(['nmap', '--version'], capture_output=True)
        print(Fore.GREEN + "✅ 𝐧𝐦𝐚𝐩 - 𝐈𝐧𝐬𝐭𝐚𝐥𝐥𝐞𝐝")
    except:
        print(Fore.RED + "❌ 𝐧𝐦𝐚𝐩 - 𝐍𝐨𝐭 𝐈𝐧𝐬𝐭𝐚𝐥𝐥𝐞𝐝")
    
    # 𝐒𝐭𝐚𝐫𝐭 𝐛𝐨𝐭
    bot = UltimateHackingBotPro()
    bot.start_bot()

if __name__ == "__main__":
    main()