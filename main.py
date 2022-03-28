from flask import Flask, request, url_for, redirect, abort, render_template

import mysql.connector

#formas de envios desde flask sin necesidad de un formulario
#CURL -X POST http://localhost:5000/post/1
#CURL -d "llave1=dato1&llave2=dato2" -X POST http://localhost:5000/lele
#abort se usa para poder detener la ejecucion de nuestra funcion y devolver un status code

#Get -> cuando quieres el listar o quieres mostrar algo
#Post -> cuando quieres crear
#Put -> cuando quieres actualizar
#Delete -> cuando quieres eliminar algo

app = Flask(__name__)

db = mysql.connector.connect(
    host= 'localhost',
    user= 'root',
    password= '',
    database = 'flask'
)

#este atributo se lo ponemos para que nos devuelva en diccionario dictionary= True
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    return 'hola'

@app.route('/post/<post_id>', methods = ['GET', 'POST'])
def lala(post_id):
    if request.method == 'GET':
        return 'Get post' + post_id
    return 'Post post' + post_id

@app.route('/lele', methods = ['GET', 'POST'])
def lele():
    #redirect(url_for('lala', post_id=1))
    #print(request.form['llave1'])
    #print(request.form['llave2'])
    #abort(504)
    return {
        'username ' : 'Miguel',
        'email': 'miguel.ramirez@utp.edu.co'
    }

@app.route('/usuarios')
def usuarios():
    cursor.execute("SELECT * FROM Usuario")
    usuarios = cursor.fetchall()

    return render_template('usuarios.html', usuarios = usuarios)

#Get -> para nosotros poder obtener el formulario
#Post -> el de post para poder manejar lo que haremos cuando queramos crear un registro
@app.route('/crear', methods = ['GET', 'POST'])
def crear():
    if request.method == 'POST':
        username = request.form['name']
        edad = request.form['edad']
        email = request.form['email']
        #no pasamos la sentencia directamente porque desde el formulario me pueden inyectar sql
        #por lo tanto si lo hago como cursor.execute(sql, values), se va a encargar de algun manera verificar
        sql = 'insert into Usuario (username, edad, email) values (%s, %s, %s)'
        values = (username, edad, email )
        cursor.execute(sql, values)
        #comprometemos para que se vea el cambio
        db.commit()
        return redirect(url_for('usuarios'))

    return render_template('crear.html')

@app.route('/home')
def home():
    cursor.execute()
    return render_template('home.html', mensaje = 'Miguel')
