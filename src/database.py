#!/usr/bin/env python3
"""
Database operations for CA Intermediate Bot
"""

import os
from datetime import datetime
from typing import Dict, List, Optional, Any

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Config

Base = declarative_base()

# ==================== DATABASE MODELS ====================

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(50), unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    total_questions = Column(Integer, default=0)
    total_correct = Column(Integer, default=0)
    total_wrong = Column(Integer, default=0)

class MCQAttempt(Base):
    __tablename__ = 'mcq_attempts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False)
    topic_id = Column(String(50))
    mcq_id = Column(String(50))
    selected_answer = Column(Integer)
    is_correct = Column(Boolean, default=False)
    attempt_time = Column(DateTime, default=datetime.utcnow)

class Doubt(Base):
    __tablename__ = 'doubts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False)
    question = Column(Text, nullable=False)
    response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Progress(Base):
    __tablename__ = 'progress'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False)
    subject = Column(String(50))
    topic = Column(String(50))
    total_attempted = Column(Integer, default=0)
    total_correct = Column(Integer, default=0)
    last_practice = Column(DateTime, default=datetime.utcnow)

# ==================== DATABASE CLASS ====================

class Database:
    def __init__(self):
        os.makedirs('data', exist_ok=True)
        
        self.engine = create_engine(
            Config.DATABASE_URL,
            connect_args={'check_same_thread': False} if 'sqlite' in Config.DATABASE_URL else {}
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.Session()
    
    def save_user(self, telegram_id: str, username: str, first_name: str, last_name: str = '') -> None:
        session = self.get_session()
        try:
            user = session.query(User).filter_by(telegram_id=telegram_id).first()
            if not user:
                user = User(telegram_id=telegram_id, username=username, first_name=first_name, last_name=last_name)
                session.add(user)
            else:
                user.last_active = datetime.utcnow()
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()
    
    def save_mcq_attempt(self, user_id: str, topic_id: str, mcq_id: str, selected: int, correct: bool) -> None:
        session = self.get_session()
        try:
            attempt = MCQAttempt(user_id=user_id, topic_id=topic_id, mcq_id=mcq_id, selected_answer=selected, is_correct=correct)
            session.add(attempt)
            
            user = session.query(User).filter_by(telegram_id=user_id).first()
            if user:
                user.total_questions += 1
                if correct:
                    user.total_correct += 1
                else:
                    user.total_wrong += 1
            
            progress = session.query(Progress).filter_by(user_id=user_id, topic=topic_id).first()
            if not progress:
                progress = Progress(user_id=user_id, topic=topic_id)
                session.add(progress)
            progress.total_attempted += 1
            if correct:
                progress.total_correct += 1
            progress.last_practice = datetime.utcnow()
            
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()
    
    def save_doubt(self, user_id: str, question: str, response: str) -> None:
        session = self.get_session()
        try:
            doubt = Doubt(user_id=user_id, question=question, response=response)
            session.add(doubt)
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        session = self.get_session()
        try:
            user = session.query(User).filter_by(telegram_id=user_id).first()
            if not user:
                return {'total_questions': 0, 'total_correct': 0, 'total_wrong': 0, 'accuracy': 0}
            
            total = user.total_questions
            correct = user.total_correct
            return {
                'total_questions': total,
                'total_correct': correct,
                'total_wrong': user.total_wrong,
                'accuracy': (correct / total * 100) if total > 0 else 0
            }
        except:
            return {}
        finally:
            session.close()
