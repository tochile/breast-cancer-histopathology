import os

from flask import Flask, render_template, request, redirect

from inference import get_prediction
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

app = Flask(__name__) 
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/login',methods=['POST'])
def login():
    
    username = request.form['username']
    password = request.form['password']
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * from user where binary username=%s and binary password=%s",[username,password])
    if(result>0):
        return render_template("index.html", username=username)
    else:
        error = 'failed'
        return render_template("login.html", error=error)


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files.get('file')
        if not file:
            return
        img_bytes = file.read()
        prediction = get_prediction(image_bytes=img_bytes)
        name = 'prissy'
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO result(username,result) VALUES(%s, %s)", (name,prediction))
        mysql.connection.commit()
        cur.close()
        return render_template('result.html',
                               class_name=prediction)
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template("admin.html")


      
@app.route('/admin_login',methods=['POST'])
def admin_login():
    
    
        
    user = request.form['username']
    pass1 = request.form['password']
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * from doctor where binary username=%s and binary password=%s",[user,pass1])
    if(result>0):
         cur = mysql.connection.cursor()
         result1 = cur.execute("SELECT * from result")
         if(result1>0):
        
             result3 = cur.fetchall()
        
         return render_template("admin_login.html", result2=result3)
    
    else:
    
        error = 'failed'
        return render_template("admin.html", error=error)
   
        
    

if __name__ == '__main__':
    app.run(debug=True)
