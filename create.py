from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
# print(MySQL)
app = Flask(__name__)
app.config['MySQL_HOST'] = 'localhost'
app.config['MySQL_USER'] = 'saydotech'
app.config['MySQL_PASSWORD'] = ''
app.config['MySQL_DB'] = 'end_db'
mysql = MySQL(app)

@app.route('/create', methods=['POST'])
def dataSet():
    cur = mysql.connection.cursor()
    cur.execute(f"""CREATE DATABASE `end_db`""")
    mysql.connection.commit()
    return "database created"
@app.route('/create/tab', methods=['POST'])
def tableCreate():
    cur = mysql.connection.cursor()
    cur.execute(f"""USE `end_db`""")
    cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS `create_note`(
                     `id` INT PRIMARY KEY AUTO_INCREMENT,
                      `note_title` VARCHAR(100) NOT NULL,
                       `note_content` LONGTEXT,
                       `author` VARCHAR(50),
                        `created_at` timestamp DEFAULT current_time
                    );
                 """)
    mysql.connection.commit()
    return("table created successfully")

@app.route('/create/insert', methods=['POST','GET'])
def createNote():
    cur = mysql.connection.cursor()
    cur.execute("""USE `end_db`""")
    if request.method == 'POST':
        id = request.json['id']
        note_title = request.json['note_title']
        note_content = request.json['note_content']
        author = request.json['author']
        created_at = request.json['created_at']
        cur.execute(f"""INSERT INTO `create_note` VALUES (%s, %s, %s, %s, %s)""",
                    (id, note_title, note_content, author, created_at))
        mysql.connection.commit()
        return jsonify([id, note_title, note_content, author, created_at])
    elif request.method == "GET":
        cur.execute(f"""SELECT * FROM `create_note`""")
        feedback = cur.fetchall()
        mysql.connection.commit()
        return jsonify(feedback)
    

# # app.config['MySQL_CURSORCLASS'] = 'DictCursor'
# 
# # create note
# @app.route("/post", methods=['POST'])
# def create():
#     if request.method == 'GET':
#         return (f'wrong request method')
#     elif request.method == 'POST':
#         cur = mysql.connection.cursor()
#         id = ''
#         email = request.json['email']
#         password = request.json['password']
#         firstName = request.json['firstName']
#         lastname = request.json['lastname']
#         date = 'now()'
#         cur.execute("""use blog_db""")
#         cur.execute(f"""INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s)""",
#                     (id, email, password, firstName, lastname, date))
#         mysql.connection.commit()
#         cur.close()
#         return (f"note ccreated")

# @app.route("/read", methods=['GET'])
# def read():
    
#     cur = mysql.connection.cursor()
#     cur.execute('''use python_db''')
#     cur.execute('''SELECT * FROM pyusers''')
#     mysql.connection.commit()
#     fetchdata = cur.fetchall()
#     cur.close()
#     return jsonify(fetchdata)


if (__name__ == '__main__'):
    app.run(debug=True)