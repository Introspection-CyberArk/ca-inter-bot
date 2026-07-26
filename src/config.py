#!/usr/bin/env python3
"""
Configuration file for CA Intermediate Bot
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Bot configuration"""
    
    # Telegram Bot Token
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'YOUR_BOT_TOKEN_HERE')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/ca_bot.db')
    
    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Bot Settings
    BOT_NAME = "CA Inter Exam Helper"
    BOT_USERNAME = "@ca_inter_exam_bot"
    VERSION = "2.0"
    CREATOR = "MeNgHeaNg"
    POWERED_BY = "@Introspection007"
    
    # Limits
    MAX_MCQS_PER_TOPIC = 50
    MAX_TEST_QUESTIONS = 10
    MAX_HISTORY = 100
    
    # Timeouts
    CONVERSATION_TIMEOUT = 300  # 5 minutes
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if cls.TELEGRAM_TOKEN == "YOUR_BOT_TOKEN_HERE":
            raise ValueError("Please set TELEGRAM_TOKEN in .env file")
        return True
