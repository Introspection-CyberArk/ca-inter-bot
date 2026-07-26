import os
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8707473118:AAErmBRuzuU9JRR08mE4TNsGDGUWdHwVpxU"
DOUBT_INPUT = 1

class CAContent:
    def __init__(self):
        self.subjects = {
            'accounts': '📚 Accounting',
            'law': '⚖️ Business Laws', 
            'taxation': '💰 Taxation',
            'costing': '📊 Costing',
            'audit': '📋 Auditing',
            'fm_sm': '📑 FM & SM'
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
            # ===== ACCOUNTING MCQs =====
            'acc_1': [
                {'id': 'acc_1_1', 'question': 'Which accounting standard deals with Property, Plant and Equipment?', 'options': ['AS 10', 'AS 16', 'AS 7', 'AS 19'], 'correct_answer': 0, 'explanation': 'AS 10 deals with Property, Plant and Equipment.', 'hint': 'Remember AS 10'},
                {'id': 'acc_1_2', 'question': 'What is Capital Reserve?', 'options': ['Credited to P&L', 'Shown as Liability', 'Shown as Reserve & Surplus', 'Transferred to General Reserve'], 'correct_answer': 2, 'explanation': 'Capital reserve is shown under Reserves & Surplus.', 'hint': 'Think Balance Sheet'},
                {'id': 'acc_1_3', 'question': 'Which method is used for consolidation?', 'options': ['Equity method', 'Proportionate method', 'Full consolidation', 'Cost method'], 'correct_answer': 2, 'explanation': 'Full consolidation is used when parent has control.', 'hint': 'Control = Full'},
                {'id': 'acc_1_4', 'question': 'Goodwill is a:', 'options': ['Fixed asset', 'Intangible asset', 'Current asset', 'Liability'], 'correct_answer': 1, 'explanation': 'Goodwill is an intangible asset.', 'hint': 'Can you touch it?'},
                {'id': 'acc_1_5', 'question': 'Depreciation is:', 'options': ['Cash expense', 'Non-cash expense', 'Revenue expense', 'Capital expense'], 'correct_answer': 1, 'explanation': 'Depreciation is a non-cash expense.', 'hint': 'No cash outflow'}
            ],
            'acc_2': [
                {'id': 'acc_2_1', 'question': 'Minimum number of members in a private company?', 'options': ['2', '3', '5', '7'], 'correct_answer': 0, 'explanation': 'Private company needs minimum 2 members.', 'hint': 'Private = 2'},
                {'id': 'acc_2_2', 'question': 'What is share premium?', 'options': ['Revenue reserve', 'Capital reserve', 'Profit', 'Liability'], 'correct_answer': 1, 'explanation': 'Share premium is a capital reserve.', 'hint': 'Capital nature'},
                {'id': 'acc_2_3', 'question': 'Debentures are:', 'options': ['Ownership security', 'Debt security', 'Equity', 'Hybrid'], 'correct_answer': 1, 'explanation': 'Debentures are debt securities.', 'hint': 'Borrowing'}
            ],
            # ===== LAW MCQs =====
            'law_1': [
                {'id': 'law_1_1', 'question': 'Minimum directors in a public company?', 'options': ['2', '3', '5', '7'], 'correct_answer': 1, 'explanation': 'Section 149 requires minimum 3 directors.', 'hint': 'Public = 3'},
                {'id': 'law_1_2', 'question': 'Maximum directors in a public company?', 'options': ['10', '15', '20', 'No limit'], 'correct_answer': 1, 'explanation': 'Maximum 15 directors, can be increased.', 'hint': 'Section 149'},
                {'id': 'law_1_3', 'question': 'What is MOA?', 'options': ['Internal rules', 'Fundamental rules', 'Share rules', 'Meeting rules'], 'correct_answer': 1, 'explanation': 'MOA contains fundamental rules of company.', 'hint': 'Foundation'},
                {'id': 'law_1_4', 'question': 'What is AOA?', 'options': ['Internal management', 'External management', 'Share capital', 'Directors'], 'correct_answer': 0, 'explanation': 'AOA deals with internal management.', 'hint': 'Internal rules'},
                {'id': 'law_1_5', 'question': 'Which act governs companies in India?', 'options': ['Companies Act 1956', 'Companies Act 2013', 'Companies Act 2000', 'Companies Act 1990'], 'correct_answer': 1, 'explanation': 'Companies Act 2013 is the current law.', 'hint': 'Current law'}
            ],
            'law_2': [
                {'id': 'law_2_1', 'question': 'What is a contract?', 'options': ['Agreement', 'Enforceable agreement', 'Promise', 'Deed'], 'correct_answer': 1, 'explanation': 'Contract is an enforceable agreement.', 'hint': 'Legal enforceability'},
                {'id': 'law_2_2', 'question': 'Consideration means:', 'options': ['Free', 'Something in return', 'Gift', 'Donation'], 'correct_answer': 1, 'explanation': 'Consideration is something given in return.', 'hint': 'Quid pro quo'}
            ],
            # ===== TAXATION MCQs =====
            'tax_1': [
                {'id': 'tax_1_1', 'question': 'Residential status is based on:', 'options': ['Citizenship', 'Domicile', 'Physical presence', 'All'], 'correct_answer': 2, 'explanation': 'Based on physical presence in India.', 'hint': 'Days in India'},
                {'id': 'tax_1_2', 'question': 'Basic exemption limit for individual below 60?', 'options': ['₹2,50,000', '₹3,00,000', '₹5,00,000', '₹10,00,000'], 'correct_answer': 0, 'explanation': '₹2,50,000 is the limit.', 'hint': '2.5 lakh'},
                {'id': 'tax_1_3', 'question': 'Section 80C limit is:', 'options': ['₹1,00,000', '₹1,50,000', '₹2,00,000', '₹2,50,000'], 'correct_answer': 1, 'explanation': '₹1,50,000 is the 80C limit.', 'hint': '1.5 lakh'},
                {'id': 'tax_1_4', 'question': 'What is TDS?', 'options': ['Tax at source', 'Tax deduction at source', 'Tax on deposit', 'Tax on service'], 'correct_answer': 1, 'explanation': 'TDS means Tax Deduction at Source.', 'hint': 'Deduction'},
                {'id': 'tax_1_5', 'question': 'What is GST?', 'options': ['Goods Service Tax', 'General Sales Tax', 'Government Service Tax', 'Goods Sales Tax'], 'correct_answer': 0, 'explanation': 'GST = Goods and Services Tax.', 'hint': 'S = Services'}
            ],
            'tax_3': [
                {'id': 'tax_3_1', 'question': 'CGST is collected by:', 'options': ['State', 'Central', 'Both', 'Local'], 'correct_answer': 1, 'explanation': 'CGST is collected by Central Government.', 'hint': 'C = Central'},
                {'id': 'tax_3_2', 'question': 'SGST is collected by:', 'options': ['State', 'Central', 'Both', 'Local'], 'correct_answer': 0, 'explanation': 'SGST is collected by State Government.', 'hint': 'S = State'},
                {'id': 'tax_3_3', 'question': 'IGST is applicable on:', 'options': ['Intra-state', 'Inter-state', 'Both', 'Local'], 'correct_answer': 1, 'explanation': 'IGST applies on inter-state transactions.', 'hint': 'I = Inter-state'}
            ],
            # ===== COSTING MCQs =====
            'cost_1': [
                {'id': 'cost_1_1', 'question': 'BEP formula in units?', 'options': ['FC/CM per unit', 'VC/CM per unit', 'FC+VC', 'TC/U'], 'correct_answer': 0, 'explanation': 'BEP = FC / Contribution per unit.', 'hint': 'FC / CM'},
                {'id': 'cost_1_2', 'question': 'Fixed cost is:', 'options': ['Variable', 'Constant', 'Semi-variable', 'Step'], 'correct_answer': 1, 'explanation': 'Fixed cost remains constant.', 'hint': 'No change'},
                {'id': 'cost_1_3', 'question': 'Variable cost:', 'options': ['Constant', 'Changes with output', 'Fixed', 'Mixed'], 'correct_answer': 1, 'explanation': 'Variable cost changes with output.', 'hint': 'Changes'},
                {'id': 'cost_1_4', 'question': 'Contribution =', 'options': ['Sales - VC', 'Sales - FC', 'Sales - TC', 'Profit + FC'], 'correct_answer': 0, 'explanation': 'Contribution = Sales - Variable Cost.', 'hint': 'S - VC'}
            ],
            'cost_2': [
                {'id': 'cost_2_1', 'question': 'BEP in value =', 'options': ['FC/PV Ratio', 'VC/PV Ratio', 'FC * PV', 'Profit/PV'], 'correct_answer': 0, 'explanation': 'BEP in value = Fixed Cost / PV Ratio.', 'hint': 'FC / PV'},
                {'id': 'cost_2_2', 'question': 'PV Ratio =', 'options': ['CM/Sales', 'FC/Sales', 'VC/Sales', 'Profit/Sales'], 'correct_answer': 0, 'explanation': 'PV Ratio = Contribution / Sales.', 'hint': 'CM/S'}
            ],
            # ===== AUDIT MCQs =====
            'aud_1': [
                {'id': 'aud_1_1', 'question': 'Primary objective of audit?', 'options': ['Detect fraud', 'Express opinion', 'Prepare statements', 'Manage company'], 'correct_answer': 1, 'explanation': 'To express opinion on financial statements.', 'hint': 'Opinion'},
                {'id': 'aud_1_2', 'question': 'Internal audit is:', 'options': ['Mandatory', 'Voluntary', 'Required by law', 'Optional'], 'correct_answer': 0, 'explanation': 'Internal audit is mandatory for certain companies.', 'hint': 'Compulsory'},
                {'id': 'aud_1_3', 'question': 'Statutory audit is:', 'options': ['Voluntary', 'Mandatory', 'Optional', 'Internal'], 'correct_answer': 1, 'explanation': 'Statutory audit is mandatory by law.', 'hint': 'Law requires'}
            ],
            'aud_2': [
                {'id': 'aud_2_1', 'question': 'Internal control means:', 'options': ['Policies', 'Procedures', 'Both', 'None'], 'correct_answer': 2, 'explanation': 'Internal control includes policies and procedures.', 'hint': 'Both'},
                {'id': 'aud_2_2', 'question': 'Audit evidence should be:', 'options': ['Sufficient', 'Appropriate', 'Both', 'None'], 'correct_answer': 2, 'explanation': 'Evidence must be sufficient and appropriate.', 'hint': 'Both required'}
            ],
            # ===== FM & SM MCQs =====
            'fm_1': [
                {'id': 'fm_1_1', 'question': 'Primary objective of FM?', 'options': ['Profit maximization', 'Wealth maximization', 'Sales maximization', 'Cost minimization'], 'correct_answer': 1, 'explanation': 'Wealth maximization is the primary objective.', 'hint': 'Shareholder wealth'},
                {'id': 'fm_1_2', 'question': 'Capital budgeting deals with:', 'options': ['Short-term', 'Long-term', 'Both', 'None'], 'correct_answer': 1, 'explanation': 'Capital budgeting deals with long-term decisions.', 'hint': 'Long-term'},
                {'id': 'fm_1_3', 'question': 'Working capital means:', 'options': ['Fixed assets', 'Current assets', 'Current liabilities', 'Both B & C'], 'correct_answer': 3, 'explanation': 'Working capital = Current Assets - Current Liabilities.', 'hint': 'CA - CL'},
                {'id': 'fm_1_4', 'question': 'Strategic management deals with:', 'options': ['Short-term', 'Long-term', 'Day-to-day', 'Operational'], 'correct_answer': 1, 'explanation': 'Strategic management is long-term in nature.', 'hint': 'Long-term vision'}
            ],
            'fm_2': [
                {'id': 'fm_2_1', 'question': 'Gross working capital =', 'options': ['Current assets', 'Current liabilities', 'Fixed assets', 'Total assets'], 'correct_answer': 0, 'explanation': 'Gross working capital = Current Assets.', 'hint': 'Gross = CA'},
                {'id': 'fm_2_2', 'question': 'Net working capital =', 'options': ['CA - CL', 'CA + CL', 'FA - CL', 'FA + CL'], 'correct_answer': 0, 'explanation': 'Net working capital = Current Assets - Current Liabilities.', 'hint': 'CA - CL'}
            ]
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
        q = query.lower()
        if 'depreciation' in q:
            return "📘 DEPRECIATION: Systematic allocation of cost over useful life. Methods: SLM, WDV."
        if 'gst' in q:
            return "📘 GST: Comprehensive indirect tax. Types: CGST, SGST, IGST. Rates: 5%, 12%, 18%, 28%."
        if 'section 80c' in q or '80c' in q:
            return "📘 SECTION 80C: Tax deduction up to ₹1,50,000. Eligible investments: PPF, LIC, ELSS, NSC, etc."
        if 'company law' in q:
            return "📘 COMPANY LAW: Governed by Companies Act 2013. Key sections: 149 (Directors), 180 (Board powers)."
        if 'audit' in q:
            return "📘 AUDIT: Independent examination of financial statements. Types: Statutory, Internal, Tax."
        return "📘 CONCEPT: Important CA Inter topic. Refer ICAI module. Practice MCQs for better understanding!"

    def find_related_mcqs(self, query):
        all_mcqs = [mcq for mcqs in self.mcqs.values() for mcq in mcqs]
        keywords = query.lower().split()
        related = []
        for mcq in all_mcqs:
            q_lower = mcq['question'].lower()
            if any(k in q_lower for k in keywords[:3]):
                related.append(mcq)
                if len(related) >= 3:
                    break
        return related

class CABot:
    def __init__(self):
        self.content = CAContent()
        self.user_sessions = {}
        self.CREATOR = "MeNgHeaNg"
        self.POWERED_BY = "@Introspection007"

    async def start(self, update, context):
        user = update.effective_user
        self.user_sessions[user.id] = {
            'current_subject': None, 'current_topic': None, 'topic_name': None,
            'mcqs': [], 'current_mcq': 0, 'score': 0, 'total': 0, 'history': []
        }
        keyboard = [
            [InlineKeyboardButton("📚 Accounting", callback_data="sub_accounts"), InlineKeyboardButton("⚖️ Law", callback_data="sub_law")],
            [InlineKeyboardButton("💰 Taxation", callback_data="sub_taxation"), InlineKeyboardButton("📊 Costing", callback_data="sub_costing")],
            [InlineKeyboardButton("📋 Audit", callback_data="sub_audit"), InlineKeyboardButton("📑 FM & SM", callback_data="sub_fm_sm")],
            [InlineKeyboardButton("❓ Ask Doubt", callback_data="ask_doubt"), InlineKeyboardButton("📊 Progress", callback_data="show_progress")],
            [InlineKeyboardButton("📝 Practice Test", callback_data="practice_test"), InlineKeyboardButton("ℹ️ About", callback_data="about_bot")]
        ]
        await update.message.reply_text(
            f"🎓 WELCOME TO CA INTER BOT v2.0\n\nHey {user.first_name}! 👋\n\nI'm your CA exam assistant with 50+ MCQs!\n\n⭐ Powered By: {self.POWERED_BY}\n🔧 Developed by: {self.CREATOR}",
            reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    async def about_bot(self, update, context):
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            f"ℹ️ ABOUT\n\nCA Inter Bot v2.0\n\nCreated by: {self.CREATOR}\n⭐ Powered by: {self.POWERED_BY}\n\n📚 50+ MCQs\n📚 6 Subjects\n📚 20+ Topics",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_main")]]),
            parse_mode='Markdown')

    async def show_topics(self, update, context, subject_code):
        query = update.callback_query
        user_id = query.from_user.id
        self.user_sessions[user_id]['current_subject'] = subject_code
        topics = self.content.get_topics(subject_code)
        keyboard = [[InlineKeyboardButton(f"{t['emoji']} {t['name']}", callback_data=f"topic_{t['id']}")] for t in topics]
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_main")])
        await query.edit_message_text(
            f"📚 {self.content.get_subjects().get(subject_code)}\n\nChoose a topic:",
            reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    async def start_mcq(self, update, context, topic_id):
        query = update.callback_query
        user_id = query.from_user.id
        mcqs = self.content.get_mcqs(topic_id)
        if not mcqs:
            await query.edit_message_text("No MCQs available for this topic yet.", parse_mode='Markdown')
            return
        topic_name = self.content.get_topic_name(topic_id)
        self.user_sessions[user_id].update({
            'current_topic': topic_id, 'topic_name': topic_name,
            'mcqs': mcqs, 'current_mcq': 0, 'score': 0, 'total': len(mcqs), 'history': []
        })
        await self.display_mcq(update, context, user_id)

    async def display_mcq(self, update, context, user_id):
        session = self.user_sessions[user_id]
        if session['current_mcq'] >= session['total']:
            await self.show_results(update, context, user_id)
            return
        mcq = session['mcqs'][session['current_mcq']]
        keyboard = [[InlineKeyboardButton(f"{chr(65+i)}. {opt}", callback_data=f"ans_{i}")] for i, opt in enumerate(mcq['options'])]
        keyboard.append([InlineKeyboardButton("📊 Progress", callback_data="show_progress"), InlineKeyboardButton("💡 Hint", callback_data=f"hint_{session['current_mcq']}")])
        await update.callback_query.edit_message_text(
            f"📚 {session['topic_name']} (Q{session['current_mcq']+1}/{session['total']})\n\n📝 {mcq['question']}",
            reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    async def handle_answer(self, update, context):
        query = update.callback_query
        user_id = query.from_user.id
        selected = int(query.data.replace("ans_", ""))
        session = self.user_sessions[user_id]
        mcq = session['mcqs'][session['current_mcq']]
        is_correct = selected == mcq['correct_answer']
        if is_correct: session['score'] += 1
        session['history'].append({'question': mcq['question'], 'correct': is_correct, 'explanation': mcq.get('explanation', '')})
        keyboard = [[InlineKeyboardButton("➡️ 
