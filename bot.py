#!/usr/bin/env python3
"""
CA INTERMEDIATE EXAM BOT - ULTIMATE FINAL VERSION
Created by: MeNgHeaNg
Powered by: @Introspection007
Version: 3.0
"""

import os
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==================== CONFIGURATION ====================
TOKEN = "8707473118:AAErmBRuzuU9JRR08mE4TNsGDGUWdHwVpxU"
PORT = int(os.environ.get('PORT', 8443))
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== MCQ DATABASE ====================
MCQS = {
    'Auditing': [
        {
            'q': 'The previous auditors did not reply to the communication of the new auditor. Which fundamental principle is not followed?',
            'opts': ['Objectivity', 'Integrity', 'Professional behaviour', 'Professional competence'],
            'ans': 2,
            'exp': 'Not replying violates professional behaviour.'
        },
        {
            'q': 'The auditor did not carry out other audit procedures to justify management treatment. What is lacking?',
            'opts': ['Professional Skepticism', 'Objectivity', 'Integrity', 'Professional Behaviour'],
            'ans': 0,
            'exp': 'Accepting management explanations without evidence shows lack of professional skepticism.'
        },
        {
            'q': 'Providing accounting and bookkeeping services to an audit client creates what threat?',
            'opts': ['Self-interest', 'Self-review', 'Confidentiality', 'Intimidation'],
            'ans': 1,
            'exp': 'The auditor would be reviewing their own work, creating a self-review threat.'
        },
        {
            'q': 'Audited Financial statements provide:',
            'opts': ['Absolute assurance', 'Reasonable assurance', 'No assurance', 'Guarantee'],
            'ans': 1,
            'exp': 'Audit provides reasonable assurance, not absolute.'
        },
        {
            'q': 'An audit file may be kept in:',
            'opts': ['Physical only', 'Electronic only', 'Physical or electronic', 'Both required'],
            'ans': 2,
            'exp': 'SA 230 allows audit documentation in physical or electronic form.'
        },
        {
            'q': 'Sufficiency of audit evidence refers to:',
            'opts': ['Quality', 'Quantity', 'Source', 'Relevance'],
            'ans': 1,
            'exp': 'Sufficiency refers to the quantity of audit evidence.'
        },
        {
            'q': 'Appropriateness of audit evidence refers to:',
            'opts': ['Quality', 'Quantity', 'Source', 'Amount'],
            'ans': 0,
            'exp': 'Appropriateness refers to the quality and relevance of audit evidence.'
        },
        {
            'q': 'As per SA 560, when a fact becomes known after the report date but before issuance, the auditor shall:',
            'opts': ['Modify the opinion', 'Discuss with management', 'Notify shareholders', 'Withdraw'],
            'ans': 1,
            'exp': 'SA 560 requires the auditor to discuss with management to determine if amendments are needed.'
        },
        {
            'q': 'A loan with adequate margin but technically overdue should be classified as:',
            'opts': ['NPA', 'Standard Asset', 'Written off', 'Doubtful'],
            'ans': 1,
            'exp': 'If technically overdue but has adequate margin, it is not classified as NPA.'
        },
        {
            'q': 'The scope of audit includes:',
            'opts': ['Only cash', 'Only P&L', 'All aspects', 'Only statutory'],
            'ans': 2,
            'exp': 'The scope covers all aspects of the entity relevant to financial statements.'
        },
        {
            'q': 'Benefits of audit planning include:',
            'opts': ['Deviating from standards', 'Ignoring important areas', 'Proper organization', 'Eliminating all risks'],
            'ans': 2,
            'exp': 'Audit planning helps in proper organization and efficient management.'
        },
        {
            'q': 'When more persuasive audit evidence is needed, the auditor should:',
            'opts': ['Decrease testing', 'Increase testing', 'Skip procedures', 'Rely on management'],
            'ans': 1,
            'exp': 'To obtain more persuasive evidence, the extent of testing should be increased.'
        },
        {
            'q': 'Attendance at physical inventory counting is:',
            'opts': ['Optional', 'Mandatory unless impracticable', 'Not required', 'Required only for retail'],
            'ans': 1,
            'exp': 'SA 501 requires attendance at physical inventory counting unless impracticable.'
        },
        {
            'q': 'A qualified opinion is issued when misstatements are:',
            'opts': ['Material and pervasive', 'Material but not pervasive', 'Immaterial', 'None'],
            'ans': 1,
            'exp': 'Qualified opinion is issued when misstatements are material but not pervasive.'
        },
        {
            'q': 'An adverse opinion is issued when misstatements are:',
            'opts': ['Material and pervasive', 'Material but not pervasive', 'Immaterial', 'None'],
            'ans': 0,
            'exp': 'Adverse opinion is issued when misstatements are both material and pervasive.'
        },
        {
            'q': 'What is the primary objective of an audit?',
            'opts': ['Detect fraud', 'Express opinion', 'Prepare statements', 'Manage company'],
            'ans': 1,
            'exp': 'The primary objective is to express an opinion on financial statements.'
        },
        {
            'q': 'What is a self-review threat?',
            'opts': ['Financial interest', 'Reviewing own work', 'Close relationship', 'Pressure from client'],
            'ans': 1,
            'exp': 'Self-review threat occurs when the auditor reviews their own work.'
        }
    ],
    'Financial Management': [
        {
            'q': 'What is the formula for Cost of Equity using Gordon model?',
            'opts': ['D1/P0 + g', 'P0/D1 + g', 'D1/P0 - g', 'D0/P0 + g'],
            'ans': 0,
            'exp': 'Gordon model: Ke = (D1 / P0) + g.'
        },
        {
            'q': 'What is the formula for Financial Leverage?',
            'opts': ['EBIT/EBT', 'EBT/EBIT', 'Contribution/EBIT', 'EBIT/Interest'],
            'ans': 0,
            'exp': 'Financial Leverage = EBIT / EBT.'
        },
        {
            'q': 'What is the formula for Operating Leverage?',
            'opts': ['Contribution/EBIT', 'EBIT/Contribution', 'EBIT/EBT', 'EBT/EBIT'],
            'ans': 0,
            'exp': 'Operating Leverage = Contribution / EBIT.'
        },
        {
            'q': 'What is the formula for Combined Leverage?',
            'opts': ['OL x FL', 'OL + FL', 'FL / OL', 'OL - FL'],
            'ans': 0,
            'exp': 'Combined Leverage = Operating Leverage x Financial Leverage.'
        },
        {
            'q': 'What is the formula for EPS?',
            'opts': ['PAT / Shares', 'EBIT / Shares', 'EBT / Shares', 'Contribution / Shares'],
            'ans': 0,
            'exp': 'EPS = PAT / Number of equity shares.'
        },
        {
            'q': 'What does WACC stand for?',
            'opts': ['Weighted Average Cost of Capital', 'Weighted Average Cost of Debt', 'Weighted Average Cost of Equity', 'Weighted Average Cost of Assets'],
            'ans': 0,
            'exp': 'WACC is the weighted average cost of capital.'
        },
        {
            'q': 'What is the formula for after-tax cost of debt?',
            'opts': ['Kd(1-t)', 'Kd(1+t)', 'Kd/(1-t)', 'Kd/(1+t)'],
            'ans': 0,
            'exp': 'After-tax cost of debt = Kd * (1 - Tax Rate).'
        },
        {
            'q': 'What is the formula for Break-Even Point in units?',
            'opts': ['FC / Contribution per unit', 'FC * Contribution per unit', 'VC / Contribution per unit', 'Sales / Contribution per unit'],
            'ans': 0,
            'exp': 'BEP units = Fixed Costs / Contribution per unit.'
        },
        {
            'q': 'What is the formula for P/V Ratio?',
            'opts': ['Contribution / Sales', 'Sales / Contribution', 'FC / Sales', 'VC / Sales'],
            'ans': 0,
            'exp': 'P/V Ratio = Contribution / Sales.'
        },
        {
            'q': 'What is the formula for Margin of Safety?',
            'opts': ['Sales - BEP Sales', 'Sales + BEP Sales', 'Sales / BEP Sales', 'BEP Sales - Sales'],
            'ans': 0,
            'exp': 'Margin of Safety = Actual Sales - Break-Even Sales.'
        }
    ],
    'Strategic Management': [
        {
            'q': 'What is the central core value of DezineFabs business philosophy?',
            'opts': ['Exclusivity', 'Sustainability', 'Profit maximization', 'International expansion'],
            'ans': 1,
            'exp': 'DezineFabs core value is sustainability.'
        },
        {
            'q': 'How did DezineFabs respond to changing customer behavior?',
            'opts': ['Increasing prices', 'Introducing sustainable clothing', 'Ignoring feedback', 'Reducing variety'],
            'ans': 1,
            'exp': 'They responded by launching an eco-friendly clothing line.'
        },
        {
            'q': 'What is a Strategic Alliance?',
            'opts': ['Merger of two companies', 'Relationship between businesses', 'Acquisition', 'Liquidation'],
            'ans': 1,
            'exp': 'A strategic alliance is a relationship between two or more businesses.'
        },
        {
            'q': 'What does SWOT stand for?',
            'opts': ['Strengths, Weaknesses, Opportunities, Threats', 'Strengths, Weaknesses, Options, Trends', 'Sales, Wages, Operations, Taxes', 'Strategy, Work, Organization, Time'],
            'ans': 0,
            'exp': 'SWOT = Strengths, Weaknesses, Opportunities, and Threats.'
        },
        {
            'q': 'What is Market Penetration Strategy?',
            'opts': ['New products in new markets', 'Existing products in existing markets', 'New products in existing markets', 'Existing products in new markets'],
            'ans': 1,
            'exp': 'Market penetration focuses on increasing sales of existing products in existing markets.'
        },
        {
            'q': 'What is Diversification Strategy?',
            'opts': ['New products in new markets', 'Existing products in existing markets', 'New products in existing markets', 'Existing products in new markets'],
            'ans': 0,
            'exp': 'Diversification involves entering new markets with new products.'
        },
        {
            'q': 'What is a Mission Statement?',
            'opts': ['Future vision', 'Current purpose', 'Financial goals', 'Employee policies'],
            'ans': 1,
            'exp': 'A mission statement defines the organization current purpose and objectives.'
        },
        {
            'q': 'What is a Vision Statement?',
            'opts': ['Future aspirations', 'Current purpose', 'Financial goals', 'Employee policies'],
            'ans': 0,
            'exp': 'A vision statement defines the organization desired future state.'
        },
        {
            'q': 'What is a Turnaround Strategy?',
            'opts': ['Expansion', 'Restoring profitability', 'Liquidation', 'Merger'],
            'ans': 1,
            'exp': 'Turnaround strategy is adopted to reverse declining performance.'
        }
    ],
    'Costing': [
        {
            'q': 'What is the formula for Economic Order Quantity (EOQ)?',
            'opts': ['sqrt(2AO/C)', 'sqrt(2AC/O)', 'sqrt(2CO/A)', 'sqrt(AO/2C)'],
            'ans': 0,
            'exp': 'EOQ = sqrt(2 * Annual Demand * Ordering Cost / Carrying Cost).'
        },
        {
            'q': 'What is Activity-Based Costing (ABC)?',
            'opts': ['Costing based on volume', 'Costing based on activities', 'Costing based on time', 'Costing based on materials'],
            'ans': 1,
            'exp': 'ABC assigns overhead costs to products based on activities consumed.'
        },
        {
            'q': 'What is Standard Costing?',
            'opts': ['Actual costs', 'Predetermined costs', 'Historical costs', 'Future costs'],
            'ans': 1,
            'exp': 'Standard costing uses predetermined standards for costs and revenues.'
        },
        {
            'q': 'What is Material Price Variance?',
            'opts': ['Actual Price - Standard Price', 'Actual Quantity - Standard Quantity', 'Actual Cost - Standard Cost', 'Actual Price - Actual Quantity'],
            'ans': 0,
            'exp': 'Material Price Variance = (Actual Price - Standard Price) x Actual Quantity.'
        },
        {
            'q': 'What is Material Usage Variance?',
            'opts': ['Actual Price - Standard Price', 'Actual Quantity - Standard Quantity', 'Actual Cost - Standard Cost', 'Actual Price - Actual Quantity'],
            'ans': 1,
            'exp': 'Material Usage Variance = (Actual Quantity - Standard Quantity) x Standard Price.'
        },
        {
            'q': 'What is a Budget?',
            'opts': ['Historical record', 'Quantitative plan', 'Financial statement', 'Audit report'],
            'ans': 1,
            'exp': 'A budget is a quantitative plan of action for a future period.'
        },
        {
            'q': 'What is a Flexible Budget?',
            'opts': ['Fixed budget', 'Budget that adjusts for activity', 'Budget for one level', 'Budget for all levels'],
            'ans': 1,
            'exp': 'A flexible budget adjusts for changes in activity level.'
        },
        {
            'q': 'What is Process Costing?',
            'opts': ['For unique products', 'For homogeneous products', 'For services', 'For retail'],
            'ans': 1,
            'exp': 'Process costing is used for homogeneous products in continuous production.'
        },
        {
            'q': 'What are Joint Products?',
            'opts': ['Products from same process', 'Products from different processes', 'Main products', 'By-products'],
            'ans': 0,
            'exp': 'Joint products are two or more products produced simultaneously from a common process.'
        },
        {
            'q': 'What is the Net Realizable Value Method?',
            'opts': ['Allocates joint cost based on physical quantity', 'Allocates joint cost based on sales value', 'Allocates joint cost based on final sales value less further costs', 'Allocates joint cost equally'],
            'ans': 2,
            'exp': 'NRV method allocates joint costs based on final sales value less further processing costs.'
        }
    ]
}

# ==================== BOT CLASS ====================
class CABot:
    def __init__(self):
        self.sessions = {}
        self.POWERED_BY = "@Introspection007"
        self.CREATOR = "MeNgHeaNg"
        self.VERSION = "3.0"
        self.subjects = list(MCQS.keys())

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        self.sessions[user.id] = {
            'subject': None,
            'mcqs': [],
            'idx': 0,
            'score': 0,
            'total': 0,
            'history': []
        }
        
        keyboard = []
        for subject in self.subjects:
            keyboard.append([InlineKeyboardButton(f"📚 {subject}", callback_data=f"sub_{subject}")])
        
        keyboard.append([
            InlineKeyboardButton("📊 Progress", callback_data="progress"),
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ])
        
        welcome = f"""
🎓 WELCOME TO CA INTER BOT v{self.VERSION}

Hey {user.first_name}! 👋

I have {sum(len(mcqs) for mcqs in MCQS.values())}+ MCQs from your PDFs!

Choose a subject to start practicing:

---
⭐ Powered by: {self.POWERED_BY}
🔧 Developed by: {self.CREATOR}
"""
        
        await update.message.reply_text(
            welcome,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    async def about(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        about_text = f"""
ℹ️ ABOUT THIS BOT

CA Inter Exam Bot v{self.VERSION}

⭐ Powered by: {self.POWERED_BY}
🔧 Developed by: {self.CREATOR}

📚 {sum(len(mcqs) for mcqs in MCQS.values())}+ MCQs
📚 {len(self.subjects)} Subjects:
• Auditing
• Financial Management
• Strategic Management
• Costing

All questions extracted from ICAI RTPs!
"""
        
        await query.edit_message_text(
            about_text,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back")]]),
            parse_mode='Markdown'
        )

    async def show_topics(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        subject = query.data.replace("sub_", "")
        user = query.from_user.id
        
        self.sessions[user]['subject'] = subject
        mcqs = MCQS.get(subject, [])
        
        if not mcqs:
            await query.edit_message_text(
                "No MCQs for this subject.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back")]])
            )
            return
        
        self.sessions[user]['mcqs'] = mcqs
        self.sessions[user]['idx'] = 0
        self.sessions[user]['score'] = 0
        self.sessions[user]['total'] = len(mcqs)
        self.sessions[user]['history'] = []
        
        await self.show_mcq(update, context, user)

    async def show_mcq(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user: int):
        session = self.sessions[user]
        
        if session['idx'] >= session['total']:
            await self.show_results(update, context, user)
            return
        
        mcq = session['mcqs'][session['idx']]
        
        keyboard = []
        for i, opt in enumerate(mcq['opts']):
            keyboard.append([InlineKeyboardButton(f"{chr(65+i)}. {opt}", callback_data=f"ans_{i}")])
        
        keyboard.append([
            InlineKeyboardButton("💡 Hint", callback_data="hint"),
            InlineKeyboardButton("📊 Progress", callback_data="progress")
        ])
        
        message = f"""
📝 {session['subject']}
Question {session['idx'] + 1}/{session['total']}

{mcq['q']}

Choose your answer:
"""
        
        await update.callback_query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    async def handle_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        user = query.from_user.id
        selected = int(query.data.replace("ans_", ""))
        
        session = self.sessions[user]
        mcq = session['mcqs'][session['idx']]
        is_correct = selected == mcq['ans']
        
        if is_correct:
            session['score'] += 1
        
        session['history'].append({
            'q': mcq['q'],
            'correct': is_correct
        })
        
        keyboard = [
            [InlineKeyboardButton("➡️ Next Question", callback_data="next")],
            [InlineKeyboardButton("📊 Progress", callback_data="progress")]
        ]
        
        feedback = "✅ CORRECT!" if is_correct else "❌ INCORRECT!"
        
        await query.edit_message_text(
            f"{feedback}\n\n"
            f"Correct Answer: {mcq['opts'][mcq['ans']]}\n\n"
            f"Explanation:\n{mcq['exp']}\n\n"
            f"Score: {session['score']}/{session['total']}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
   
