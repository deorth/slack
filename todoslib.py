#!/home/d3l1r1um/opt/python-3.6.6/bin/python3

import MySQLdb

db = MySQLdb.connect(host="mysql.vasserman.net",
        user="olgavass",
        passwd="zXqAwG2mquFMshVRRZbAVpaWjJv47H",
        db="olgavass")

def get_todos(user_id):

    cur = db.cursor()

    todo_list = {}

    cur.execute("SELECT a.id, a.todo, b.color FROM slack_todos a INNER JOIN slack_todos_priorities b on a.priority = b.id WHERE a.user_id=%s AND a.complete=0 order by a.priority, a.id;", [user_id])

    for row in cur.fetchall():
        todo_id = row[0]
        text = row[1]
        priority_color = row[2]

        todo_list[todo_id] = (priority_color, text)

    db.close()

    return todo_list


def get_all_todos(user_id):

    cur = db.cursor()

    todo_list = {}

    cur.execute("SELECT a.id, a.todo, a.complete, b.color FROM slack_todos a INNER JOIN slack_todos_priorities b on a.priority = b.id WHERE a.user_id=%s order by a.complete, a.priority, a.id;", [user_id])

    for row in cur.fetchall():
        todo_id = row[0]
        text = row[1]
        complete = row[2]
        priority_color = row[3]

        todo_list[todo_id] = (priority_color, text, complete)

    db.close()

    return todo_list

def complete_todo(todo_id, user_id, complete):

    cur = db.cursor()

    if (complete == 1):    

        cur.execute("UPDATE slack_todos SET complete = 1 where id=%s and user_id=%s", (todo_id, user_id))

        if (cur.rowcount == 0):
            result = "{\"text\": \":shit: Something went wrong! No matching task found.\", \"replace_original\": false}"
        else:
            result = "{\"text\": \":boom: Task complete!\", \"replace_original\": false}"

    else:
    
        cur.execute("UPDATE slack_todos SET complete = 0 where id=%s and user_id=%s", (todo_id, user_id))

        if (cur.rowcount == 0):
            result = "{\"text\": \":shit: Something went wrong! No matching task found.\", \"replace_original\": false}"
        else:
            result = "{\"text\": \":confounded: Task marked incomplete...\", \"replace_original\": false}"
            
    db.commit()
        
    return result
