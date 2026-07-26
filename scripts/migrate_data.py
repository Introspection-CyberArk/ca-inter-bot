#!/usr/bin/env python3
"""
CA Intermediate Bot - Data Migration Script
Initialize and migrate database
"""

import os
import sys
import json
import sqlite3
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import Config
from database import Database, Base

class DataMigrator:
    def __init__(self):
        self.db = Database()
        self.data_dir = "data"
        self.create_directories()
    
    def create_directories(self):
        """Create required directories"""
        dirs = [
            f"{self.data_dir}/mcqs",
            f"{self.data_dir}/subjects",
            f"{self.data_dir}/backups",
            f"{self.data_dir}/database",
            "logs"
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
        print("✅ Directories created")
    
    def init_database(self):
        """Initialize database tables"""
        try:
            # Create tables
            Base.metadata.create_all(self.db.engine)
            print("✅ Database tables created")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
    
    def backup_database(self):
        """Backup current database"""
        db_path = "data/database/ca_bot.db"
        if os.path.exists(db_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"data/backups/ca_bot_{timestamp}.db"
            
            # Copy file
            import shutil
            shutil.copy2(db_path, backup_path)
            print(f"✅ Database backed up to: {backup_path}")
        else:
            print("ℹ️ No database to backup")
    
    def import_mcqs_from_json(self):
        """Import MCQs from JSON files"""
        mcq_dir = "data/mcqs"
        if not os.path.exists(mcq_dir):
            return
        
        imported = 0
        for file in os.listdir(mcq_dir):
            if file.endswith('.json'):
                file_path = os.path.join(mcq_dir, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                print(f"📥 Importing from {file}...")
                # This would be expanded to import to database
    
    def run(self, init=False):
        """Run migration"""
        print("=" * 50)
        print("📊 DATA MIGRATION SCRIPT")
        print(f"⭐ Powered by: @Introspection007")
        print("=" * 50)
        
        if init:
            self.backup_database()
            self.init_database()
            self.import_mcqs_from_json()
            print("\n✅ Migration completed successfully!")
        else:
            print("ℹ️ Use --init to initialize database")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', action='store_true', help='Initialize database')
    parser.add_argument('--backup', action='store_true', help='Backup database')
    
    args = parser.parse_args()
    
    migrator = DataMigrator()
    
    if args.init:
        migrator.run(init=True)
    elif args.backup:
        migrator.backup_database()
    else:
        migrator.run()
