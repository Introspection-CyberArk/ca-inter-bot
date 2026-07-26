# =================================================================
# FINAL WORKING BOT.PY - CA INTERMEDIATE EXAM BOT
# Created by: MeNgHeaNg | Powered by: @Introspection007
# =================================================================
import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# --- Configuration ---
TOKEN = "8707473118:AAErmBRuzuU9JRR08mE4TNsGDGUWdHwVpxU"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- States ---
DOUBT_INPUT = 1

# --- Content Database ---
class CAContent:
    def __init__(self):
        self.subjects = {'accounts': '📚 Accounting', 'law': '⚖️ Business Laws', 'taxation': '💰 Taxation'}
        self.topics = {
            'accounts': [{'id': 'acc_1', 'name': 'Accounting Standards', 'emoji': '📖'}],
            'law': [{'id': 'law_1', 'name': 'Company Law', 'emoji': '🏛️'}],
            'taxation': [{'id': 'tax_1', 'name': 'Income Tax Basics', 'emoji': '💵'}]
        }
        self.mcqs = {
            'acc_1': [{'id': 'acc_1_1', 'question': 'Which accounting standard deals with PPE?', 'options': ['AS 10', 'AS 16', 'AS 7', 'AS 19'], 'correct_answer': 0, 'explanation': 'AS 10 deals with PPE.'}],
            'law_1': [{'id': 'law_1_1', 'question': 'Minimum directors in a public company?', 'options': ['2', '3', '5', '7'], 'correct_answer': 1, 'explanation': 'Section 149 requires min 3 directors.'}],
            'tax_1': [{'id': 'tax_1_1', 'question': 'Residential status is based on:', 'options': ['Citizenship', 'Domicile', 'Physical presence', 'All'], 'correct_answer': 2, 'explanation': 'Based on physical presence.'}]
        }
    def get_subjects(self): return self.subjects
    def get_topics(self, subject_code): return self.topics.get(subject_code, [])
    def get_mcqs(self, topic_id): return self.mcqs.get(topic_id, [])
    def get_topic_name(self, topic_id):
        for topics in self.topics.values():
            for topic in topics:
                if topic['id'] == topic_id: return topic['name']
        return "Unknown"
    def explain_concept(self, query):
        if 'depreciation' in query.lower(): return "📘 DEPRECIATION: Systematic cost allocation over useful life."
        elif 'gst' in query.lower(): return "📘 GST: Comprehensive indirect tax with CGST, SGST, IGST."
        else: return "📘 CONCEPT: Important CA Inter topic. Refer ICAI module."
    def find_related_mcqs(self, query):
        all_mcqs = [mcq for mcqs in self.mcqs.values() for mcq in mcqs]
        return [mcq for mcq in all_mcqs if any(k in mcq['question'].lower() for k in query.lower().split()[:3])][:2]

# --- Bot Class ---
class CABot:
    def __init__(self):
        self.content = CAContent()
        self.user_sessions = {}
        self.CREATOR = "MeNgHeaNg"
        self.POWERED_BY = "@Introspection007"

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        self.user_sessions[user.id] = {'current_subject': None, 'current_topic': None, 'mcqs': [], 'current_mcq': 0, 'score': 0, 'total': 0, 'history': []}
        keyboard = [
            [InlineKeyboardButton("📚 Accounting", callback_data="sub_accounts"), InlineKeyboardButton("⚖️ Law", callback_data="sub_law")],
            [InlineKeyboardButton("💰 Taxation", callback_data="sub_taxation")],
            [InlineKeyboardButton("❓ Ask Doubt", callback_data="ask_doubt"), InlineKeyboardButton("📊 Progress", callback_data="show_progress")],
            [InlineKeyboardButton("📝 Practice Test", callback_data="practice_test"), InlineKeyboardButton("ℹ️ About", callback_data="about_bot")]
        ]
        await update.message.reply_text(f"🎓 WELCOME TO CA INTER BOT v2.0\n\nHey {user.first_name}! 👋\n\nI'm your CA exam assistant.\n\n⭐ Powered By: {self.POWERED_BY}\n🔧 Developed by: {self.CREATOR}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    # --- Handlers (All working) ---
    async def about_bot(self, update, context):
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(f"ℹ️ ABOUT\n\nCA Inter Bot v2.0\n\nCreated by: {self.CREATOR}\n⭐ Powered by: {self.POWERED_BY}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_main")]]), parse_mode='Markdown')

    async def show_topics(self, update, context, subject_code):
        query = update.callback_query
        user_id = query.from_user.id
        self.user_sessions[user_id]['current_subject'] = subject_code
        topics = self.content.get_topics(subject_code)
        keyboard = [[InlineKeyboardButton(f"{t['emoji']} {t['name']}", callback_data=f"topic_{t['id']}")] for t in topics]
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_main")])
        await query.edit_message_text(f"📚 {self.content.get_subjects().get(subject_code)}\n\nChoose a topic:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    async def start_mcq(self, update, context, topic_id):
        query = update.callback_query
        user_id = query.from_user.id
        mcqs = self.content.get_mcqs(topic_id)
        if not mcqs:
            await query.edit_message_text("No MCQs available.", parse_mode='Markdown')
            return
        topic_name = self.content.get_topic_name(topic_id)
        self.user_sessions[user_id].update({'current_topic': topic_id, 'topic_name': topic_name, 'mcqs': mcqs, 'current_mcq': 0, 'score': 0, 'total': len(mcqs), 'history': []})
        await self.display_mcq(update, context, user_id)

    async def display_mcq(self, update, context, user_id):
        session = self.user_sessions[user_id]
        mcqs = session['mcqs']
        current = session['current_mcq']
        if current >= session['total']:
            await self.show_results(update, context, user_id)
            return
        mcq = mcqs[current]
        keyboard = [[InlineKeyboardButton(f"{chr(65+i)}. {opt}", callback_data=f"ans_{i}")] for i, opt in enumerate(mcq['options'])]
        keyboard.append([InlineKeyboardButton("📊 Progress", callback_data="show_progress"), InlineKeyboardButton("💡 Hint", callback_data=f"hint_{current}")])
        await update.callback_query.edit_message_text(f"📚 {session['topic_name']} (Q{current+1}/{session['total']})\n\n📝 {mcq['question']}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    async def handle_answer(self, update, context):
        query = update.callback_query
        user_id = query.from_user.id
        selected = int(query.data.replace("ans_", ""))
        session = self.user_sessions[user_id]
        mcq = session['mcqs'][session['current_mcq']]
        is_correct = selected == mcq['correct_answer']
        if is_correct:
            session['score'] += 1
        session['history'].append({'question': mcq['question'], 'correct': is_correct, 'correct_answer': mcq['options'][mcq['correct_answer']], 'explanation': mcq.get('explanation', '')})
        keyboard = [[InlineKeyboardButton("➡️ Next", callback_data="next_mcq_")], [InlineKeyboardButton("📊 Progress", callback_data="show_progress")]]
        await query.edit_message_text(f"{'✅ CORRECT!' if is_correct else '❌ INCORRECT!'}\n\nCorrect Answer: {mcq['options'][mcq['correct_answer']]}\n\nExplanation: {mcq.get('explanation', '')}\n\nScore: {session['score']}/{session['total']}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        session['current_mcq'] += 1

    async def next_mcq(self, update, context):
        await self.display_mcq(update, context, update.callback_query.from_user.id)

    async def show_results(self, update, context, user_id):
        session = self.user_sessions[user_id]
        score, total = session['score'], session['total']
        result_text = f"📊 QUIZ COMPLETE!\n\nTopic: {session.get('topic_name', 'Practice')}\n✅ Correct: {score}\n❌ Incorrect: {total-score}\n📈 Score: {(score/total*100):.1f}%\n\n{'🌟 EXCELLENT!' if score/total >= 0.8 else '👍 GOOD!' if score/total >= 0.6 else '📖 NEEDS IMPROVEMENT'}"
        keyboard = [[InlineKeyboardButton("🔄 Retry", callback_data=f"retry_{session.get('current_topic', '')}"), InlineKeyboardButton("📚 Back", callback_data="back_main")]]
        await update.callback_query.edit_message_text(result_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    async def retry_topic(self, update, context):
        await self.start_mcq(update, context, update.callback_query.data.replace("retry_", ""))

    async def ask_doubt(self, update, context):
        await update.callback_query.edit_message_text("🤔 ASK YOUR DOUBT\n\nType your question:", parse_mode='Markdown')
        return DOUBT_INPUT

    async def handle_doubt(self, update, context):
        explanation = self.content.explain_concept(update.message.text)
        related = self.content.find_related_mcqs(update.message.text)
        response = explanation + ("\n\n📝 Related Questions:\n" + "\n".join([f"{i+1}. {m['question']}" for i, m in enumerate(related)]) if related else "")
        await update.message.reply_text(response, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_main")]]), parse_mode='Markdown')
        return ConversationHandler.END

    async def show_progress(self, update, context):
        session = self.user_sessions.get(update.callback_query.from_user.id, {})
        history = session.get('history', [])
        if not history:
            await update.callback_query.edit_message_text("📊 NO DATA YET!\n\nStart practicing.", parse_mode='Markdown')
            return
        correct = sum(1 for h in history if h['correct'])
        await update.callback_query.edit_message_text(f"📊 YOUR PROGRESS\n\nTotal: {len(history)}\n✅ Correct: {correct}\n📈 Accuracy: {(correct/len(history)*100):.1f}%", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📝 Practice More", callback_data="back_main")]]), parse_mode='Markdown')

    async def practice_test(self, update, context):
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        subject = self.user_sessions.get(user_id, {}).get('current_subject', 'accounts')
        all_mcqs = [mcq for topic in self.content.get_topics(subject) for mcq in self.content.get_mcqs(topic['id'])]
        if len(all_mcqs) < 5:
            await query.edit_message_text("Not enough MCQs for a test!", parse_mode='Markdown')
            return
        test_mcqs = random.sample(all_mcqs, min(5, len(all_mcqs)))
        self.user_sessions[user_id].update({'test_mcqs': test_mcqs, 'test_index': 0, 'test_score': 0, 'test_total': len(test_mcqs)})
        await self.display_test_mcq(update, context, user_id)

    async def display_test_mcq(self, update, context, user_id):
        session = self.user_sessions[user_id]
        if session['test_index'] >= session['test_total']:
            await self.show_test_results(update, context, user_id)
            return
        mcq = session['test_mcqs'][session['test_index']]
        keyboard = [[InlineKeyboardButton(f"{chr(65+i)}. {opt}", callback_data=f"test_ans_{i}")] for i, opt in enumerate(mcq['options'])]
        await update.callback_query.edit_message_text(f"📝 TEST - Q{session['test_index']+1}/{session['test_total']}\n\n{mcq['question']}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    async def handle_test_answer(self, update, context):
        query = update.callback_query
        user_id = query.from_user.id
        selected = int(query.data.replace("test_ans_", ""))
        session = self.user_sessions[user_id]
        mcq = session['test_mcqs'][session['test_index']]
        is_correct = selected == mcq['correct_answer']
        if is_correct:
            session['test_score'] += 1
        await query.answer(f"{'✅ Correct!' if is_correct else '❌ Answer: ' + mcq['options'][mcq['correct_answer']]}", show_alert=True)
        session['test_index'] += 1
        if session['test_index'] >= session['test_total']:
            await self.show_test_results(update, context, user_id)
        else:
            await self.display_test_mcq(update, context, user_id)

    async def show_test_results(self, update, context, user_id):
        session = self.user_sessions[user_id]
        score, total = session['test_score'], session['test_total']
        await update.callback_query.edit_message_text(f"📊 TEST COMPLETE!\n\n✅ Correct: {score}/{total}\n📈 Score: {(score/total*100):.1f}%\n\n{'🌟 EXCELLENT!' if score/total >= 0.7 else '💪 KEEP PRACTICING!'}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Retry Test", callback_data="practice_test"), InlineKeyboardButton("📚 Back", callback_data="back_main")]]), parse_mode='Markdown')

    async def show_hint(self, update, context):
        query = update.callback_query
        user_id = query.from_user.id
        session = self.user_sessions[user_id]
        if session.get('current_mcq', 0) < len(session.get('mcqs', [])):
            await query.answer(f"💡 Hint: {session['mcqs'][session['current_mcq']].get('hint', 'Think about the concept')}", show_alert=True)

    async def callback_query_handler(self, update, context):
        data = update.callback_query.data
        if data == "back_main": await self.start(update, context)
        elif data == "about_bot": await self.about_bot(update, context)
        elif data == "ask_doubt": await self.ask_doubt(update, context)
        elif data == "show_progress": await self.show_progress(update, context)
        elif data == "practice_test": await self.practice_test(update, context)
        elif data.startswith("sub_"): await self.show_topics(update, context, data.replace("sub_", ""))
        elif data.startswith("topic_"): await self.start_mcq(update, context, data.replace("topic_", ""))
        elif data.startswith("ans_"): await self.handle_answer(update, context)
        elif data.startswith("test_ans_"): await self.handle_test_answer(update, context)
        elif data.startswith("retry_"): await self.retry_topic(update, context)
        elif data == "next_mcq_": await self.next_mcq(update, context)
        elif data.startswith("hint_"): await self.show_hint(update, context)

def main():
    app = Application.builder().token(TOKEN).build()
    bot = CABot()
    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(CommandHandler("help", bot.start))
    app.add_handler(ConversationHandler(entry_points=[CallbackQueryHandler(bot.ask_doubt, pattern="^ask_doubt$")], states={DOUBT_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_doubt)]}, fallbacks=[CommandHandler("start", bot.start)]))
    app.add_handler(CallbackQueryHandler(bot.callback_query_handler))
    print("="*50 + "\n🤖 CA INTER BOT v2.0 RUNNING\n" + "="*50 + f"\n⭐ Powered by: {bot.POWERED_BY}\n🔧 Developed by: {bot.CREATOR}")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__": main()
