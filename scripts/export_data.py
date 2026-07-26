#!/usr/bin/env python3
"""
CA Intermediate Bot - Data Export Script
Export all data in various formats
"""

import os
import sys
import json
import csv
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from content import CAContent

class DataExporter:
    def __init__(self):
        self.content = CAContent()
    
    def export_to_json(self, filename="export_full.json"):
        """Export all data to JSON"""
        data = {
            'subjects': self.content.subjects,
            'topics': self.content.topics,
            'mcqs': self.content.mcqs,
            'exported_at': datetime.now().isoformat(),
            'version': '2.0'
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Data exported to {filename}")
        print(f"   📚 Subjects: {len(data['subjects'])}")
        print(f"   📖 Topics: {sum(len(t) for t in data['topics'].values())}")
        print(f"   📝 MCQs: {sum(len(m) for m in data['mcqs'].values())}")
    
    def export_to_csv(self, filename="export_mcqs.csv"):
        """Export MCQs to CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Topic', 'Question', 'Option A', 'Option B', 'Option C', 'Option D', 'Correct Answer', 'Explanation'])
            
            for topic_id, mcqs in self.content.mcqs.items():
                topic_name = self.content.get_topic_name(topic_id)
                for mcq in mcqs:
                    writer.writerow([
                        topic_name,
                        mcq['question'],
                        mcq['options'][0],
                        mcq['options'][1],
                        mcq['options'][2],
                        mcq['options'][3],
                        mcq['correct_answer'] + 1,
                        mcq.get('explanation', '')
                    ])
        
        print(f"✅ MCQs exported to {filename}")

if __name__ == "__main__":
    exporter = DataExporter()
    
    print("=" * 50)
    print("📊 DATA EXPORT SCRIPT")
    print("⭐ Powered by: @Introspection007")
    print("=" * 50)
    
    exporter.export_to_json()
    exporter.export_to_csv()
