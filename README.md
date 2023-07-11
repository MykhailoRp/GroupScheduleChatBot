# GroupScheduleChatBot
*This bot was created to manage schedule of a university group and create queues for specified lessons*

## Description
In this work, the task was to create a telegram bot to send notifications to users about the start of classes and create queues for the corresponding classes. The bot had to be able to send messages 5 minutes before the start of the lesson, at the start, and at the end. Notifications should be personalized for each user, and each user should be able to customize individual notifications.
One of the key elements of the developed program is a queuing system with priorities. The queues are divided according to priority, where students in the group who are ready to take the test the fastest have the highest priority, followed by students who want to take the test later, and then students from other groups. The process of advancing the queue is based on the confirmation of the student who is currently in charge or the administrator.

The program uses JSON and pickle formats to store information about students. This allows you to store data in a format convenient for further use and prevents data loss.

To accomplish this task, I used the asyncio, aiogram, json, and pickle libraries. Asyncio is used for asynchronous programming, aiogram is used to create bot telegrams and interact with the Telegram API, and json and pickle are used to work with data storage formats.

As a result of the work, I successfully developed a Telegram bot that sends personalized messages to users about the beginning of pairs and creates queues for the corresponding pairs. The bot is able to work asynchronously, which allows it to perform its tasks efficiently. In addition, the program stores student data in a format that is easy to read and use for further analysis.

Thus, the developed Telegram bot is an effective tool for notifying students about classes, organizing queues, and providing information about the status of the Moodle website. It can be useful in educational institutions where timely information and organization of the learning process are important.

## Setup
1. Run "pip install -r requirements.txt" in command line
2. Run setup.py to start setup process
3. Enter asked information in set format
4. Start bot from the same terminal or with start.py

## Features

- Authorisation with name data
- Creation of queues for specified lessons
  - Separate queue for students from other groups
  - Separate queue for students that want to answer now and later
  - Queue admin control
  - Queue notifications
- Notification settings for users
