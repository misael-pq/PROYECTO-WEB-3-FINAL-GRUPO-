from flask import Flask, jsonify, render_template, request #type:ignore
from flask_mysqldb import MySQL #type:ignore
from flask_jwt_extended import JWTManager, create_access_token, jwt_required #type:ignore

app = Flask(__name__)
mysql = MySQL(app)

app.config['JWT_SECRET_KEY'] = '7323'
jwt = JWTManager(app)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "control_db"

@app.route('/')
def inicio():
    return render_template("prestamos.html")

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username == 'admin' and password == '123':
        token = create_access_token(identity=username)
        return jsonify(access_token=token)
    return jsonify({"error": "credenciales incorrectas"}), 401

# GET (Listar todas)
@app.route('/solicitudes', methods=['GET'])
def listar_solicitudes():
    cursor = mysql.connection.cursor()
    sql = """SELECT s.id_solicitud, u.nombre AS usuario, e.nombre AS equipo, s.fecha_solicitud, s.estado 
        FROM solicitudes s
        JOIN usuarios u ON s.id_usuario = u.id_usuario
        JOIN equipos e ON s.id_equipo = e.id_equipo"""
    cursor.execute(sql)
    datos = cursor.fetchall()

    solicitudes = []
    for fila in datos:
        solicitudes.append({
            "id_solicitud": fila[0],
            "usuario": fila[1],
            "equipo": fila[2],
            "fecha_solicitud": fila[3].strftime('%Y-%m-%d'),
            "estado": fila[4]
        })
    cursor.close()
    return jsonify(solicitudes)

# Consulta Personalizada (Filtrar por Estado)
@app.route('/solicitudes/estado/<estado>', methods=['GET'])
def solicitudes_por_estado(estado):
    cursor = mysql.connection.cursor()
    sql = """SELECT s.id_solicitud, u.nombre AS usuario, e.nombre AS equipo, s.fecha_solicitud, s.estado 
        FROM solicitudes s
        JOIN usuarios u ON s.id_usuario = u.id_usuario
        JOIN equipos e ON s.id_equipo = e.id_equipo
        WHERE s.estado = %s"""
    cursor.execute(sql, (estado,))
    datos = cursor.fetchall()

    solicitudes = []
    for fila in datos:
        solicitudes.append({
            "id_solicitud": fila[0],
            "usuario": fila[1],
            "equipo": fila[2],
            "fecha_solicitud": fila[3].strftime('%Y-%m-%d'),
            "estado": fila[4]
        })
    cursor.close()
    return jsonify(solicitudes)

# POST
@app.route('/solicitudes', methods=['POST'])
@jwt_required()
def insertar_solicitud():
    data = request.get_json()
    id_usuario = data['id_usuario']
    id_equipo = data['id_equipo']
    fecha_solicitud = data['fecha_solicitud']
    estado = 'Pendiente'

    cursor = mysql.connection.cursor()
    sql = """INSERT INTO solicitudes(id_usuario, id_equipo, fecha_solicitud, estado)
             VALUES(%s, %s, %s, %s)"""
    cursor.execute(sql, (id_usuario, id_equipo, fecha_solicitud, estado))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje": "Solicitud registrada con exito"}), 201

# PUT
@app.route('/solicitudes/<int:id>', methods=['PUT'])
@jwt_required()
def modificar_estado_solicitud(id):
    data = request.get_json()
    estado = data['estado']

    cursor = mysql.connection.cursor()
    sql = """UPDATE solicitudes
             SET estado = %s
             WHERE id_solicitud = %s """

    cursor.execute(sql, (estado, id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Estado de la solicitud modificado"}), 200

# DELETE
@app.route('/solicitudes/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_solicitud(id):
    cursor = mysql.connection.cursor()
    sql = """DELETE FROM solicitudes
          WHERE id_solicitud = %s"""
    cursor.execute(sql, (id,))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({"mensaje": "Solicitud eliminada correctamente"}), 200

if __name__ == '__main__':
    app.run(debug=True)