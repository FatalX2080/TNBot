# Telegram Notification Bot
This bot is used to track events with a specific due date. Only admins registered with the project's config file have access. Interaction with telegram takes place through the ***aiogram*** library.
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

# :loudspeaker: Usages
Here is an up-to-date list of commands for interacting with the bot:
```
/state - checking the bot's performance  
/add - allows you to add a new record to the storage
/del - allows you to delete a new record in the storage
/log - returns a log file for tracking and monitoring work
/change - allows you to change the news
/print - displays the news for the specified date
/group_print - displays the news for the specified date in the group
/shutdown - allows you to disable the bot 
/next_few_days - allows you to disable the bot
```
All commands except statistics can be executed only on behalf of the administrator. The ADMIN_DEBUG flag allows you to track all user IDs that are trying to interact with the bot.

# :package: Project Structure
```
TNBot
├── bot
│   ├── bot.py
│   ├── filters.py
│   ├── handlers
│   │   ├── commands.py
│   │   ├── handlers.py
│   │   ├── poll.py
│   │   └── strategy.py
│   ├── keyboards.py
│   └── middleware.py
├── config.py
├── data
├── main.py
├── models
│   ├── exceptions.py
│   └── vault.py
├── README.md
├── requirements.txt
└── utils
    ├── backup.py
    ├── clli.py
    ├── help.py
    ├── mdatetime.py
    └── notification.py
```

# :bookmark_tabs: Futures
- Add Record editing
- Сopy warning
- Сatching copies using FuzzyWuzzy
- Сonfiguring doker for fast deployment
- Add birthdays 
- Сreate auto backups by time 