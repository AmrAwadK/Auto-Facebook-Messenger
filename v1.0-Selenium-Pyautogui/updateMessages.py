# This script uses 'friends' table & message templates to update messages in
# 'Messages' Table.

import keyboardMap
import sqlite3

# This code is used to populate the messages table to be sent.

def GenerateMessage(name, adj, gender):
    if gender == 'Male':
        msg_template = 'كل سنه و _صفه_ طيب يا _اسم_ ^_^ طمني اخبارك ايه ؟'
    else:
        msg_template = 'كل سنه و _صفه_ طيبه يا _اسم_ ^_^ طمنيني اخبارك ايه ؟'
    msg = msg_template.replace('_اسم_', name)
    msg = msg.replace('_صفه_', adj)
    return msg    

# Connect to SQL database
connection = sqlite3.connect('FB_Friends.db')
cursor = connection.cursor()

# Create 'Messages' table if it doesn't exist
cursor.execute('CREATE TABLE IF NOT EXISTS \
    Messages(Name TEXT, MessangerLink TEXT, Message TEXT, MappedMessage TEXT, Status TEXT)')

# Select the rows you want to update    
cursor.execute("SELECT Name, NickName, Adjective, Gender, MessengerLink FROM friends")

for row in cursor.fetchall():
    # Generate message from template & data
    msg_arabic = GenerateMessage(row[1], row[2], row[3])
    # Map message to keystrokes on keyboard
    msg_mapped = keyboardMap.MapArabicToKeyboard(msg_arabic)
    # Update 'Messages' Table
    cursor.execute("INSERT INTO Messages \
    VALUES(?,?,?,?,?)",(row[0], row[4], msg_arabic, msg_mapped, 'Done' ))
    connection.commit()

    print('Message updated for: ',row[0])
