#!/usr/bin/env python3
"""
CA Intermediate Exam Bot - Main Application
Created by: MeNgHeaNg
Powered by: @Introspection007
Version: 2.0
"""

import os
import logging
import random
from datetime import datetime
from typing import Dict, List, Optional, Any

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

# Import local modules
from config import Config
from content import CAContent
from database import Database
from utils import (
    format_message,
    validate_input,
    get_performance_level,
    calculate_accuracy,
    sanitize_text
)

# ==================== LOGGING ====================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== CONSTANTS ====================
(SUBJECT, TOPIC, DOUBT_INPUT, TEST_MODE) = range(4)

# ==================== MAIN BOT CLASS ====================
class CABot:
    """CA Intermediate Exam Bot - Main Class"""
    
    def __init__(self):
        """Initialize bot with content and database"""
        self.content = CAContent()
        self.db = Database()
        self.user_sessions = {}
        self.VERSION = Config.VERSION
        self.CREATOR = Config.CREATOR
        self.POWERED_BY = Config.POWERED_BY
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Start command - Show welcome message with credits"""
        user = update.effective_user
        
        # Save user to database
        self.db.save_user(
            telegram_id=str(user.id),
            username=user.username or "Unknown",
            first_name=user.first_name or "User",
            last_name=user.last_name or ""
        )
        
        # Initialize user session
        self.user_sessions[user.id] = {
            'current_subject': None,
            'current_topic': None,
            'topic_name': None,
            'score': 0,
            'total': 0,
            'mcqs': [],
            'current_mcq': 0,
            'history': [],
            'started_at': datetime.now().isoformat(),
            'test_mcqs': [],
            'test_index': 0,
            'test_score': 0,
            'test_total': 0
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
• 📝 Practice Tests
• ❓ Doubt Solving

**Choose your subject below to start:**

---
⭐ **Powered By:** {self.POWERED_BY}
🔧 **Developed by:** {self.CREATOR}
📚 **CA Intermediate - Complete Prep**
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
    
    async def about_bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show about bot with credits"""
        query = update.callback_query
        await query.answer()
        
        about_text = f"""
ℹ️ **ABOUT THIS BOT**

📚 **CA Intermediate Exam Prep Bot**
Version {self.VERSION}

**👨‍💻 Creator:**
**{self.CREATOR}** - Owner & Developer
⭐ **{self.POWERED_BY}** - Project Lead & Creator

**🎯 Purpose:**
Help CA Intermediate students excel in exams through:
• MCQ Practice
• Concept Explanations  
• Progress Tracking
• Practice Tests

**🛠️ Tech Stack:**
• Python 3.11
• python-telegram-bot v20.3
• Render Cloud Hosting
• SQLite Database

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

*"Excellence is not a skill, it's an attitude"*
"""
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Main", callback_data="back_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            about_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_topics(self, update: Update, context: ContextTypes.DEFAULT_TYPE, subject_code: str) -> None:
        """Show topics for selected subject"""
        query = update.callback_query
        user_id = query.from_user.id
        
        self.user_sessions[user_id]['current_subject'] = subject_code
        subjects = self.content.get_subjects()
        subject_name = subjects.get(subject_code, "Subject")
        topics = self.content.get_topics(subject_code)
        
        if not topics:
            await query.edit_message_text(
                f"❌ No topics available for {subject_name}\nTry another subject!",
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
        
        keyboard.append([
            InlineKeyboardButton("🔙 Back to Main", callback_data="back_main"),
            InlineKeyboardButton("ℹ️ About", callback_data="about_bot")
        ])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"📚 **{subject_name}**\n\nChoose a topic to practice:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def start_mcq(self, update: Update, context: ContextTypes.DEFAULT_TYPE, topic_id: str) -> None:
        """Start MCQ practice for a topic"""
        query = update.callback_query
        user_id = query.from_user.id
        
        mcqs = self.content.get_mcqs(topic_id)
        
        if not mcqs:
            await query.edit_message_text(
                "❌ No MCQs available for this topic yet!\nTry another topic.",
                parse_mode='Markdown'
            )
            return
        
        # Update session
        topic_name = self.content.get_topic_name(topic_id)
        self.user_sessions[user_id]['current_topic'] = topic_id
        self.user_sessions[user_id]['topic_name'] = topic_name
        self.user_sessions[user_id]['mcqs'] = mcqs
        self.user_sessions[user_id]['current_mcq'] = 0
        self.user_sessions[user_id]['score'] = 0
        self.user_sessions[user_id]['total'] = len(mcqs)
        self.user_sessions[user_id]['history'] = []
        
        await self.display_mcq(update, context, user_id)
    
    async def display_mcq(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
        """Display current MCQ"""
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
            letter = chr(65 + i)  # A, B, C, D
            keyboard.append([
                InlineKeyboardButton(f"{letter}. {option}", callback_data=f"ans_{i}")
            ])
        
        keyboard.append([
            InlineKeyboardButton("📊 Progress", callback_data="show_progress"),
            InlineKeyboardButton("💡 Hint", callback_data=f"hint_{current}")
        ])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = f"""
📚 **{topic_name}** (Question {current + 1}/{total})

📝 **{mcq['question']}**

Choose your answer:
"""
        
        await update.callback_query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def handle_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle MCQ answer"""
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
        
        # Update stats
        if is_correct:
            session['score'] += 1
        
        # Save history
        session['history'].append({
            'question': mcq['question'],
            'selected': selected,
            'correct': is_correct,
            'correct_answer': mcq['correct_answer'],
            'explanation': mcq.get('explanation', 'No explanation available'),
            'topic': session.get('topic_name', 'Unknown')
        })
        
        # Save to database
        self.db.save_mcq_attempt(
            user_id=str(user_id),
            topic_id=session.get('current_topic', ''),
            mcq_id=mcq.get('id', 'unknown'),
            selected=selected,
            correct=is_correct
        )
        
        # Show feedback
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
        
        # Add credits to feedback
        await query.edit_message_text(
            f"{feedback}\n\n"
            f"**Correct Answer:** {correct_answer}\n\n"
            f"**Explanation:**\n{mcq.get('explanation', 'No explanation available')}\n\n"
            f"📊 Score: {session['score']}/{session.get('total', 0)}\n\n"
            f"⭐ **Powered by:** {self.POWERED_BY}",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        # Move to next MCQ
        session['current_mcq'] = current + 1
    
    async def next_mcq(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Go to next MCQ"""
        query = update.callback_query
        user_id = query.from_user.id
        await self.display_mcq(update, context, user_id)
    
    async def show_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
        """Show MCQ results"""
        session = self.user_sessions.get(user_id, {})
        total = session.get('total', 0)
        score = session.get('score', 0)
        percentage = calculate_accuracy(score, total)
        level = get_performance_level(percentage)
        
        # Get weak areas
        weak_areas = []
        for item in session.get('history', []):
            if not item['correct']:
                question = item['question'][:40] + "..."
                weak_areas.append(question)
        
        result_text = f"""
📊 **QUIZ COMPLETE!**

📝 Topic: {session.get('topic_name', 'Practice')}
✅ Correct: {score}
❌ Incorrect: {total - score}
📈 Score: {percentage:.1f}%

{level}
"""
        
        if weak_areas:
            result_text += f"\n🎯 **Areas for Improvement:**\n"
            for area in weak_areas[:3]:
                result_text += f"• {area}\n"
        
        result_text += f"\n⭐ **Powered by:** {self.POWERED_BY}"
        
        keyboard = [
            [
                InlineKeyboardButton("🔄 Retry", callback_data=f"retry_{session.get('current_topic', '')}"),
                InlineKeyboardButton("📚 New Subject", callback_data="back_main")
            ],
            [InlineKeyboardButton("📊 Full Progress", callback_data="show_progress")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            result_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def retry_topic(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Retry a topic"""
        query = update.callback_query
        user_id = query.from_user.id
        topic_id = query.data.replace("retry_", "")
        await self.start_mcq(update, context, topic_id)
    
    async def ask_doubt(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle doubt asking"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            "🤔 **ASK YOUR DOUBT**\n\n"
            "Type your question or concept name, and I'll explain it with examples!\n\n"
            "*Examples:*\n"
            "• What is depreciation?\n"
            "• Explain GST in detail\n"
            "• How does Section 80C work?\n"
            "• What is a company under Company Law?\n"
            "• Explain audit planning\n\n"
            "💡 *Be specific for better explanations!*\n\n"
            "Type your question now:",
            parse_mode='Markdown'
        )
        return DOUBT_INPUT
    
    async def handle_doubt(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle doubt input with AI-powered explanation"""
        user_input = update.message.text
        user_id = update.effective_user.id
        
        if not validate_input(user_input):
            await update.message.reply_text(
                "⚠️ Please enter a valid question. Avoid special characters or very long messages.",
                parse_mode='Markdown'
            )
            return DOUBT_INPUT
        
        # Get explanation
        explanation = self.content.explain_concept(user_input)
        
        # Find related MCQs
        related = self.content.find_related_mcqs(user_input)
        
        response = explanation
        
        if related:
            response += "\n\n📝 **Related Practice Questions:**\n"
            for i, mcq in enumerate(related[:2], 1):
                response += f"\n{i}. {mcq['question']}"
            
            response += "\n\n*Start a topic to practice these questions!*"
        
        # Add credits
        response += f"\n\n---\n⭐ **Powered by:** {self.POWERED_BY}"
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Main", callback_data="back_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            response,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        # Save doubt to database
        self.db.save_doubt(
            user_id=str(user_id),
            question=user_input,
            response=explanation[:500]  # Save first 500 chars
        )
        
        return ConversationHandler.END
    
    async def show_progress(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show user progress with detailed analytics"""
        query = update.callback_query
        user_id = query.from_user.id
        session = self.user_sessions.get(user_id, {})
        
        # Get database stats
        db_stats = self.db.get_user_stats(str(user_id))
        
        history = session.get('history', [])
        total = len(history)
        
        if total == 0:
            await query.edit_message_text(
                "📊 **NO DATA YET!**\n\n"
                "Start practicing MCQs to track your progress.\n"
                "Your performance will be analyzed automatically.\n\n"
                "📈 **Quick Stats:**\n"
                f"• Total Questions: 0\n"
                f"• Accuracy: 0%\n"
                f"• Topics Covered: 0\n\n"
                "💡 **Tip:** Practice regularly for best results!\n\n"
                f"⭐ **Powered by:** {self.POWERED_BY}",
                parse_mode='Markdown'
            )
            return
        
        correct = sum(1 for h in history if h['correct'])
        percentage = calculate_accuracy(correct, total)
        
        # Topic-wise breakdown
        topic_stats = {}
        for h in history:
            topic = h.get('topic', 'General')
            if topic not in topic_stats:
                topic_stats[topic] = {'total': 0, 'correct': 0}
            topic_stats[topic]['total'] += 1
            if h['correct']:
                topic_stats[topic]['correct'] += 1
        
        progress_text = f"""
📊 **YOUR PROGRESS REPORT**

📝 Total Questions: {total}
✅ Correct: {correct}
❌ Incorrect: {total - correct}
📈 Accuracy: {percentage:.1f}%

📚 **Topics Covered:** {len(topic_stats)}
"""
        
        # Show top topics
        if topic_stats:
            progress_text += "\n📖 **Topic Breakdown:**\n"
            for topic, stats in list(topic_stats.items())[:3]:
                acc = calculate_accuracy(stats['correct'], stats['total'])
                emoji = "🌟" if acc >= 80 else "👍" if acc >= 60 else "📖"
                progress_text += f"• {emoji} {topic}: {acc:.1f}%\n"
        
        progress_text += f"\n⭐ **Powered by:** {self.POWERED_BY}"
        
        keyboard = [
            [InlineKeyboardButton("📝 Practice More", callback_data="back_main")],
            [InlineKeyboardButton("📊 Full Analytics", callback_data="full_analytics")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            progress_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def practice_test(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Generate practice test with random questions"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        session = self.user_sessions.get(user_id, {})
        subject = session.get('current_subject', 'accounts')
        
        # Get all MCQs from subject
        all_mcqs = []
        topics = self.content.get_topics(subject)
        for topic in topics:
            mcqs = self.content.get_mcqs(topic['id'])
            all_mcqs.extend(mcqs)
        
        if len(all_mcqs) < 5:
            await query.edit_message_text(
                "❌ Not enough MCQs for a test!\n"
                f"Need at least 5 questions. Currently: {len(all_mcqs)}\n\n"
                "Try a different subject or practice more topics.",
                parse_mode='Markdown'
            )
            return
     
