#!/bin/bash

# تنظیم متغیرهای محیطی
export PYTHONUNBUFFERED=1
export PYTHONPATH=$PYTHONPATH:$(pwd)

# ایجاد فایل لاگ
mkdir -p logs
touch logs/bot.log

# اجرای ربات
while true; do
    echo "Starting bot..."
    python telegram_gemini_bot_amirrezatube.py >> logs/bot.log 2>&1
    if [ $? -eq 0 ]; then
        echo "Bot exited normally. Restarting in 5 seconds..."
    else
        echo "Bot crashed. Restarting in 5 seconds..."
    fi
    sleep 5
done 