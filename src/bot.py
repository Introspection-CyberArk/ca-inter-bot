#!/usr/bin/env python3
"""
CA Intermediate Exam Bot - Main Application
Created by: MeNgHeaNg
Powered by: @Introspection007
Version: 2.0
"""

import os
import sys
import logging
import random
from datetime import datetime
from typing import Dict, List, Optional, Any

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Telegram imports
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)

# ==================== CONFIGURATION ====================
class Config:
    """Bot configuration"""
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '8707473118:AAErmBRuzuU9JRR08mE4TNsGDGUWdHwVpxU')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/ca_bot.db')
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    VERSION = "2.0"
    CREATOR = "MeNgHeaNg"
    POWERED_BY = "@Introspection007"

# ==================== LOGGING ====================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== CONSTANTS ====================
(SUBJECT, TOPIC, DOUBT_INPUT, TEST_MODE) = range(4)

# ==================== CA CONTENT ====================
class CAContent:
    """Complete CA Intermediate content database"""
    
    def __init__(self):
        self.subjects = {
            'accounts': '📚 Accounting',
            'law': '⚖️ Business Laws', 
            'taxation': '💰 Taxation',
            'costing': '📊 Cost & Management Accounting',
            'audit': '📋 Auditing',
            'fm_sm': '📑 Financial Management & Strategic Management'
        }
        
        self.topics = {
            'accounts': [
                {'id': 'acc_1', 'name': 'Accounting Standards', 'emoji': '📖'},
                {'id': 'acc_2', 'name': 'Company Accounts', 'emoji': '🏢'},
                {'id': 'acc_3', 'name': 'Consolidation', 'emoji': '📊'},
                {'id': 'acc_4', 'name': 'Partnership Accounts', 'emoji': '🤝'},
                {'id': 'acc_5', 'name': 'Financial Statements', 'emoji': '📈'}
            ],
            'law': [
                {'id': 'law_1', 'name': 'Company Law', 'emoji': '🏛️'},
                {'id': 'law_2', 'name': 'Contract Law', 'emoji': '📜'},
                {'id': 'law_3', 'name': 'Negotiable Instruments', 'emoji': '💳'},
                {'id': 'law_4', 'name': 'LLP Law', 'emoji': '🤝'}
            ],
            'taxation': [
                {'id': 'tax_1', 'name': 'Income Tax Basics', 'emoji': '💵'},
                {'id': 'tax_2', 'name': 'TDS & TCS', 'emoji': '💰'},
                {'id': 'tax_3', 'name': 'GST', 'emoji': '🛒'},
                {'id': 'tax_4', 'name': 'Filing Returns', 'emoji': '📋'}
            ],
            'costing': [
                {'id': 'cost_1', 'name': 'Cost Sheet', 'emoji': '📊'},
                {'id': 'cost_2', 'name': 'BEP Analysis', 'emoji': '📈'},
                {'id': 'cost_3', 'name': 'Standard Costing', 'emoji': '🎯'},
                {'id': 'cost_4', 'name': 'Budgeting', 'emoji': '📅'}
            ],
            'audit': [
                {'id': 'aud_1', 'name': 'Audit Planning', 'emoji': '📋'},
                {'id': 'aud_2', 'name': 'Internal Audit', 'emoji': '🔍'},
                {'id': 'aud_3', 'name': 'Statutory Audit', 'emoji': '✅'},
                {'id': 'aud_4', 'name': 'Audit Report', 'emoji': '📄'}
            ],
            'fm_sm': [
                {'id': 'fm_1', 'name': 'Financial Management', 'emoji': '💹'},
                {'id': 'fm_2', 'name': 'Working Capital', 'emoji': '🔄'},
                {'id': 'fm_3', 'name': 'Strategic Management', 'emoji': '🎯'},
                {'id': 'fm_4', 'name': 'Corporate Governance', 'emoji': '🏢'}
            ]
        }
        
        self.mcqs = {
            'acc_1': [
                {
                    'id': 'acc_1_1',
                    'question': 'Which accounting standard deals with Property, Plant and Equipment?',
                    'options': ['AS 10', 'AS 16', 'AS 7', 'AS 19'],
                    'correct_answer': 0,
                    'explanation': 'AS 10 deals with Property, Plant and Equipment. It covers depreciation and fixed assets.',
                    'hint': 'Remember the standard numbers!'
                },
                {
                    'id': 'acc_1_2',
                    'question': 'What is the accounting treatment for Capital Reserve?',
                    'options': [
                        'Credited to Profit & Loss A/c',
                        'Shown in Balance Sheet as liability',
                        'Shown in Balance Sheet as Reserve & Surplus',
                        'Transferred to general reserve'
                    ],
                    'correct_answer': 2,
                    'explanation': 'Capital reserve is shown under Reserves & Surplus in the Balance Sheet. It cannot be used for dividend distribution.',
                    'hint': 'Think about where reserves are shown in Balance Sheet'
                },
                {
                    'id': 'acc_1_3',
                    'question': 'Which method is used for consolidation of financial statements?',
                    'options': [
                        'Equity method',
                        'Proportionate method',
                        'Full consolidation method',
                        'Cost method'
                    ],
                    'correct_answer': 2,
                    'explanation': 'Full consolidation method is used where the parent company has control over the subsidiary.',
                    'hint': 'Consider which method shows complete control'
                }
            ],
            'law_1': [
                {
                    'id': 'law_1_1',
                    'question': 'Minimum number of directors required in a public company?',
                    'options': ['2', '3', '5', '7'],
                    'correct_answer': 1,
                    'explanation': 'Section 149(1) of Companies Act 2013 requires minimum 3 directors for a public company.',
                    'hint': 'Check Companies Act 2013'
                }
            ],
            'tax_1': [
                {
                    'id': 'tax_1_1',
                    'question': 'Residential status of an individual is determined based on:',
                    'options': [
                        'Citizenship',
                        'Domicile',
                        'Physical presence in India',
                        'All of the above'
                    ],
                    'correct_answer': 2,
                    'explanation': 'Residential status depends on the number of days of physical presence in India, not citizenship.',
                    'hint': 'Focus on physical presence'
                }
            ],
            'cost_1': [
                {
                    'id': 'cost_1_1',
                    'question': 'What is the formula for Break-Even Point in units?',
                    'options': [
                        'Fixed Costs / Contribution per unit',
                        'Variable Costs / Contribution per unit',
                        'Fixed Costs + Variable Costs',
                        'Total Costs / Units'
                    ],
                    'correct_answer': 0,
                    'explanation': 'Break-Even Point in units = Fixed Costs / Contribution per unit',
                    'hint': 'BEP = FC / CM per unit'
                }
            ]
        }
    
    def get_subjects(self):
        return self.subjects
    
    def get_topics(self, subject_code):
        return self.topics.get(subject_code, [])
    
    def get_mcqs(self, topic_id):
        return self.mcqs.get(topic_id, [])
    
    def get_topic_name(self, topic_id):
        for topics in self.topics.values():
            for topic in topics:
                if topic['id'] == topic_id:
                    return topic['name']
        return "Unknown Topic"
    
    def explain_concept(self, query):
        query_lower = query.lower()
        
        if 'depreciation' in query_lower:
            return """
📘 **DEPRECIATION - COMPLETE EXPLANATION**

**What is Depreciation?**
Depreciation is the systematic allocation of the depreciable amount of an asset over its useful life.

**🔑 Key Points:**
• Applies to tangible fixed assets
• Based on historical cost
• Non-cash expense
• Reduces book value

**📊 Methods:**
1. **Straight Line Method (SLM)** - Equal depreciation every year
2. **Written Down Value (WDV)** - Higher depreciation in early years

**💡 Example:**
Company buys machinery for ₹1,00,000
Useful life: 10 years
Residual value: ₹10,000

Annual Depreciation (SLM) = (1,00,000 - 10,000) / 10 = ₹9,000
"""
        elif 'gst' in query_lower:
            return """
📘 **GST - GOODS AND SERVICES TAX**

**What is GST?**
GST is a comprehensive indirect tax levied on supply of goods and services.

**🏗️ Structure:**
• **CGST** - Central GST
• **SGST** - State GST  
• **IGST** - Integrated GST

**📊 GST Rates:**
• 5% - Essential items
• 12% - Standard goods
• 18% - Most services
• 28% - Luxury items
"""
        else:
            return """
📘 **CONCEPT EXPLANATION**

I'll help you understand this CA Inter concept!

**🔍 What is it?**
This is an important topic in CA Intermediate syllabus.

**🎯 How to Study:**
1. Read from ICAI module
2. Practice problems
3. Attempt MCQs
4. Revise regularly

**📝 Need specific help?**
Ask me targeted questions like:
• "Explain depreciation with example"
• "What is GST and how it works?"
• "Tell me about Section 80C"
"""
    
    def find_related_mcqs(self, query):
        all_mcqs = []
        for mcqs in self.mcqs.values():
            all_mcqs.extend(mcqs)
        
        keywords = query.lower().split()
        related = []
        
        for mcq in all_mcqs:
            question_lower = mcq['question'].lower()
            if any(k in question_lower for k in keywords[:3]):
                related.append(mcq)
                if len(related) >= 3:
                    break
        
        return related

# ==================== DATABASE (SIMPLE VERSION) ====================
class Database:
    """Simple database operations"""
    
    def __init__(self):
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        self.db_file = os.path.join(self.data_dir, "ca_bot.db")
    
    def save_user(self, telegram_id, username, first_name, last_name=""):
        pass
    
    def save_mcq_attempt(self, user_id, topic_id, mcq_id, selected, correct):
        pass
    
    def save_doubt(self, user_id, question, response):
        pass
    
    def get_user_stats(self, user_id):
        return {'total_questions': 0, 'total_correct': 0, 'total_wrong': 0, 'accuracy': 0}

# ==================== UTILITY FUNCTIONS ====================
def calculate_accuracy(correct, total):
    if total == 0:
        return 0.0
    return (correct / total) * 100

def get_performance_level(accuracy):
    if accuracy >= 80:
        return "🌟 EXCELLENT! You're a CA star!"
    elif accuracy >= 60:
        return "👍 GOOD! Keep practicing!"
    elif accuracy >= 40:
        return "📖 NEEDS IMPROVEMENT. Review concepts."
    else:
        return "💪 DON'T GIVE UP! Practice more!"

def validate_input(text, max_length=1000):
    if not text or len(text) > max_length:
        return False
    return True

# ==================== MAIN BOT CLASS ====================
class CABot:
    def __init__(self):
        self.content = CAContent()
        self.db = Database()
        self.user_sessions = {}
        self.VERSION = Config.VERSION
        self.CREATOR = Config.CREATOR
        self.POWERED_BY = Config.POWERED_BY
        
    async def start(self, update, context):
        user = update.effective_user
        
        self.user_sessions[user.id] = {
            'current_subject': None,
            'current_topic': None,
            'topic_name': None,
            'score': 0,
            'total': 0,
            'mcqs': [],
            'current_mcq': 0,
            'history': []
        }
        
        welcome = f"""
🎓 **WELCOME TO CA INTER BOT v{self.VERSION}**

Hey {user.first_name}! 👋

I'm your CA Intermediate exam preparation assistant.

**📚 What I Offer:**
• 📝 MCQ Practice with Explanations
• 💡 Concept Understanding
• 📊 Progress Tracking
• 🎯 Weak Area Identification

**Choose your subject below to start:**

---
⭐ **Powered By:** {self.POWERED_BY}
🔧 **Developed by:** {self.CREATOR}
---
"""
        
        keyboard = [
            [
                InlineKeyboardButton("📚 Accounting", callback_data="sub_accounts"),
                InlineKeyboardButton("⚖️ Business Law", callback_data="sub_law")
            ],
            [
                InlineKeyboardButton("💰 Taxation", callback_data="sub_taxation"),
                InlineKeyboardButton("📊 Costing", callback_data="sub_costing")
            ],
            [
                InlineKeyboardButton("📋 Auditing", callback_data="sub_audit"),
                InlineKeyboardButton("📑 FM & SM", callback_data="sub_fm_sm")
            ],
            [
                InlineKeyboardButton("❓ Ask Doubt", callback_data="ask_doubt"),
                InlineKeyboardButton("📊 My Progress", callback_data="show_progress")
            ],
            [
                InlineKeyboardButton("📝 Practice Test", callback_data="practice_test"),
                InlineKeyboardButton("ℹ️ About", callback_data="about_bot")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def about_bot(self, update, context):
        query = update.callback_query
        await query.answer()
        
        about_text = f"""
ℹ️ **ABOUT THIS BOT**

📚 **CA Intermediate Exam Prep Bot**
Version {self.VERSION}

**👨‍💻 Creator:**
**{self.CREATOR}** - Owner & Developer
⭐ **{self.POWERED_BY}** - Project Lead

**📚 Subjects Covered:**
✅ Accounting
✅ Business Laws
✅ Taxation
✅ Costing
✅ Auditing
✅ FM & SM

---
⭐ **Powered By:** {self.POWERED_BY}
🔧 **Developed with ❤️ by {self.CREATOR}**
"""
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Main", callback_data="back_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            about_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_topics(self, update, context, subject_code):
        query = update.callback_query
        user_id = query.from_user.id
        
        self.user_sessions[user_id]['current_subject'] = subject_code
        subjects = self.content.get_subjects()
        subject_name = subjects.get(subject_code, "Subject")
        topics = self.content.get_topics(subject_code)
        
        if not topics:
            await query.edit_message_text(
                f"❌ No topics available for {subject_name}",
                parse_mode='Markdown'
            )
            return
        
        keyboard = []
        for topic in topics:
            keyboard.append([
                InlineKeyboardButton(
                    f"{topic.get('emoji', '📌')} {topic['name']}",
                    callback_data=f"topic_{topic['id']}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("🔙 Back to Main", callback_data="back_main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"📚 **{subject_name}**\n\nChoose a topic to practice:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def start_mcq(self, update, context, topic_id):
        query = update.callback_query
        user_id = query.from_user.id
        
        mcqs = self.content.get_mcqs(topic_id)
        
        if not mcqs:
            await query.edit_message_text(
                "❌ No MCQs available for this topic yet!",
                parse_mode='Markdown'
            )
            return
        
        topic_name = self.content.get_topic_name(topic_id)
        self.user_sessions[user_id]['current_topic'] = topic_id
        self.user_sessions[user_id]['topic_name'] = topic_name
        self.user_sessions[user_id]['mcqs'] = mcqs
        self.user_sessions[user_id]['current_mcq'] = 0
        self.user_sessions[user_id]['score'] = 0
        self.user_sessions[user_id]['total'] = len(mcqs)
        self.user_sessions[user_id]['history'] = []
        
        await self.display_mcq(update, context, user_id)
    
    async def display_mcq(self, update, context, user_id):
        session = self.user_sessions.get(user_id, {})
        mcqs = session.get('mcqs', [])
        current = session.get('current_mcq', 0)
        total = session.get('total', 0)
        topic_name = session.get('topic_name', 'Topic')
        
        if current >= total:
            await self.show_results(update, context, user_id)
            return
        
        mcq = mcqs[current]
        
        keyboard = []
        for i, option in enumerate(mcq['options']):
            letter = chr(65 + i)
            keyboard.append([
                InlineKeyboardButton(f"{letter}. {option}", callback_data=f"ans_{i}")
            ])
        
        keyboard.append([
            InlineKeyboardButton("📊 Progress", callback_data="show_progress"),
            InlineKeyboardButton("💡 Hint", callback_data=f"hint_{current}")
        ])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            f"📚 **{topic_name}** (Q{current + 1}/{total})\n\n"
            f"📝 **{mcq['question']}**\n\nChoose your answer:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def handle_answer(self, update, context):
        query = update.callback_query
        user_id = query.from_user.id
        selected = int(query.data.replace("ans_", ""))
        
        session = self.user_sessions.get(user_id, {})
        mcqs = session.get('mcqs', [])
        current = session.get('current_mcq', 0)
        
        if current >= len(mcqs):
            return
        
        mcq = mcqs[current]
        is_correct = selected == mcq['correct_answer']
        
        if is_correct:
            session['score'] += 1
        
        session['history'].append({
            'question': mcq['question'],
            'selected': selected,
            'correct': is_correct,
            'correct_answer': mcq['correct_answer'],
            'explanation': mcq.get('explanation', 'No explanation available'),
            'topic': session.get('topic_name', 'Unknown')
        })
        
        feedback = "✅ **CORRECT!**" if is_correct else "❌ **INCORRECT!**"
        correct_answer = mcq['options'][mcq['correct_answer']]
        
        keyboard = [
            [InlineKeyboardButton("➡️ Next Question", callback_data="next_mcq_")],
            [
                InlineKeyboardButton("📊 Progress", callback_data="show_progress"),
                InlineKeyboardButton("🔙 Back", callback_data="back_main")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"{feedback}\n\n"
            f"**Correct Answer:** {correct_answer}\n\n"
            f"**Explanation:**\n{mcq.get('explanation', 'No explanation available')}\n\n"
            f"📊 Score: {session['score']}/{session.get('total', 0)}\n\n"
            f"⭐ **Powere
