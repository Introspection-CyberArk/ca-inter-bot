#!/usr/bin/env python3
"""
Utility functions for CA Intermediate Bot
"""

import re
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any

def format_message(text: str, max_length: int = 4000) -> str:
    """Format message to avoid Telegram's length limit"""
    if len(text) <= max_length:
        return text
    
    paragraphs = text.split('\n\n')
    formatted = ""
    for para in paragraphs:
        if len(formatted) + len(para) + 2 <= max_length:
            formatted += para + '\n\n'
        else:
            break
    
    return formatted + "\n\n... (continued)"

def validate_input(text: str, max_length: int = 1000) -> bool:
    """Validate user input"""
    if not text or len(text) > max_length:
        return False
    
    patterns = [
        r'<script.*?>.*?</script>',
        r'on\w+\s*=',
        r'javascript:',
        r'data:',
        r'vbscript:'
    ]
    
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    
    return True

def calculate_accuracy(correct: int, total: int) -> float:
    """Calculate accuracy percentage"""
    if total == 0:
        return 0.0
    return (correct / total) * 100

def get_performance_level(accuracy: float) -> str:
    """Get performance level based on accuracy"""
    if accuracy >= 80:
        return "🌟 EXCELLENT! You're a CA star!"
    elif accuracy >= 60:
        return "👍 GOOD! Keep practicing!"
    elif accuracy >= 40:
        return "📖 NEEDS IMPROVEMENT. Review concepts."
    else:
        return "💪 DON'T GIVE UP! Practice more!"

def sanitize_text(text: str) -> str:
    """Sanitize text for Telegram"""
    text = re.sub(r'<[^>]+>', '', text)
    chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in chars:
        text = text.replace(char, f'\\{char}')
    return text
