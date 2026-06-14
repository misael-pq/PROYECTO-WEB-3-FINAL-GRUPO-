from flask import jsonify, render_template

def registrar_devoluciones(app, mysql):

    @app.route('/devoluciones_html')
    def devoluciones_html():
        return render_template('devoluciones.html')

    @app.route('/devoluciones/<int:id_prestamo>', methods=['PUT'])
    def devolver_equipo(id_prestamo):
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