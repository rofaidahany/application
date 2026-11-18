from flask import Flask, jsonify, request
import sqlite3



app = Flask(__name__)
DB = 'database.db'

with sqlite3.connect(DB) as db :
    db.execute('CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT,'' title TEXT, content TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY AUTOINCREMENT,'' q TEXT, a TEXT)')
    
    
    
@app.route('/news',methods=['GET','POST'])
def news():
    with sqlite3.connect(DB)as db:
        if request.method =='POST':
            d = request.json
            db.execute('INSERT INTO news (title, content) VALUES (?,?)',(d['title'],d['content']),)
            return '',201
        return jsonify([
            {'id':r[0], 'title':r[1],'content':r[2]} for r in db.execute('SELECT * FROM news').fetchall()
        ])




@app.route('/questions',methods=['GET','POST'])
def questions():
    with sqlite3.connect(DB) as db:
        if request.method == 'POST':
            d = request.json
            db.execute('INSERT INTO questions (q,a) VALUES(?,?)',(d['q'],d['a']))
            return '',201 
        return jsonify([
            {'id':r[0], 'q':r[1],'a':r[2]} for r in db.execute('SELECT * FROM questions').fetchall()
        ])
        
        
        
        
        

@app.route('/search')
def search():
    q = f'%{request.args.get('q','')}%'
    with sqlite3.connect(DB) as db:
        n = db.excute('SELECT * FROM news WHERE title LIKE ? OR content LIKE ?',(q,q)).fetchall()
        qs = db.execute('SELECT * FROM questions WHERE q LIKE ? OR a LIKE ?',(q,q)).fetchall()
        return jsonify({
                        'news':[{'id':r[0],'title':r[1],'content':r[2]}for r in n],
                        'questions':[{'id':r[0],'q':r[1],'a':r[2]}for r in qs],
                        })


app.run(port=5000)