import os
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# ===== LOGGING =====
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== CONFIG =====
TOKEN = "8707473118:AAErmBRuzuU9JRR08mE4TNsGDGUWdHwVpxU"
DOUBT_INPUT = 1

# ===== CONTENT =====
subjects = {
    'accounts': 'Accounting',
    'law': 'Law',
    'taxation': 'Taxation',
    'costing': 'Costing',
    'audit': 'Audit',
    'fm_sm': 'FM and SM'
}

topics = {
    'accounts': [
        {'id': 'acc_1', 'name': 'Accounting Standards'},
        {'id': 'acc_2', 'name': 'Company Accounts'},
        {'id': 'acc_3', 'name': 'Consolidation'}
    ],
    'law': [
        {'id': 'law_1', 'name': 'Company Law'},
        {'id': 'law_2', 'name': 'Contract Law'}
    ],
    'taxation': [
        {'id': 'tax_1', 'name': 'Income Tax Basics'},
        {'id': 'tax_2', 'name': 'GST'}
    ],
    'costing': [
        {'id': 'cost_1', 'name': 'Cost Sheet'},
        {'id': 'cost_2', 'name': 'BEP Analysis'}
    ],
    'audit': [
        {'id': 'aud_1', 'name': 'Audit Planning'},
        {'id': 'aud_2', 'name': 'Internal Audit'}
    ],
    'fm_sm': [
        {'id': 'fm_1', 'name': 'Financial Management'},
        {'id': 'fm_2', 'name': 'Working Capital'}
    ]
}

mcqs = {
    'acc_1': [
        {'q': 'Which AS deals with PPE?', 'opts': ['AS 10', 'AS 16', 'AS 7', 'AS 19'], 'ans': 0, 'exp': 'AS 10 deals with PPE.'},
        {'q': 'What is Capital Reserve?', 'opts': ['P and L', 'Liability', 'Reserve and Surplus', 'General'], 'ans': 2, 'exp': 'Shown under Reserves.'}
    ],
    'law_1': [
        {'q': 'Min directors in public company?', 'opts': ['2', '3', '5', '7'], 'ans': 1, 'exp': 'Section 149: min 3.'},
        {'q': 'Max directors in public company?', 'opts': ['10', '15', '20', 'No limit'], 'ans': 1, 'exp': 'Max 15 directors.'}
    ],
    'tax_1': [
        {'q': 'Residential status based on?', 'opts': ['Citizenship', 'Domicile', 'Physical presence', 'All'], 'ans': 2, 'exp': 'Based on physical presence.'},
        {'q': '80C limit is?', 'opts': ['1L', '1.5L', '2L', '2.5L'], 'ans': 1, 'exp': '1.5 lakh is 80C limit.'}
    ],
    'cost_1': [
        {'q': 'BEP formula in units?', 'opts': ['FC/CM', 'VC/CM', 'FC+VC', 'TC/U'], 'ans': 0, 'exp': 'BEP = FC / CM per unit.'}
    ],
    'aud_1': [
        {'q': 'Primary objective of audit?', 'opts': ['Detect fraud', 'Express opinion', 'Prepare stmts', 'Manage'], 'ans': 1, 'exp': 'To express opinion on financials.'}
    ],
    'fm_1': [
        {'q': 'Primary objective of FM?', 'opts': ['Profit max', 'Wealth max', 'Sales max', 'Cost min'], 'ans': 1, 'exp': 'Wealth maximization is primary.'}
    ]
}

def get_topics(subj):
    return topics.get(subj, [])

def get_mcqs(topic_id):
    return mcqs.get(topic_id, [])

def get_topic_name(topic_id):
    for subj in topics.values():
        for t in subj:
            if t['id'] == topic_id:
                return t['name']
    return 'Unknown'

# ===== BOT =====
class Bot:
    def __init__(self):
        self.sessions = {}

    async def start(self, update, context):
        user = update.effective_user
        self.sessions[user.id] = {'subject': None, 'topic': None, 'mcqs': [], 'index': 0, 'score': 0, 'total': 0, 'history': []}
        keyboard = [
            [InlineKeyboardButton('Accounting', callback_data='sub_accounts'), InlineKeyboardButton('Law', callback_data='sub_law')],
            [InlineKeyboardButton('Taxation', callback_data='sub_taxation'), InlineKeyboardButton('Costing', callback_data='sub_costing')],
            [InlineKeyboardButton('Audit', callback_data='sub_audit'), InlineKeyboardButton('FM and SM', callback_data='sub_fm_sm')],
            [InlineKeyboardButton('Doubt', callback_data='doubt'), InlineKeyboardButton('Progress', callback_data='progress')],
            [InlineKeyboardButton('Test', callback_data='test'), InlineKeyboardButton('About', callback_data='about')]
        ]
        msg = f'CA INTER BOT v2.0\n\nHey {user.first_name}! 👋\n\nPowered by: @Introspection007\nDeveloped by: MeNgHeaNg'
        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    async def about(self, update, context):
        q = update.callback_query
        await q.answer()
        await q.edit_message_text('CA Inter Bot v2.0\n\nBy: MeNgHeaNg\nPowered: @Introspection007', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Back', callback_data='back')]]), parse_mode='Markdown')

    async def show_topics(self, update, context, subj):
        q = update.callback_query
        user = q.from_user.id
        self.sessions[user]['subject'] = subj
        ts = get_topics(subj)
        if not ts:
            await q.edit_message_text('No topics.', parse_mode='Markdown')
            return
        keyboard = [[InlineKeyboardButton(t['name'], callback_data=f'topic_{t["id"]}')] for t in ts]
        keyboard.append([InlineKeyboardButton('Back', callback_data='back')])
        await q.edit_message_text(f'{subjects.get(subj)} - Choose topic:', reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    async def start_mcq(self, update, context, topic_id):
        q = update.callback_query
        user = q.from_user.id
        ms = get_mcqs(topic_id)
        if not ms:
            await q.edit_message_text('No MCQs yet.', parse_mode='Markdown')
            return
        name = get_topic_name(topic_id)
        self.sessions[user].update({'topic': topic_id, 'mcqs': ms, 'index': 0, 'score': 0, 'total': len(ms), 'history': []})
        await self.show_mcq(update, context, user)

    async def show_mcq(self, update, context, user):
        s = self.sessions[user]
        if s['index'] >= s['total']:
            await self.results(update, context, user)
            return
        mcq = s['mcqs'][s['index']]
        keyboard = [[InlineKeyboardButton(f'{chr(65+i)}. {opt}', callback_data=f'ans_{i}')] for i, opt in enumerate(mcq['opts'])]
        keyboard.append([InlineKeyboardButton('Progress', callback_data='progress')])
        await update.callback_query.edit_message_text(
            f"{s['topic']} (Q{s['index']+1}/{s['total']})\n\n{mcq['q']}",
            reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown'
        )

    async def handle_ans(self, update, context):
        q = update.callback_query
        user = q.from_user.id
        selected = int(q.data.replace('ans_', ''))
        s = self.sessions[user]
        mcq = s['mcqs'][s['index']]
        correct = selected == mcq['ans']
        if correct:
            s['score'] += 1
        s['history'].append({'q': mcq['q'], 'correct': correct})
        keyboard = [[InlineKeyboardButton('Next', callback_data='next')], [InlineKeyboardButton('Progress', callback_data='progress')]]
        await q.edit_message_text(
            f"{'CORRECT!' if correct else 'INCORRECT!'}\n\nAnswer: {mcq['opts'][mcq['ans']]}\n\n{mcq.get('exp', '')}\n\nScore: {s['score']}/{s['total']}",
            reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown'
        )
        s['index'] += 1

    async def next(self, update, context):
        await self.show_mcq(update, context, update.callback_query.from_user.id)

    async def results(self, update, context, user):
        s = self.sessions[user]
        pct = (s['score']/s['total']*100) if s['total'] > 0 else 0
        level = 'EXCELLENT!' if pct >= 80 else 'GOOD!' if pct >= 60 else 'KEEP PRACTICING!'
        keyboard = [[InlineKeyboardButton('Retry', callback_data=f'retry_{s["topic"]}'), InlineKeyboardButton('Back', callback_data='back')]]
        await update.callback_query.edit_message_text(
            f"QUIZ DONE!\n\nCorrect: {s['score']}\nIncorrect: {s['total']-s['score']}\nScore: {pct:.1f}%\n\n{level}",
            reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown'
        )

    async def retry(self, update, context):
        await self.start_mcq(update, context, update.callback_query.data.replace('retry_', ''))

    async def doubt(self, update, context):
        await update.callback_query.edit_message_text('Ask your doubt:\n- Depreciation\n- GST\n- Section 80C\n- Company Law', parse_mode='Markdown')
        return DOUBT_INPUT

    async def handle_doubt(self, update, context):
        text = update.message.text.lower()
        if 'depreciation' in text:
            ans = 'DEPRECIATION: Cost allocation over useful life. Methods: SLM, WDV.'
        elif 'gst' in text:
            ans = 'GST: CGST, SGST, IGST. Rates: 5%, 12%, 18%, 28%.'
        elif '80c' in text:
            ans = 'SEC 80C: Up to 1.5L deduction. Investments: PPF, LIC, ELSS, NSC.'
        else:
            ans = 'Important CA concept. Refer ICAI module.'
        await update.message.reply_text(ans, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Back', callback_data='back')]]), parse_mode='Markdown')
        return ConversationHandler.END

    async def progress(self, update, context):
        s = self.sessions.get(update.callback_query.from_user.id, {})
        h = s.get('history', [])
        if not h:
            await update.callback_query.edit_message_text('No data yet. Start practicing!', parse_mode='Markdown')
            return
        correct = sum(1 for x in h if x['correct'])
        await update.callback_query.edit_message_text(
            f"PROGRESS\n\nTotal: {len(h)}\nCorrect: {correct}\nAccuracy: {(correct/len(h)*100):.1f}%",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Back', callback_data='back')]]), parse_mode='Markdown'
        )

    async def test(self, update, context):
        q = update.callback_query
        await q.answer()
        user = q.from_user.id
        subj = self.sessions.get(user, {}).get('subject', 'accounts')
        all_mcqs = []
        for t in get_topics(subj):
            all_mcqs.extend(get_mcqs(t['id']))
        if len(all_mcqs) < 3:
            await q.edit_message_text('Not enough MCQs for test.', parse_mode='Markdown')
            return
        test_qs = random.sample(all_mcqs, min(5, len(all_mcqs)))
        self.sessions[user].update({'test': test_qs, 'test_idx': 0, 'test_score': 0, 'test_total': len(test_qs)})
        await self.show_test(update, context, user)

    async def show_test(self, update, context, user):
        s = self.sessions[user]
        if s['test_idx'] >= s['test_total']:
            await self.test_results(update, context, user)
            return
        mcq = s['test'][s['test_idx']]
        keyboard = [[InlineKeyboardButton(f'{chr(65+i)}. {opt}', callback_data=f'tans_{i}')] for i, opt in enumerate(mcq['opts'])]
        await update.callback_query.edit_message_text(
            f"TEST Q{s['test_idx']+1}/{s['test_total']}\n\n{mcq['q']}",
            reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown'
        )

    async def handle_test_ans(self, update, context):
        q = update.callback_query
        user = q.from_user.id
        selected = int(q.data.replace('tans_', ''))
        s = self.sessions[user]
        mcq = s['test'][s['test_idx']]
        correct = selected == mcq['ans']
        if correct:
            s['test_score'] += 1
        await q.answer(f"{'Correct!' if correct else 'Answer: ' + mcq['opts'][mcq['ans']]}", show_alert=True)
        s['test_idx'] += 1
        if s['test_idx'] >= s['test_total']:
            await self.test_results(update, context, user)
        else:
            await self.show_test(update, context, user)

    async def test_results(self, update, context, user):
        s = self.sessions[user]
        pct = (s['test_score']/s['test_total']*100) if s['test_total'] > 0 else 0
        keyboard = [[InlineKeyboardButton('Retry Test', callback_data='test'), InlineKeyboardButton('Back', callback_data='back')]]
        await update.callback_query.edit_message_text(
            f"TEST DONE!\n\nCorrect: {s['test_score']}/{s['test_total']}\nScore: {pct:.1f}%\n\n{'EXCELLENT!' if pct >= 70 else 'KEEP PRACTICING!'}",
            reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown'
        )

    async def handler(self, update, context):
        data = update.callback_query.data
        if data == 'back': await self.start(update, context)
        elif data == 'about': await self.about(update, context)
        elif data == 'doubt': return await self.doubt(update, context)
        elif data == 'progress': await self.progress(update, context)
        elif data == 'test': await self.test(update, context)
        elif data.startswith('sub_'): await self.show_topics(update, context, data.replace('sub_', ''))
        elif data.startswith('topic_'): await self.start_mcq(update, context, data.replace('topic_', ''))
        elif data.startswith('ans_'): await self.handle_ans(update, context)
        elif data.startswith('tans_'): await self.handle_test_ans(update, context)
        elif data.startswith('retry_'): await self.retry(update, context)
        elif data == 'next': await self.next(update, context)

def main():
    app = Application.builder().token(TOKEN).build()
    bot = Bot()
    app.add_handler(CommandHandler('start', bot.start))
    app.add_handler(CommandHandler('help', bot.start))
    app.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(bot.doubt, pattern='^doubt$')],
        states={DOUBT_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_doubt)]},
        fallbacks=[CommandHandler('start', bot.start)]
    ))
    app.add_handler(CallbackQueryHandler(bot.handler))
    print('='*40)
    print('CA INTER BOT v2.0 RUNNING')
    print('Powered by: @Introspection007')
    print('Developed by: MeNgHeaNg')
    print('='*40)
    app.run_polling(allowed_updates=Update.ALL_TYPES, read_timeout=10, write_timeout=10, connect_timeout=10)

if __name__ == '__main__':
    main()
