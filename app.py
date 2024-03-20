from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'senabd'

app.secret_key = 'mysecretkey'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuario WHERE nombre_usuario = %s AND password = %s', (nombre_usuario, password))
        usuario = cur.fetchone()
        cur.close()
        if usuario:
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('task'))
        else:
            flash('Credenciales inválidas. Por favor, inténtalo de nuevo.', 'danger')
            return redirect(url_for('index'))

@app.route('/task')
def task():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM curso')
    data = cur.fetchall()
    return render_template('index.html', cursos=data)

@app.route('/add_cursos', methods=['GET', 'POST'])
def add_cursos():
    if request.method == "POST":
        try:
            codigo = request.form['codigo']
            nombre = request.form['nombre']
            horas = request.form['horas']
            area = request.form['area']

            if not codigo or not nombre or not horas or not area:
                raise ValueError("Todos los campos son obligatorios. Por favor, rellene todos los campos.")

            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO curso (codigo, nombre, horas, area) VALUES (%s, %s, %s, %s)', (codigo, nombre, horas, area))
            mysql.connection.commit()
            flash('Curso agregado exitosamente', 'success')
        except Exception as e:
            flash(str(e), 'error')

        return redirect(url_for('index'))
    else:
        return render_template('index.html')

@app.route('/edit/<id>')
def get_curso(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM curso WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_curso.html', c=data[0])

@app.route('/update/<id>', methods=['POST'])
def update_curso(id):
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        horas = request.form['horas']
        area = request.form['area']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE curso SET codigo = %s, nombre = %s, horas = %s, area = %s WHERE id = %s', (codigo, nombre, horas, area, id))
        mysql.connection.commit()
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM curso WHERE ID = %s', (id,))
    mysql.connection.commit()
    return redirect(url_for('index'))

def pagina_no_encontrada(error):
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)