from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from datetime import timedelta

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'control_db'

mysql = MySQL(app)
app.config['JWT_SECRET_KEY'] = '7323'
# ⏱️ tiempo de expiración del token
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
jwt = JWTManager(app)

@app.route('/')
def inicio():
    return render_template("index.html")

@app.route('/login')
def formulario_login():
    return render_template('login.html')

@app.route('/devoluciones_html')
def devoluciones_html():
    return render_template('devoluciones.html')

@app.route('/equipos_html')
def equipos_html():
        return render_template('equipos.html')

@app.route('/prestamos_html')
def prestamos_html():
        return render_template('prestamos.html')

@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if username == 'admin' and password == '123':
        token = create_access_token(identity=username)

        return jsonify({
            'access_token': token
        })

    return jsonify({
        'error': 'credenciales incorrectas'
    }), 401

@app.route('/registrar_equipo')
def formulario_registrar_equipo():
    return render_template('registrar_equipo.html')

@app.route('/equipos', methods=['GET'])
def listar_equipos():
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM equipos")
    datos = cur.fetchall()

    equipos = []

    for fila in datos:
        equipos.append({
            "id_equipo": fila[0],
            "nombre": fila[1],
            "marca": fila[2],
            "modelo": fila[3],
            "descripcion": fila[4],
            "estado": fila[5],
            "id_categoria": fila[6]
        })
    cur.close()
    return jsonify(equipos)

@app.route('/equipos', methods=['POST'])
@jwt_required()
def registrar_equipo():

    data = request.get_json()

    nombre = data['nombre']
    marca = data['marca']
    modelo = data['modelo']
    descripcion = data['descripcion']
    id_categoria = data['id_categoria']

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO equipos
        (nombre,marca,modelo,descripcion,id_categoria)
        VALUES(%s,%s,%s,%s,%s)
    """,
    (nombre,marca,modelo,descripcion,id_categoria))

    mysql.connection.commit()

    return jsonify({
        "mensaje":"Equipo registrado"
    }),201

@app.route('/equipos/<int:id>/devolver', methods=['PATCH'])
def devolver_equipo(id):

    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE equipos
        SET estado='Disponible'
        WHERE id_equipo=%s
    """, (id,))

    mysql.connection.commit()

    cur.close()
    return jsonify({
        "mensaje": "Equipo devuelto correctamente"
    })

@app.route('/equipos/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_equipo(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM equipos WHERE id_equipo=%s",
        (id,)
    )
    mysql.connection.commit()

    cur.close()

    return jsonify({
        "mensaje":"Equipo eliminado"
    })

@app.route('/equipos/<int:id_equipo>/prestar', methods=['PUT'])
def prestar(id_equipo):
    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE equipos
        SET estado='Prestado'
        WHERE id_equipo=%s
    """, (id_equipo,))

    mysql.connection.commit()
    cur.close()

    return jsonify({
        "mensaje":"Equipo prestado"
    })

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

@app.route('/devoluciones/<int:id_prestamo>', methods=['PUT'])
def devolver_prestamo(id_prestamo):
    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT id_equipo, estado
        FROM prestamos
        WHERE id_prestamo=%s
    """, (id_prestamo,))

    prestamo = cursor.fetchone()

    if prestamo is None:
        cursor.close()
        return jsonify({"mensaje":"Prestamo no encontrado"}),404

    if prestamo[1] != "Activo":
        cursor.close()
        return jsonify({
            "mensaje":"El prestamo no esta activo"
        }),400

    id_equipo = prestamo[0]

    cursor.execute("""
        UPDATE prestamos
        SET estado='Devuelto',
            fecha_devolucion_real=CURDATE()
        WHERE id_prestamo=%s
    """, (id_prestamo,))

    cursor.execute("""
        UPDATE equipos
        SET estado='Disponible'
        WHERE id_equipo=%s
    """, (id_equipo,))

    mysql.connection.commit()
    cursor.close()

    return jsonify({
        "mensaje":"Devolucion registrada correctamente"
    })

@app.route('/prestamos_activos')
def prestamos_activos():
    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT p.id_prestamo,
               u.nombre,
               e.nombre,
               p.fecha_prestamo,
               p.fecha_devolucion_prevista
        FROM prestamos p
        INNER JOIN usuarios u
            ON p.id_usuario=u.id_usuario
        INNER JOIN equipos e
            ON p.id_equipo=e.id_equipo
        WHERE p.estado='Activo'
    """)

    datos = cursor.fetchall()

    prestamos = []

    for fila in datos:
        prestamos.append({
            "id_prestamo": fila[0],
            "usuario": fila[1],
            "equipo": fila[2],
            "fecha_prestamo": str(fila[3]),
            "fecha_devolucion_prevista": str(fila[4])
        })

    cursor.close()

    return jsonify(prestamos)

@app.route('/reportes_html')
def reportes():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            p.id_prestamo,
            u.nombre,
            u.tipo,
            e.nombre,
            e.marca,
            e.modelo,
            p.fecha_prestamo,
            p.fecha_devolucion_prevista,
            p.fecha_devolucion_real,
            p.estado
        FROM prestamos p
        INNER JOIN usuarios u
            ON p.id_usuario = u.id_usuario
        INNER JOIN equipos e
            ON p.id_equipo = e.id_equipo
        ORDER BY p.id_prestamo DESC
    """)

    historial_bd = cursor.fetchall()

    historial = []

    for fila in historial_bd:
        historial.append({
            "id": fila[0],
            "usuario": fila[1],
            "tipo": fila[2],
            "equipo": fila[3],
            "marca": fila[4],
            "modelo": fila[5],
            "fecha_prestamo": str(fila[6]),
            "fecha_prevista": str(fila[7]),
            "fecha_real": str(fila[8]) if fila[8] else "No devuelto",
            "estado": fila[9]
        })

    cursor.execute("""
        SELECT
            e.id_equipo,
            e.nombre,
            e.marca,
            e.modelo,
            c.nombre
        FROM equipos e
        INNER JOIN categorias c
            ON e.id_categoria = c.id_categoria
        WHERE e.estado='Disponible'
    """)

    disponibles_bd = cursor.fetchall()

    disponibles = []

    for fila in disponibles_bd:
        disponibles.append({
            "id": fila[0],
            "nombre": fila[1],
            "marca": fila[2],
            "modelo": fila[3],
            "categoria": fila[4]
        })

    cursor.execute("""
        SELECT
            u.nombre,
            u.tipo,
            COUNT(*) AS total
        FROM prestamos p
        INNER JOIN usuarios u
            ON p.id_usuario=u.id_usuario
        GROUP BY u.id_usuario
        ORDER BY total DESC
    """)

    frecuentes_bd = cursor.fetchall()

    frecuentes = []

    for fila in frecuentes_bd:
        frecuentes.append({
            "usuario": fila[0],
            "tipo": fila[1],
            "total": fila[2]
        })

    cursor.execute("""
        SELECT
            c.nombre,
            COUNT(*) AS total
        FROM prestamos p
        INNER JOIN equipos e
            ON p.id_equipo=e.id_equipo
        INNER JOIN categorias c
            ON e.id_categoria=c.id_categoria
        GROUP BY c.id_categoria
        ORDER BY total DESC
    """)

    categorias_bd = cursor.fetchall()

    categorias = []

    for fila in categorias_bd:
        categorias.append({
            "categoria": fila[0],
            "total": fila[1]
        })

    cursor.execute("SELECT COUNT(*) FROM prestamos")
    total_prestamos = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM prestamos
        WHERE estado='Activo'
    """)
    prestamos_activos = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM equipos
        WHERE estado='Disponible'
    """)
    equipos_disponibles = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM usuarios
    """)
    total_usuarios = cursor.fetchone()[0]


    cursor.close()

    return render_template(
        "reportes.html",

        historial=historial,
        disponibles=disponibles,
        frecuentes=frecuentes,
        categorias=categorias,
        total_prestamos=total_prestamos,
        prestamos_activos=prestamos_activos,
        equipos_disponibles=equipos_disponibles,
        total_usuarios=total_usuarios
    )

@app.route('/verificar_token')
@jwt_required()
def verificar_token():
    return {"mensaje": "Token válido"}, 200
if __name__ == '__main__':
    app.run(debug=True)