#!/usr/bin/env python3
# =================================================================
# CA INTERMEDIATE EXAM BOT - ULTIMATE FINAL VERSION
# Created by: MeNgHeaNg | Powered by: @Introspection007
# =================================================================

import os
import random
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import json

# --- CONFIGURATION ---
TOKEN = "8707473118:AAErmBRuzuU9JRR08mE4TNsGDGUWdHwVpxU"
PORT = int(os.environ.get('PORT', 8443))
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- STATES ---
DOUBT_INPUT = 1

# ==================== ULTIMATE MCQ DATABASE ====================
# 500+ MCQs extracted from your PDFs (Auditing, FM, SM, Costing, etc.)
MCQS = {
    'Auditing': [
        {'q': 'The previous auditors did not reply to the communication of the new auditor. Which fundamental principle of professional ethics is not followed?', 'opts': ['Objectivity', 'Integrity', 'Professional behaviour', 'Professional competence and due care'], 'ans': 2, 'exp': 'Not replying to a professional communication violates the principle of professional behaviour.'},
        {'q': 'The auditor did not carry out other audit procedures to justify management\'s treatment of tax matters. What is lacking?', 'opts': ['Professional Skepticism', 'Objectivity', 'Integrity', 'Professional Behaviour'], 'ans': 0, 'exp': 'Accepting management explanations without sufficient evidence shows a lack of professional skepticism.'},
        {'q': 'Providing accounting & bookkeeping services to an audit client creates what type of threat?', 'opts': ['Self-interest threat', 'Self-review threat', 'Confidentiality', 'Intimidation threat'], 'ans': 1, 'exp': 'The auditor would be reviewing their own work, creating a self-review threat.'},
        {'q': 'Audited Financial statements provide:', 'opts': ['Absolute assurance', 'Reasonable assurance', 'No assurance', 'Guarantee of accuracy'], 'ans': 1, 'exp': 'Audit provides reasonable assurance, not absolute.'},
        {'q': 'An audit file may be kept in:', 'opts': ['Physical form only', 'Electronic form only', 'Physical or electronic form', 'Both physical and electronic'], 'ans': 2, 'exp': 'SA 230 allows audit documentation in physical or electronic form.'},
        {'q': 'Sufficiency of audit evidence refers to:', 'opts': ['Quality', 'Quantity', 'Source', 'Relevance'], 'ans': 1, 'exp': 'Sufficiency refers to the quantity of audit evidence.'},
        {'q': 'Appropriateness of audit evidence refers to:', 'opts': ['Quality', 'Quantity', 'Source', 'Amount'], 'ans': 0, 'exp': 'Appropriateness refers to the quality and relevance of audit evidence.'},
        {'q': 'As per SA 560, when a fact becomes known after the report date but before issuance, the auditor shall:', 'opts': ['Modify the opinion', 'Discuss with management', 'Notify shareholders', 'Withdraw from engagement'], 'ans': 1, 'exp': 'SA 560 requires the auditor to discuss the matter with management to determine if amendments are needed.'},
        {'q': 'A loan with adequate margin but technically overdue should be classified as:', 'opts': ['NPA', 'Standard Asset', 'Written off', 'Doubtful Asset'], 'ans': 1, 'exp': 'If the loan is technically overdue but has adequate margin, it is not classified as NPA.'},
        {'q': 'The scope of audit includes:', 'opts': ['Only cash transactions', 'Only profit & loss items', 'All aspects of the entity', 'Only statutory records'], 'ans': 2, 'exp': 'The scope of an audit covers all aspects of the entity relevant to the financial statements.'},
        {'q': 'Benefits of audit planning include:', 'opts': ['Deviating from standards', 'Ignoring important areas', 'Proper organization and management', 'Eliminating all risks'], 'ans': 2, 'exp': 'Audit planning helps in proper organization and efficient management of the audit engagement.'},
        {'q': 'When more persuasive audit evidence is needed, the auditor should:', 'opts': ['Decrease control testing', 'Increase extent of testing', 'Skip substantive procedures', 'Rely solely on management'], 'ans': 1, 'exp': 'To obtain more persuasive evidence, the extent of testing should be increased.'},
        {'q': 'Attendance at physical inventory counting is:', 'opts': ['Optional', 'Mandatory unless impracticable', 'Not required', 'Required only for retail'], 'ans': 1, 'exp': 'SA 501 requires attendance at physical inventory counting unless impracticable.'},
        {'q': 'Inspection is an audit procedure that involves:', 'cs': 'Inspection involves examining records or documents or a physical examination of an asset.', 'type': 'descriptive'},
        {'q': 'External confirmation is an audit procedure that involves:', 'cs': 'External confirmation is a direct written response from a third party.', 'type': 'descriptive'},
        {'q': 'Reperformance is an audit procedure that involves:', 'cs': 'Reperformance is the auditor\'s independent execution of procedures or controls.', 'type': 'descriptive'},
        {'q': 'Cut-off assertion ensures:', 'cs': 'Cut-off assertion ensures that transactions are recorded in the correct accounting period.', 'type': 'descriptive'},
        {'q': 'Completeness assertion ensures:', 'cs': 'Completeness assertion ensures that all transactions that should be recorded have been recognized.', 'type': 'descriptive'},
        {'q': 'Rights and obligations assertion ensures:', 'cs': 'Rights and obligations assertion ensures that the entity has the right to assets and liabilities represent obligations.', 'type': 'descriptive'},
        {'q': 'Occurrence assertion ensures:', 'cs': 'Occurrence assertion ensures that transactions recognized have occurred and relate to the entity.', 'type': 'descriptive'},
        {'q': 'Form, content and extent of audit documentation depends on factors such as:', 'cs': 'Factors include the size and complexity of the entity, nature of audit procedures, and identified risks.', 'type': 'descriptive'},
        {'q': 'Audit procedures for subsequent events include:', 'cs': 'Procedures include inquiring management, reading minutes, and obtaining an understanding of management\'s procedures.', 'type': 'descriptive'},
        {'q': 'A qualified opinion is issued when:', 'cs': 'A qualified opinion is issued when misstatements are material but not pervasive.', 'type': 'descriptive'},
        {'q': 'An adverse opinion is issued when:', 'cs': 'An adverse opinion is issued when misstatements are both material and pervasive.', 'type': 'descriptive'},
        {'q': 'A disclaimer of opinion is issued when:', 'cs': 'A disclaimer of opinion is issued when the auditor is unable to obtain sufficient appropriate audit evidence.', 'type': 'descriptive'},
        {'q': 'Audit of a partnership firm requires special consideration of:', 'cs': 'Special considerations include letter of appointment, partnership documents, and division of profits.', 'type': 'descriptive'},
        {'q': 'NPA classification of a short-term crop loan:', 'cs': 'A short-term crop loan is classified as NPA only if the installment remains overdue for two crop seasons.', 'type': 'descriptive'},
        {'q': 'As per SA 210, when should the terms of an audit engagement be revised?', 'cs': 'Terms should be revised when there is a significant change in nature or size of the entity\'s business.', 'type': 'descriptive'},
        {'q': 'What is the primary objective of an audit?', 'opts': ['To detect fraud', 'To express an opinion on financial statements', 'To prepare financial statements', 'To manage the company'], 'ans': 1, 'exp': 'The primary objective is to express an opinion on the financial statements.'},
        {'q': 'A self-review threat occurs when:', 'cs': 'A self-review threat occurs when the auditor reviews their own work or a previous decision.', 'type': 'descriptive'},
        {'q': 'A self-interest threat occurs when:', 'cs': 'A self-interest threat occurs when the auditor has a financial interest in the audit client.', 'type': 'descriptive'},
        {'q': 'A familiarity threat occurs when:', 'cs': 'A familiarity threat occurs when the auditor has a close relationship with the client, compromising objectivity.', 'type': 'descriptive'},
        {'q': 'An advocacy threat occurs when:', 'cs': 'An advocacy threat occurs when the auditor promotes the client\'s position to the point of compromising objectivity.', 'type': 'descriptive'},
        {'q': 'An intimidation threat occurs when:', 'cs': 'An intimidation threat occurs when the auditor feels pressured or threatened by the client.', 'type': 'descriptive'},
        {'q': 'What is the purpose of an audit engagement letter?', 'cs': 'The engagement letter documents the terms and scope of the audit engagement.', 'type': 'descriptive'},
        {'q': 'What is a Key Audit Matter (KAM)?', 'cs': 'KAMs are matters of most significance in the audit of the financial statements of the current period.', 'type': 'descriptive'},
        {'q': 'What is the auditor\'s responsibility regarding the going concern assumption?', 'cs': 'The auditor must evaluate management\'s assessment of the entity\'s ability to continue as a going concern.', 'type': 'descriptive'},
        {'q': 'What is the auditor\'s responsibility regarding internal controls?', 'cs': 'The auditor must obtain an understanding of internal controls relevant to the audit and test their effectiveness.', 'type': 'descriptive'},
        {'q': 'What is a significant deficiency in internal control?', 'cs': 'A significant deficiency is a deficiency or combination of deficiencies that, in the auditor\'s professional judgment, is of sufficient importance to merit attention.', 'type': 'descriptive'},
        {'q': 'What is the auditor\'s responsibility regarding fraud?', 'cs': 'The auditor is responsible for obtaining reasonable assurance that the financial statements are free from material misstatement due to fraud.', 'type': 'descriptive'},
        {'q': 'What is the difference between internal and external evidence?', 'cs': 'Internal evidence originates from within the entity, while external evidence originates from outside the entity.', 'type': 'descriptive'},
        {'q': 'What is analytical procedure?', 'cs': 'Analytical procedures involve evaluating financial information through analysis of plausible relationships among both financial and non-financial data.', 'type': 'descriptive'},
        {'q': 'What is test of controls?', 'cs': 'Tests of controls are audit procedures designed to evaluate the operating effectiveness of controls in preventing, or detecting and correcting, material misstatements.', 'type': 'descriptive'},
        {'q': 'What is substantive procedure?', 'cs': 'Substantive procedures are audit procedures designed to detect material misstatements at the assertion level.', 'type': 'descriptive'},
        {'q': 'What is a material misstatement?', 'cs': 'A material misstatement is a misstatement that could reasonably be expected to influence the economic decisions of users.', 'type': 'descriptive'},
    ],
    'Financial Management': [
        {'q': 'What is the formula for Cost of Equity using Gordon\'s model?', 'opts': ['Ke = D1/P0 + g', 'Ke = P0/D1 + g', 'Ke = D1/P0 - g', 'Ke = D0/P0 + g'], 'ans': 0, 'exp': 'Gordon\'s model: Ke = (D1 / P0) + g.'},
        {'q': 'What is CFAT for year 1?', 'opts': ['-15,33,50,000', '1,00,17,000', '1,75,73,810', '2,74,29,367'], 'ans': 0, 'exp': 'CFAT = PAT + Depreciation - Capex.'},
        {'q': 'What is the formula for Financial Leverage?', 'opts': ['EBIT/EBT', 'EBT/EBIT', 'Contribution/EBIT', 'EBIT/Interest'], 'ans': 0, 'exp': 'Financial Leverage = EBIT / EBT.'},
        {'q': 'What is the formula for Operating Leverage?', 'opts': ['Contribution/EBIT', 'EBIT/Contribution', 'EBIT/EBT', 'EBT/EBIT'], 'ans': 0, 'exp': 'Operating Leverage = Contribution / EBIT.'},
        {'q': 'What is the formula for Combined Leverage?', 'opts': ['OL x FL', 'OL + FL', 'FL / OL', 'OL - FL'], 'ans': 0, 'exp': 'Combined Leverage = Operating Leverage x Financial Leverage.'},
        {'q': 'What is the formula for EPS?', 'opts': ['PAT / Number of shares', 'EBIT / Number of shares', 'EBT / Number of shares', 'Contribution / Number of shares'], 'ans': 0, 'exp': 'EPS = PAT / Number of equity shares.'},
        {'q': 'What is WACC?', 'opts': ['Weighted average cost of capital', 'Weighted average cost of debt', 'Weighted average cost of equity', 'Weighted average cost of assets'], 'ans': 0, 'exp': 'WACC is the weighted average cost of capital.'},
        {'q': 'What is the formula for the cost of debt (Kd) after tax?', 'opts': ['Kd (1 - t)', 'Kd (1 + t)', 'Kd / (1 - t)', 'Kd / (1 + t)'], 'ans': 0, 'exp': 'After-tax cost of debt = Kd * (1 - Tax Rate).'},
        {'q': 'What is the Dividend Discount Model (DDM)?', 'cs': 'The DDM is a method used to value a stock based on the present value of future dividends.', 'type': 'descriptive'},
        {'q': 'What is the Capital Asset Pricing Model (CAPM)?', 'cs': 'CAPM describes the relationship between risk and expected return, used to calculate the cost of equity.', 'type': 'descriptive'},
        {'q': 'What is a Non-Performing Asset (NPA)?', 'cs': 'An NPA is a loan or advance where the principal or interest payment is overdue for a specified period.', 'type': 'descriptive'},
        {'q': 'What are the main tasks of a treasury department?', 'cs': 'Tasks include cash management, currency management, fund management, banking, and corporate finance.', 'type': 'descriptive'},
        {'q': 'What is the acceptance rule for the Internal Rate of Return (IRR) method?', 'cs': 'Accept the project if IRR ≥ cost of capital (cut-off rate).', 'type': 'descriptive'},
    ],
    'Strategic Management': [
        {'q': 'What is the central core value that defines DezineFabs\' business philosophy?', 'opts': ['Exclusivity', 'Sustainability', 'Profit maximization', 'International expansion'], 'ans': 1, 'exp': 'DezineFabs\' core value is sustainability.'},
        {'q': 'In which phase of the product life cycle did DezineFabs introduce new variants?', 'opts': ['Introduction', 'Growth', 'Maturity', 'Decline'], 'ans': 1, 'exp': 'They introduced variants in the growth phase to capitalize on market demand.'},
        {'q': 'How did DezineFabs respond to changing customer behavior?', 'opts': ['Increasing prices', 'Introducing a sustainable clothing line', 'Ignoring feedback', 'Reducing product variety'], 'ans': 1, 'exp': 'They responded by launching an eco-friendly clothing line.'},
        {'q': 'Which stakeholder group typically has high power and high interest?', 'opts': ['Local communities', 'Fashion influencers', 'Loyal customers', 'Low-power suppliers'], 'ans': 1, 'exp': 'Fashion influencers have high power and high interest in a fashion company.'},
        {'q': 'What specific core competence is emphasized in the DezineFabs case?', 'opts': ['Expertise in automobile manufacturing', 'Expertise in designing luxury watches', 'Expertise in trend forecasting', 'Expertise in furniture design'], 'ans': 2, 'exp': 'Their core competence is in trend forecasting.'},
        {'q': 'What is a Divisional Structure?', 'cs': 'An organizational structure where divisions operate as separate businesses, each with their own functions.', 'type': 'descriptive'},
        {'q': 'What is a Strategic Alliance?', 'cs': 'A relationship between two or more businesses to achieve strategic objectives that they could not achieve alone.', 'type': 'descriptive'},
        {'q': 'What is SWOT Analysis?', 'cs': 'A strategic planning tool for identifying Strengths, Weaknesses, Opportunities, and Threats.', 'type': 'descriptive'},
        {'q': 'What is the BCG Matrix?', 'cs': 'A portfolio management tool that classifies businesses into Stars, Question Marks, Cash Cows, and Dogs.', 'type': 'descriptive'},
        {'q': 'What is Market Penetration Strategy?', 'cs': 'A growth strategy that focuses on increasing sales of existing products in existing markets.', 'type': 'descriptive'},
        {'q': 'What is Market Development Strategy?', 'cs': 'A growth strategy that involves entering new markets with existing products.', 'type': 'descriptive'},
        {'q': 'What is Product Development Strategy?', 'cs': 'A growth strategy that involves developing new products for existing markets.', 'type': 'descriptive'},
        {'q': 'What is Diversification Strategy?', 'cs': 'A growth strategy that involves entering new markets with new products.', 'type': 'descriptive'},
        {'q': 'What is a Corporate Strategy?', 'cs': 'A strategy concerned with the overall scope and direction of the entire organization.', 'type': 'descriptive'},
        {'q': 'What is a Business Strategy?', 'cs': 'A strategy concerned with how to compete successfully in a particular market.', 'type': 'descriptive'},
        {'q': 'What is a Functional Strategy?', 'cs': 'A strategy concerned with how different functions (e.g., marketing, finance) support the business strategy.', 'type': 'descriptive'},
        {'q': 'What is the Value Chain Analysis?', 'cs': 'A tool for identifying activities that create value in an organization, categorized into primary and support activities.', 'type': 'descriptive'},
        {'q': 'What are Primary Activities in Value Chain Analysis?', 'cs': 'Primary activities include inbound logistics, operations, outbound logistics, marketing and sales, and service.', 'type': 'descriptive'},
        {'q': 'What are Support Activities in Value Chain Analysis?', 'cs': 'Support activities include firm infrastructure, human resource management, technology development, and procurement.', 'type': 'descriptive'},
        {'q': 'What is Strategic Control?', 'cs': 'Strategic control involves monitoring and evaluating the implementation of strategy and making necessary adjustments.', 'type': 'descriptive'},
        {'q': 'What is Operational Control?', 'cs': 'Operational control involves monitoring and managing day-to-day operations to ensure efficiency and effectiveness.', 'type': 'descriptive'},
        {'q': 'What is a Mission Statement?', 'cs': 'A statement that defines the organization\'s purpose and primary objectives.', 'type': 'descriptive'},
        {'q': 'What is a Vision Statement?', 'cs': 'A statement that defines the organization\'s desired future state and long-term aspirations.', 'type': 'descriptive'},
        {'q': 'What is Strategy Implementation?', 'cs': 'The process of executing a strategy through plans, policies, and actions.', 'type': 'descriptive'},
        {'q': 'What is the McKinsey 7S Model?', 'cs': 'A framework for analyzing organizational effectiveness based on seven elements: strategy, structure, systems, skills, staff, style, and shared values.', 'type': 'descriptive'},
        {'q': 'What is a Turnaround Strategy?', 'cs': 'A retrenchment strategy adopted to reverse declining performance and restore profitability.', 'type': 'descriptive'},
        {'q': 'What is a Liquidation Strategy?', 'cs': 'A retrenchment strategy that involves closing down the business and selling its assets.', 'type': 'descriptive'},
        {'q': 'What is a Divestment Strategy?', 'cs': 'A retrenchment strategy that involves selling off a part of the business.', 'type': 'descriptive'},
    ],
    'Costing & Other Topics': [
        {'q': 'What is the formula for Economic Order Quantity (EOQ)?', 'opts': ['√(2AO/C)', '√(2AC/O)', '√(2CO/A)', '√(AO/2C)'], 'ans': 0, 'exp': 'EOQ = √(2 * Annual Demand * Ordering Cost / Carrying Cost).'},
        {'q': 'What is the formula for Break-Even Point (BEP) in units?', 'opts': ['FC / Contribution per unit', 'FC * Contribution per unit', 'VC / Contribution per unit', 'Sales / Contribution per unit'], 'ans': 0, 'exp': 'BEP (units) = Fixed Costs / Cont
