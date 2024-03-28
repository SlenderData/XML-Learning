# 本程序用于创建并初始化用于本章上机作业的 SQLite 数据库

import sqlite3

# 连接数据库
conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# 如果已存在的student表，将其删除
cursor.execute('DROP TABLE IF EXISTS student')

# 创建student表，设置id为非空且自增
cursor.execute('''CREATE TABLE student
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   sex TEXT,
                   age INTEGER)''')

# 由于id设置为自增，插入数据时不需要指定id
students = [('tom', 'male', 23),
            ('jack', 'male', 18),
            ('marry', 'female', 22),
            ('kitty', 'female', 19)]

cursor.executemany('INSERT INTO student (name, sex, age) VALUES (?, ?, ?)', students)

# 保存更改并关闭连接
conn.commit()
conn.close()
