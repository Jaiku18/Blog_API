import sqlite3

connection = sqlite3.connect('data1.db')

cursor = connection.cursor()

# MUST BE INTEGER
# This is the only place where int vs INTEGER matters—in auto-incrementing columns
create_table = "CREATE TABLE IF NOT EXISTS users_table (id INTEGER PRIMARY KEY, username text NOT NULL UNIQUE, password text, postId text, emailID text NOT NULL UNIQUE, phoneNumber text)"
cursor.execute(create_table)
connection.commit()
create_table = "CREATE TABLE IF NOT EXISTS post_table (id INTEGER PRIMARY KEY, user_id int , title text, content text, hashtag text, FOREIGN KEY(user_id) REFERENCES users_table(id))"
cursor.execute(create_table)
connection.commit()
create_table = "CREATE TABLE IF NOT EXISTS comment_table (id INTEGER PRIMARY KEY, post_id int , user_id int, comment text, FOREIGN KEY(user_id) REFERENCES users_table(id), FOREIGN KEY(post_id) REFERENCES post_table(id) )"
cursor.execute(create_table)

insert_table = "insert into users_table values(1,'jai','12345','','jai1811kumar@gmail.com','7550139079')"

cursor.execute(insert_table)
connection.commit()

connection.close()