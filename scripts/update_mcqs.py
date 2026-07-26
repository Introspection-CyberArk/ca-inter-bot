#!/usr/bin/env python3
"""
CA Intermediate Bot - MCQ Updater Script
Add, update, or delete MCQs from database
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List, Any

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from content import CAContent
from database import Database

class MCQUtils:
    """Utility class for managing MCQs"""
    
    def __init__(self):
        self.content = CAContent()
        self.db = Database()
        self.data_dir = "data/mcqs"
        os.makedirs(self.data_dir, exist_ok=True)
    
    def add_mcq(self, subject: str, topic: str, mcq_data: Dict[str, Any]) -> bool:
        """Add a new MCQ to a topic"""
        try:
            # Get topic ID
            topics = self.content.get_topics(subject)
            topic_obj = None
            for t in topics:
                if t['name'].lower() == topic.lower():
                    topic_obj = t
                    break
            
            if not topic_obj:
                print(f"❌ Topic '{topic}' not found in {subject}")
                return False
            
            topic_id = topic_obj['id']
            
            # Load existing MCQs
            file_path = f"{self.data_dir}/{subject}.json"
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    data = json.load(f)
            else:
                data = {}
            
            # Add MCQ
            if topic_id not in data:
                data[topic_id] = []
            
            # Generate ID
            mcq_id = f"{topic_id}_{len(data[topic_id]) + 1}"
            mcq_data['id'] = mcq_id
            
            data[topic_id].append(mcq_data)
            
            # Save
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ MCQ added: {mcq_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding MCQ: {e}")
            return False
    
    def list_mcqs(self, subject: str = None, topic: str = None):
        """List all MCQs"""
        subjects = self.content.get_subjects()
        
        if subject:
            subjects = {subject: subjects.get(subject, 'Unknown')}
        
        for subj, subj_name in subjects.items():
            print(f"\n📚 {subj_name}")
            topics = self.content.get_topics(subj)
            
            for t in topics:
                if topic and t['name'].lower() != topic.lower():
                    continue
                    
                mcqs = self.content.get_mcqs(t['id'])
                print(f"  ├─ {t['emoji']} {t['name']}: {len(mcqs)} MCQs")
                
                if len(mcqs) > 0:
                    for i, mcq in enumerate(mcqs[:3], 1):
                        print(f"  │  └─ Q{i}: {mcq['question'][:50]}...")
                    if len(mcqs) > 3:
                        print(f"  │  └─ ... and {len(mcqs) - 3} more")
    
    def export_mcqs(self, output_file: str = "exported_mcqs.json"):
        """Export all MCQs to JSON"""
        all_mcqs = {}
        subjects = self.content.get_subjects()
        
        for subj in subjects:
            topics = self.content.get_topics(subj)
            for topic in topics:
                mcqs = self.content.get_mcqs(topic['id'])
                if mcqs:
                    all_mcqs[topic['id']] = mcqs
        
        with open(output_file, 'w') as f:
            json.dump(all_mcqs, f, indent=2)
        
        print(f"✅ Exported {sum(len(m) for m in all_mcqs.values())} MCQs to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='CA Bot MCQ Manager')
    parser.add_argument('--add', action='store_true', help='Add a new MCQ')
    parser.add_argument('--subject', help='Subject name')
    parser.add_argument('--topic', help='Topic name')
    parser.add_argument('--question', help='MCQ question')
    parser.add_argument('--options', nargs=4, help='Four options (A, B, C, D)')
    parser.add_argument('--answer', type=int, help='Correct answer index (0-3)')
    parser.add_argument('--explanation', help='Explanation')
    parser.add_argument('--list', action='store_true', help='List all MCQs')
    parser.add_argument('--export', action='store_true', help='Export all MCQs')
    parser.add_argument('--import-file', help='Import MCQs from JSON file')
    
    args = parser.parse_args()
    
    utils = MCQUtils()
    
    if args.list:
        utils.list_mcqs(args.subject, args.topic)
    
    elif args.export:
        utils.export_mcqs()
    
    elif args.add:
        if not all([args.subject, args.topic, args.question, args.options, args.answer is not None]):
            print("❌ Missing required arguments for --add")
            print("Usage: --add --subject NAME --topic NAME --question Q --options A B C D --answer 0")
            return
        
        mcq = {
            'question': args.question,
            'options': args.options,
            'correct_answer': args.answer,
            'explanation': args.explanation or 'No explanation provided',
            'hint': 'Think about the concept'
        }
        
        utils.add_mcq(args.subject, args.topic, mcq)
    
    elif args.import_file:
        # Import from JSON file
        with open(args.import_file, 'r') as f:
            data = json.load(f)
        
        for topic_id, mcqs in data.items():
            # Find subject and topic
            for subj, topics in utils.content.topics.items():
                for topic in topics:
                    if topic['id'] == topic_id:
                        for mcq in mcqs:
                            utils.add_mcq(subj, topic['name'], mcq)
                        print(f"✅ Imported {len(mcqs)} MCQs to {topic['name']}")
    
    else:
        print("❌ No action specified. Use --list, --add, or --export")
        print("Example: python scripts/update_mcqs.py --list")
        print("Example: python scripts/update_mcqs.py --add --subject accounts --topic 'Accounting Standards' --question 'What is X?' --options A B C D --answer 0 --explanation 'Explanation'")

if __name__ == "__main__":
    main()
