#!/usr/bin/env python3
"""
CA Intermediate Content Database
Contains subjects, topics, and MCQs
"""

import json
import random
from typing import Dict, List, Optional, Any

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
            # ===== ACCOUNTING MCQS =====
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
            # ===== LAW MCQS =====
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
            # ===== TAXATION MCQS =====
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
            # ===== COSTING MCQS =====
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
    
    def get_subjects(self) -> Dict[str, str]:
        """Get all subjects"""
        return self.subjects
    
    def get_topics(self, subject_code: str) -> List[Dict[str, Any]]:
        """Get topics for a subject"""
        return self.topics.get(subject_code, [])
    
    def get_mcqs(self, topic_id: str) -> List[Dict[str, Any]]:
        """Get MCQs for a topic"""
        return self.mcqs.get(topic_id, [])
    
    def get_topic_name(self, topic_id: str) -> str:
        """Get topic name by ID"""
        for topics in self.topics.values():
            for topic in topics:
                if topic['id'] == topic_id:
                    return topic['name']
        return "Unknown Topic"
    
    def explain_concept(self, query: str) -> str:
        """Explain a concept with detailed examples"""
        query_lower = query.lower()
        
        # DEPRECIATION
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
3. **Units of Production** - Based on actual usage

**💡 Example:**
Company buys machinery for ₹1,00,000
Useful life: 10 years
Residual value: ₹10,000

Annual Depreciation (SLM) = (1,00,000 - 10,000) / 10 = ₹9,000

**📝 Journal Entry:**
