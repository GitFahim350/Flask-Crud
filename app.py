from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime  import datetime

from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'fahim'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'Flaskdb'

mysql=MySQL(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute(''' SELECT * FROM USERS WHERE id= (%s);''',(id,))
        data=cursor.fetchall()
        print (data[0][0])
        print (data[0][1])
        mysql.connection.commit()
        cursor.close()
        return render_template("update.html",data=data)
    if request.method == 'POST':
        FirstName = request.form['FirstName']
        LastName = request.form['LastName']
        Email = request.form['Email']
        Password=request.form['Password']
        Confirmpassword=request.form['ConfirmPassword']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM USERS")
        data = cursor.fetchall()
        cursor.execute('''UPDATE USERS
        SET FirstName=(%s) ,LastNAME=(%s),Email=(%s),Password=(%s),confirmPassword=(%s) WHERE id = (%s)''',(FirstName,LastName,Email,Password,Confirmpassword,id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index', notice="Successfully updated"))



@app.route('/delete/<int:id>')
def delete(id):
    print(id)
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM USERS WHERE id=(%s)''',(id,))
    
    mysql.connection.commit()
    cursor.close()
    return redirect('/users')


@app.route("/users", methods = ['POST', 'GET'])
def index():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM USERS")
        data = cursor.fetchall()
        print("ssssssssss")
        notice=""
        # print(request.args['notice'])
        # if 'request.args["notice"]' in locals():
        #     if request.args['notice']:
        #         notice=request.args['notice']
            
        print(data)
        print("SSSSSSs")
        mysql.connection.commit()
        cursor.close()
        return render_template("index.html",data=data,notice=notice)
    if request.method == 'POST':
        FirstName = request.form['FirstName']
        LastName = request.form['LastName']
        Email = request.form['Email']
        Password=request.form['Password']
        Confirmpassword=request.form['ConfirmPassword']
        
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO USERS(FirstName,LastNAME,Email,Password,ConfirmPassword) VALUES(%s,%s,%s,%s,%s)''',(FirstName,LastName,Email,Password,Confirmpassword))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index', notice="Successfully Saved"))

        


if __name__ == "__main__":
    app.run(debug=True,port=8000)
   