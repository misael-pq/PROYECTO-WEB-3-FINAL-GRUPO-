from flask import Flask
from flask_mysqldb import MySQL
from devoluciones import registrar_devoluciones

app = Flask(__name__)

app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "control_db"

mysql = MySQL(app)

registrar_devoluciones(app, mysql)

@app.route('/')
def inicio():
    return "API Control de Equipos"

if __name__ == '__main__':
    app.run(debug=True)