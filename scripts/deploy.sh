#!/bin/bash
# ============================================
# CA INTERMEDIATE BOT - DEPLOYMENT SCRIPT
# Created by: MeNgHeaNg
# Powered by: @Introspection007
# ============================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}🚀 CA INTERMEDIATE BOT DEPLOYMENT${NC}"
echo -e "${BLUE}============================================${NC}"
echo -e "⭐ Powered by: @Introspection007"
echo -e "🔧 Developed by: MeNgHeaNg"
echo -e "${BLUE}============================================${NC}"

# Check Python version
echo -e "\n${YELLOW}[1/6] Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
if [[ $(echo "$python_version" | cut -d. -f1) -lt 3 ]] || [[ $(echo "$python_version" | cut -d. -f2) -lt 8 ]]; then
    echo -e "${RED}❌ Python 3.8+ required! Found: $python_version${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python $python_version found${NC}"

# Check .env file
echo -e "\n${YELLOW}[2/6] Checking environment variables...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found!${NC}"
    echo -e "${YELLOW}Creating .env from .env.example...${NC}"
    cp .env.example .env
    echo -e "${RED}⚠️ Please edit .env and add your TELEGRAM_TOKEN${NC}"
    exit 1
fi

# Load .env
source .env
if [ -z "$TELEGRAM_TOKEN" ] || [ "$TELEGRAM_TOKEN" = "YOUR_BOT_TOKEN_HERE" ]; then
    echo -e "${RED}❌ TELEGRAM_TOKEN not set in .env!${NC}"
    echo -e "${YELLOW}Please add your token to .env file${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Environment variables loaded${NC}"

# Create directories
echo -e "\n${YELLOW}[3/6] Creating required directories...${NC}"
mkdir -p data/mcqs data/subjects data/backups data/database logs
echo -e "${GREEN}✅ Directories created${NC}"

# Install dependencies
echo -e "\n${YELLOW}[4/6] Installing dependencies...${NC}"
pip install -q -r deploy/requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Run database migration
echo -e "\n${YELLOW}[5/6] Running database migration...${NC}"
python3 scripts/migrate_data.py --init
echo -e "${GREEN}✅ Database initialized${NC}"

# Start bot
echo -e "\n${YELLOW}[6/6] Starting bot...${NC}"
echo -e "${BLUE}============================================${NC}"
echo -e "${GREEN}🤖 Bot is starting!${NC}"
echo -e "${BLUE}📚 CA Intermediate Exam Bot v2.0${NC}"
echo -e "${BLUE}⭐ Powered by: @Introspection007${NC}"
echo -e "${BLUE}🔧 Developed by: MeNgHeaNg${NC}"
echo -e "${BLUE}============================================${NC}"

python3 src/bot.py
