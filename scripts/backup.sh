#!/bin/bash
# ============================================
# CA INTERMEDIATE BOT - BACKUP SCRIPT
# ============================================

set -e

BACKUP_DIR="data/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.tar.gz"

echo "📦 Creating backup..."

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
if [ -f "data/database/ca_bot.db" ]; then
    cp data/database/ca_bot.db $BACKUP_DIR/ca_bot_$TIMESTAMP.db
    echo "✅ Database backed up"
fi

# Backup MCQ data
if [ -d "data/mcqs" ]; then
    tar -czf $BACKUP_FILE data/mcqs data/subjects $BACKUP_DIR/ca_bot_$TIMESTAMP.db 2>/dev/null || true
    echo "✅ Data backed up to: $BACKUP_FILE"
fi

# Clean old backups (keep last 10)
cd $BACKUP_DIR
ls -t backup_*.tar.gz 2>/dev/null | tail -n +11 | xargs rm -f 2>/dev/null || true
cd -

echo "✅ Backup completed successfully!"
echo "📂 Location: $BACKUP_FILE"
