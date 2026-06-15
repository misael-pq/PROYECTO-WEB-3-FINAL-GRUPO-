from flask import render_template

@app.route('/reportes')
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