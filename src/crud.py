
from flask import session, redirect, url_for, render_template
from flask_mysqldb import MySQL


def contar_clientes(mysql):   #Funciona! Pasando mysql acá y en app.py anda.
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    if session['rol'] == 1:
        cursor.execute("SELECT COUNT(*) FROM clientes WHERE existe=1")  # Admin ve todos los clientes
    else:  # Técnico solo ve sus clientes
        cursor.execute("SELECT COUNT(*) FROM clientes WHERE id_usuario = %s AND existe=1", (session['user_id'],))
    total_clientes = cursor.fetchone()[0]
    cursor.close()
    return total_clientes
    
def clientes(mysql):
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    try:
        if session['rol'] == 1:
            cursor.execute("SELECT * FROM clientes WHERE existe = 1")
        else:
            cursor.execute("SELECT * FROM clientes WHERE id_usuario = %s AND existe = 1", (session['user_id'],))
        clientes = cursor.fetchall()
    finally:
        cursor.close()
    return clientes
    
def contar_reparaciones_pendientes(mysql):
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    try:
        if session['rol'] == 1:
            # Admin ve todas las reparaciones pendientes
            cursor.execute("SELECT COUNT(*) FROM reparaciones WHERE estado = 'pendiente' AND existe=1 ")
        else:
            # Técnico solo ve sus reparaciones pendientes
            cursor.execute("SELECT COUNT(*) FROM reparaciones WHERE id_usuarios = %s AND estado = 'pendiente' AND existe=1", (session['user_id'],))
        total_reparaciones = cursor.fetchone()[0]
    except Exception as e:
        print(f"Error al contar reparaciones: {e}")
        total_reparaciones = 0  # O un valor por defecto
    finally:
        cursor.close()
    return total_reparaciones


def contar_rep_por_estado(mysql, estado):
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    try:
        if session['rol'] == 1:
            # Admin ve todas las reparaciones según el estado
            cursor.execute("SELECT COUNT(*) FROM reparaciones WHERE LOWER(estado) = %s AND existe=1", (estado.lower(),)) #estado.lower convierte el string a minuscula
        else:
            # Técnico solo ve sus reparaciones según el estado
            cursor.execute("SELECT COUNT(*) FROM reparaciones WHERE id_usuarios = %s AND LOWER(estado) = %s AND existe=1", (session['user_id'], estado.lower()))
        total_reparaciones = cursor.fetchone()[0]
    except Exception as e:
        print(f"Error al contar reparaciones: {e}")
        total_reparaciones = 0  # O un valor por defecto
    finally:
        cursor.close()
    return total_reparaciones


def pendientes(mysql):
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    try:
        if session['rol'] == 1:
            # Admin ve todas las reparaciones con estado "pendiente"
            cursor.execute("SELECT * FROM reparaciones WHERE LOWER(estado) = 'pendiente' AND existe = 1")
        else:
            # Usuario normal ve sus reparaciones con estado "pendiente"
            cursor.execute("SELECT * FROM reparaciones WHERE id_usuarios = %s AND LOWER(estado) = 'pendiente' AND existe = 1", (session['user_id'],))

        reparaciones_pen = cursor.fetchall()
    finally:
        cursor.close()
    return reparaciones_pen

# Obtener nombres con los id de clientes y usuarios:
def diccionario_nombres(mysql):
    usuarios_dict = {}
    clientes_dict = {}
    # cursor=None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id_usuarios, nombre FROM usuarios")
        usuarios = cursor.fetchall()
        usuarios_dict = {usuario[0]: usuario[1] for usuario in usuarios}
        cursor.execute("SELECT id_clientes, nombre FROM clientes")
        clientes = cursor.fetchall()
        clientes_dict = {cliente[0]: cliente[1] for cliente in clientes}
    finally:
        cursor.close()
    return usuarios_dict, clientes_dict


def finalizadas(mysql):
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    try:
        if session['rol'] == 1:
            # Admin ve todas las reparaciones con estado "pendiente"
            cursor.execute("SELECT * FROM reparaciones WHERE LOWER(estado) = 'finalizado' AND existe = 1")
        else:
            # Usuario normal ve sus reparaciones con estado "pendiente"
            cursor.execute("SELECT * FROM reparaciones WHERE id_usuarios = %s AND LOWER(estado) = 'finalizado' AND existe = 1", (session['user_id'],))
        reparaciones_fin = cursor.fetchall()
    finally:
        cursor.close()
    return reparaciones_fin

def canceladas(mysql):
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    try:
        if session['rol'] == 1:
            #Admin ve todas las reparaciones con estado "cancelado"
            cursor.execute("SELECT * FROM reparaciones WHERE LOWER(estado) = 'cancelado' AND existe = 1")
        else:
            #Usuario normal ve sus reparaciones con estado " cancelado"
            cursor.execute("SELECT * FROM reparaciones WHERE id_usuarios = %s AND LOWER(estado) = 'cancelado' AND existe = 1", (session['user_id'],))
        reparaciones_canc = cursor.fetchall()  # Cambiado el nombre de la variable
    finally:
        cursor.close()
    return reparaciones_canc  # Devuelve la lista de reparaciones canceladas

def contar_usuarios(mysql):
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    try:
        if session['rol'] == 1:
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE existe=1")  # Admin ve todos los usuarios
        else:
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE id_usuarios = %s AND existe=1", (session['user_id'],))  # Usuario normal ve sus usuarios
        total_usuarios = cursor.fetchone()[0]
    except Exception as e:
        print(f"Error al contar usuarios: {e}")
        total_usuarios = 0  # O un valor por defecto
    finally:
        cursor.close()
    return total_usuarios