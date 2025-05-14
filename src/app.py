from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
from config import config
import re  # Importa el módulo de expresiones regulares para validar el email
from crud import contar_clientes, clientes,  contar_reparaciones_pendientes,pendientes, diccionario_nombres,finalizadas,canceladas,contar_usuarios,contar_rep_por_estado

app = Flask(__name__)
mysql = MySQL(app)

# Rutas
@app.route('/')
def index():
    return render_template('indice.html')

@app.route('/auth')   #AGREGUÉ 25-2
def auth():
    return render_template('auth/login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = request.args.get('message')  # Obtener el mensaje de la URL
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombre=%s AND contrasena=%s AND existe = 1", (username, password))  # Ajustado a 'nombre' y 'contrasena'
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]  # Guarda el ID del usuario en la sesión
            session['username'] = user[1]  # Guarda el nombre del usuario en la sesión
            session['rol'] = user[3]      # Guarda el rol del usuario en la sesión
            return redirect(url_for('dashboard'))  # Usa url_for para mayor claridad
        else:
            return render_template('auth/login.html', message='Credenciales incorrectas, inténtalo de nuevo.')
    return render_template('auth/login.html')#, message=message)# Para manejar el GET

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    message = request.args.get('message')
    if request.method == 'POST':
        username = request.form['firstName']  # Cambia esto si el nombre del campo es diferente
        email = request.form['email']
        password = request.form['password']
        
        # Validar que el email no esté vacío y tenga un formato válido
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render_template('register.html', message='Por favor, ingresa un correo electrónico válido.')

        # Aquí puedes agregar validaciones adicionales si es necesario
        cursor = mysql.connection.cursor()
        
        # Verificar si el nombre de usuario ya existe
        cursor.execute("SELECT * FROM usuarios WHERE nombre=%s", (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            # Si el usuario ya existe, muestra un mensaje de error
            return render_template('register.html', message='El nombre de usuario ya está en uso.')
        
        # Aquí puedes agregar validaciones adicionales si es necesario
        cursor.execute("INSERT INTO usuarios (nombre, email, contrasena) VALUES (%s, %s, %s)", (username, email, password))
        mysql.connection.commit()
        cursor.close()
        
        # Redirigir al login con un mensaje de éxito
        return redirect(url_for('login', message='Registro exitoso. Puedes iniciar sesión ahora.'))  # Redirige al login después de registrarse

    return render_template('register.html')  # Muestra el formulario de registro

@app.route('/indice')
def indice():
    return render_template('/indice.html')
@app.route('/register')
def register():
    return render_template('/register.html')
@app.route('/contact')
def contact():
    return render_template('/contact.html')


@app.route('/panel')
def dashboard():
    total_reps_pendientes = contar_reparaciones_pendientes(mysql)
    total_clientes = contar_clientes(mysql)
    total_usuarios=contar_usuarios(mysql)
    total_reps_finalizadas=contar_rep_por_estado(mysql,'finalizado')
    total_reps_canceladas=contar_rep_por_estado(mysql,'cancelado')
    
    if 'username' in session:
        return render_template('panel.html',total_reps_canceladas=total_reps_canceladas,total_reps_finalizadas=total_reps_finalizadas,total_usuarios=total_usuarios,total_clientes=total_clientes, total_reps_pendientes=total_reps_pendientes)
    else:
        return redirect(url_for('login'))

@app.route('/clientes', endpoint='clientes')
def rclientes():
    usuarios_dict, clientes_dict = diccionario_nombres(mysql)
    fclientes = clientes(mysql)  
    return render_template('clientes.html', clientes=fclientes,usuarios_dict=usuarios_dict,clientes_dict=clientes_dict)

@app.route('/pendientes')
def rpendientes():  
    usuarios_dict, clientes_dict = diccionario_nombres(mysql)
    reparaciones_pendientes = pendientes(mysql)  
    return render_template ('pendientes.html', reparaciones_pendientes=reparaciones_pendientes,usuarios_dict=usuarios_dict,clientes_dict=clientes_dict)


@app.route('/finalizadas')
def rfinalizadas():  
    usuarios_dict, clientes_dict = diccionario_nombres(mysql)
    reparaciones_finalizadas = finalizadas(mysql)  
    return render_template ('finalizadas.html', reparaciones_finalizadas=reparaciones_finalizadas,usuarios_dict=usuarios_dict,clientes_dict=clientes_dict)


@app.route('/canceladas')
def rcanceladas():  
    usuarios_dict, clientes_dict = diccionario_nombres(mysql)
    reparaciones_canceladas = canceladas(mysql)  
    return render_template ('canceladas.html', reparaciones_canceladas=reparaciones_canceladas,usuarios_dict=usuarios_dict,clientes_dict=clientes_dict)

@app.route('/usuarios')  # Lista de usuarios (solo admin)
def usuarios():
    if 'username' not in session or session['rol'] != 1:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE existe = 1")
    usuarios = cursor.fetchall()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/edit_usuario/<int:id>', methods=['GET', 'POST'])
def edit_usuario(id):
    conn = mysql.connection
    cursor = conn.cursor()

    if request.method == 'POST':
        id_user = request.form['txtUser']
        nombre = request.form['txtNombre']
        email = request.form['txtEmail']

        sql = "UPDATE usuarios SET nombre=%s, email=%s WHERE id_usuarios=%s"
        datos = (nombre, email, id_user)

        cursor.execute(sql, datos)
        conn.commit()
        cursor.close()
        return redirect(url_for('usuarios'))

    else:  # Caso GET: mostrar el formulario de edición
        cursor.execute("SELECT * FROM usuarios WHERE id_usuarios=%s AND existe=1", (id,))
        usuario = cursor.fetchone()  # Obtiene el usuario específico por ID

        if usuario: # Verifica si el usuario existe.
            cursor.execute("SELECT * FROM usuarios WHERE existe=1")
            usuarios = cursor.fetchall()
            cursor.close()
            return render_template('edit_usuario.html', usuario=usuario, usuarios=usuarios)
        else:
            cursor.close()
            return "Usuario no encontrado", 404 # Mejor manejo de error.

@app.route('/edit_cliente/<int:id>', methods=['GET', 'POST'])
def edit_cliente(id):
    conn = mysql.connection
    cursor = conn.cursor()

    if request.method == 'POST':
        id_user = request.form['txtID']
        nombre = request.form['txtNombre']
        email = request.form['txtEmail']
        telefono = request.form['txtTelefono']

        sql = "UPDATE clientes SET nombre=%s, email=%s, telefono=%s WHERE id_clientes=%s"
        datos = (nombre, email,telefono, id_user)

        cursor.execute(sql, datos)
        conn.commit()
        cursor.close()
        return redirect(url_for('clientes'))

    else:  # Caso GET: mostrar el formulario de edición
        cursor.execute("SELECT * FROM clientes WHERE id_clientes=%s AND existe=1", (id,))
        cliente = cursor.fetchone()  # Obtiene el usuario específico por ID

        if cliente: # Verifica si el usuario existe.
            cursor.execute("SELECT * FROM clientes WHERE existe=1")
            clientes = cursor.fetchall()
            cursor.close()
            return render_template('edit_cliente.html', cliente=cliente, clientes=clientes)
        else:
            cursor.close()
            return "Cliente no encontrado", 404 




@app.route('/actualizar/<int:id>', methods=['GET', 'POST'])  # Acepta GET y POST
def actualizar(id):
    conn = mysql.connection
    cursor = conn.cursor()

    if request.method == 'POST':  # Lógica de actualización si es POST
        fecha_reparacion = request.form['txtFecha']
        descripcion = request.form['txtDescripcion']
        costo = request.form['txtCosto']  # No es request.files, es request.form para campos de texto
        existe = request.form['txtExiste']
        estado = request.form['txtEstado']
        id_clientes = request.form['txtCliente']
        id_rep = request.form['txtIDrep']

        sql = "UPDATE reparaciones SET fecha_reparacion=%s, descripcion=%s, costo=%s, existe=%s, estado=%s, id_clientes=%s WHERE id_reparaciones=%s"
        datos = (fecha_reparacion, descripcion, costo, existe, estado, id_clientes, id_rep)

        cursor.execute(sql, datos)
        conn.commit()
        cursor.close()
        return redirect(url_for('reparaciones'))  # Redirige a la lista de reparaciones

    else:  # Lógica para mostrar el formulario si es GET
        cursor.execute("SELECT * FROM reparaciones WHERE id_reparaciones=%s AND existe=1", (id,))
        reparaciones = cursor.fetchall()

        cursor.execute("SELECT * FROM usuarios WHERE existe=1")
        usuarios = cursor.fetchall()
        usuarios_dict = {usuario[0]: usuario[1] for usuario in usuarios}# Creamos diccionarios para mapear IDs a nombres. Sólo acá no me sirven, necesito ponerlos en /reparaciones también, sino la variable no existe en la tabla principal.
        cursor.execute("SELECT * FROM clientes WHERE existe=1")
        clientes = cursor.fetchall()
        clientes_dict = {cliente[0]: cliente[1] for cliente in clientes}
        cursor.close()
        
        
        return render_template('reparaciones.html', reparaciones=reparaciones, usuarios=usuarios, clientes=clientes,usuarios_dict=usuarios_dict,clientes_dict=clientes_dict,  modo_editar=True)#

@app.route('/borrar/<int:id>', methods=['GET'])  # Ahora acepta solicitudes GET
def borrar(id):
    conn = mysql.connection
    cursor = conn.cursor()

    try:
        # Ejecuta la consulta UPDATE para cambiar el estado de "existe" a 0
        sql = "UPDATE reparaciones SET existe = 0 WHERE id_reparaciones = %s"
        cursor.execute(sql, (id,))
        conn.commit()  # Guarda los cambios en la base de datos
    except Exception as e:
        print(f"Error al cambiar estado de reparación: {e}")
        conn.rollback()  # Revierte los cambios en caso de error
    finally:
        cursor.close()

    return redirect(url_for('reparaciones')) 


@app.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']  # Contraseña en texto plano
        email = request.form['email']
        admin = request.form['admin']
        existe = request.form['existe']

        cursor = mysql.connection.cursor()
        sql = "INSERT INTO usuarios (nombre, contrasena, email, admin, existe) VALUES (%s, %s, %s, %s, %s)"
        datos = (nombre, password, email, admin, existe) 
        cursor.execute(sql, datos)
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('usuarios'))

    return render_template('crear_usuario.html')


@app.route('/crear_cliente', methods=['GET', 'POST'])
def crear_cliente():
    conn = mysql.connection
    cursor = conn.cursor()
    usuarios_dict, clientes_dict = diccionario_nombres(mysql)

    
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        existe = request.form['existe']
        id_usuario = session['user_id']
        
        

        # cursor = mysql.connection.cursor()
        sql = "INSERT INTO clientes (nombre, email, telefono, existe, id_usuario) VALUES (%s, %s, %s, %s, %s)"
        datos = (nombre, email, telefono, existe, id_usuario)
        cursor.execute(sql, datos)
        conn.commit()
        cursor.close()

        return redirect(url_for('clientes'))  # Redirige a la lista de clientes

    return render_template('crear_cliente.html',usuarios_dict=usuarios_dict,clientes_dict=clientes_dict)

@app.route('/crear_reparacion', methods=['GET', 'POST'])
def crear_reparacion():
    conn = mysql.connection
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE existe=1")
    usuarios = cursor.fetchall()
    usuarios_dict = {usuario[0]: usuario[1] for usuario in usuarios}# Creamos diccionarios para mapear IDs a nombres. Sólo acá no me sirven, necesito ponerlos en /reparaciones también, sino la variable no existe en la tabla principal.
    cursor.execute("SELECT * FROM clientes WHERE existe=1")
    clientes = cursor.fetchall()
    clientes_dict = {cliente[0]: cliente[1] for cliente in clientes}

    usuarios_dict, clientes_dict = diccionario_nombres(mysql)
    
    
    # ... (código para obtener usuarios y clientes) ...
    if request.method == 'POST':  # Lógica de actualización si es POST
        fecha_reparacion = request.form['txtFecha']
        descripcion = request.form['txtDescripcion']
        costo = request.form['txtCosto']  # No es request.files, es request.form para campos de texto
        existe = request.form['txtExiste']
        estado = request.form['txtEstado']
        id_clientes = request.form['txtCliente']
        id_user = request.form['txtUser']

        sql = "INSERT INTO reparaciones (fecha_reparacion, descripcion, costo, existe, estado, id_clientes, id_usuarios) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        datos = (fecha_reparacion, descripcion, costo, existe, estado, id_clientes, id_user)

        cursor.execute(sql, datos)
        conn.commit()
        cursor.close()
        return redirect(url_for('reparaciones'))  # Redirige a la lista de reparaciones
    return render_template('crear_reparacion.html', reparaciones=reparaciones, usuarios=usuarios, clientes=clientes, usuarios_dict=usuarios_dict, clientes_dict=clientes_dict)

@app.route('/reparaciones')
def reparaciones():
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    usuarios_dict, clientes_dict = diccionario_nombres(mysql) #Lo agrego en cada route que necesite el reemplazo de usuarios. Si lo uso arriba no tiene contexto.

    if session['rol'] == 1:
        # Admin ve todas las reparaciones con "existe" = 1
        cursor.execute("SELECT * FROM reparaciones WHERE existe = 1")
    else:
        # Usuario normal ve sus reparaciones con "existe" = 1
        cursor.execute("SELECT * FROM reparaciones WHERE id_usuarios = %s AND existe = 1", (session['user_id'],))

    reparaciones = cursor.fetchall()
    return render_template('reparaciones.html', reparaciones=reparaciones,usuarios_dict=usuarios_dict, clientes_dict=clientes_dict)
# AGREGAR!!! IMPRTANTEE !!! agregar usuarios_dict acá


@app.route('/logout')
def logout():
    session.clear()  # Limpia toda la sesión
    return redirect(url_for('indice'))

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('indice'))

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True, port=5000)