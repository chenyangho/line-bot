import os
import psycopg2
# DATABASE_URL = os.environ['postgres://jglgvqhikukisk:285f7a822763e5ae8730a2910c20e4ebbd9954506cc5a4a8b4281729410cc719@ec2-3-216-181-219.compute-1.amazonaws.com:5432/d5l1ehhk24qmdk']
DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a line-booooooot').read()[:-1]
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

# create_table_query = '''CREATE TABLE WORD(
#    word_id serial PRIMARY KEY,
#    user_word VARCHAR (50) UNIQUE NOT NULL,
#    bot_word VARCHAR (50) NOT NULL,
#    created_on TIMESTAMP NOT NULL
# );'''
input_word = "透抽! 是誰"
# select_no = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'word';"
select = "SELECT user_word, bot_word FROM word;"
delete = "DELETE FROM WORD WHERE word_id = 2"
# insert = "INSERT INTO word(word_id,user_word,bot_word,created_on) VALUES(DEFAULT,'嗨','幹嘛啦!?','2021-01-02')"
# update = "UPDATE WORD SET word_id = 2 WHERE word_id = 4"
record = ('透抽', '一隻橘貓啦!', '2021-01-13')
table_columns = '(word_id, user_word, bot_word, created_on)'
postgres_insert_query = f"""INSERT INTO WORD {table_columns} VALUES (DEFAULT, %s, %s, %s);"""

# CREATE TABLE  TEST(
# ID  INT  PRIMARY KEY  AUTO_INCREMENT ,
# NAME  VARCHAR(20)
# ) ;


# cursor.execute(postgres_insert_query, record)
cursor.execute(select)
data = []
while True:
    temp = cursor.fetchone()
    if temp:
        data.append(temp)
    else:
        break

for d in data:
    if d[0] in input_word:
        print(d[1])

conn.commit()

cursor.close()
conn.close()