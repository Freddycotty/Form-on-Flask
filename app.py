from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)

#Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

#settings

app.secret_key = 'mysecretkey'

@app.route('/')
def index():
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM contacts')
  data = cur.fetchall()
  return render_template('index.html', contacts = data)
  
#AGREGAR CONTACTO
@app.route('/add_contact', methods=['POST'])
def add_contact():
  if request.method == 'POST':
    fullname = request.form['fullname']
    phone = request.form['phone']
    email = request.form['email']
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)',(fullname,phone, email))
    mysql.connection.commit()
    flash('Contact added successfully')
    return redirect(url_for('index'))

#EDITAR CONTACTO
@app.route('/edit/<string:id>')
def get_contact(id):
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM contacts WHERE id = {0}".format(id))
  data = cur.fetchall()
  return render_template('edit.html', contact = data[0])

#UPDATE AL CONTACTO
@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
  if request.method == 'POST':
    fullname = request.form['fullname']
    phone = request.form['phone']
    email = request.form['email']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE contacts SET fullname = '{0}', email = '{1}', phone = '{2}' WHERE id = '{3}'".format(fullname, email, phone, id))
    mysql.connection.commit()
    flash('Contact Update Successfully')
    return redirect(url_for('index'))

#ELIMINAR CONTACTO
@app.route('/delete/<string:id>')
def delet_contact(id):
  cur = mysql.connection.cursor()
  cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
  mysql.connection.commit()
  flash('Contact removed successfully')
  return redirect(url_for('index'))

if __name__ == '__main__':
  app.run(port = 3000, debug = True)