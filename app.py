from flask import Flask, render_template, redirect, url_for, flash
import sqlite3
import os

# Importar formularios
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.factura_form import FacturaForm

app = Flask(__name__)

# ============================================================
# CONFIGURACIÓN
# ============================================================

app.config['SECRET_KEY'] = 'maquirenthal-secret-key-2026'

# ============================================================
# FUNCIONES DE BASE DE DATOS
# ============================================================

def get_db():
    """Establece conexión con la base de datos SQLite"""
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect('data/maquirenthal.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Crea las 4 tablas si no existen"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Tabla productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            capacidad TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            categoria TEXT NOT NULL
        )
    ''')
    
    # Tabla clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            empresa TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT NOT NULL,
            ciudad TEXT NOT NULL
        )
    ''')
    
    # Tabla proveedores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            especialidad TEXT NOT NULL,
            contacto TEXT NOT NULL,
            telefono TEXT NOT NULL,
            pais TEXT NOT NULL
        )
    ''')
    
    # Tabla facturas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL,
            cliente TEXT NOT NULL,
            equipo TEXT NOT NULL,
            inicio TEXT NOT NULL,
            fin TEXT NOT NULL,
            total REAL NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Base de datos 'maquirenthal.db' creada correctamente")
    print("✅ Tablas: productos, clientes, proveedores, facturas")

# Inicializar la base de datos al iniciar la aplicación
init_db()

# ============================================================
# VARIABLES SIMPLES
# ============================================================

NOMBRE_EMPRESA = "maquirenthal"
ANIO_FUNDACION = 2023

# ============================================================
# RUTAS PRINCIPALES
# ============================================================

@app.route('/')
def index():
    return render_template('index.html', 
                          empresa=NOMBRE_EMPRESA.upper(),
                          anio=ANIO_FUNDACION)

# ============================================================
# CRUD - PRODUCTOS (SQLite)
# ============================================================

@app.route('/productos')
def productos():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos ORDER BY id DESC')
    equipos = cursor.fetchall()
    conn.close()
    return render_template('productos.html', 
                          equipos=equipos,
                          empresa=NOMBRE_EMPRESA)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def producto_nuevo():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO productos (nombre, capacidad, precio, stock, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (form.nombre.data, form.capacidad.data, form.precio.data, 
              form.stock.data, form.categoria.data))
        conn.commit()
        conn.close()
        flash('✅ Producto creado correctamente', 'success')
        return redirect(url_for('productos'))
    return render_template('formularios/producto_form.html', 
                          form=form, 
                          titulo='Nuevo Producto',
                          empresa=NOMBRE_EMPRESA)

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def producto_editar(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE id = ?', (id,))
    producto = cursor.fetchone()
    conn.close()
    
    if not producto:
        flash('❌ Producto no encontrado', 'danger')
        return redirect(url_for('productos'))
    
    form = ProductoForm(data=dict(producto))
    if form.validate_on_submit():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE productos 
            SET nombre = ?, capacidad = ?, precio = ?, stock = ?, categoria = ?
            WHERE id = ?
        ''', (form.nombre.data, form.capacidad.data, form.precio.data, 
              form.stock.data, form.categoria.data, id))
        conn.commit()
        conn.close()
        flash('✅ Producto actualizado correctamente', 'success')
        return redirect(url_for('productos'))
    
    return render_template('formularios/producto_form.html', 
                          form=form, 
                          titulo='Editar Producto',
                          empresa=NOMBRE_EMPRESA)

@app.route('/productos/eliminar/<int:id>')
def producto_eliminar(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('✅ Producto eliminado correctamente', 'success')
    return redirect(url_for('productos'))

# ============================================================
# CRUD - CLIENTES (SQLite)
# ============================================================

@app.route('/clientes')
def clientes():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes ORDER BY id DESC')
    clientes = cursor.fetchall()
    conn.close()
    return render_template('clientes.html', 
                          clientes=clientes,
                          empresa=NOMBRE_EMPRESA)

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def cliente_nuevo():
    form = ClienteForm()
    if form.validate_on_submit():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (nombre, empresa, telefono, email, ciudad)
            VALUES (?, ?, ?, ?, ?)
        ''', (form.nombre.data, form.empresa.data, form.telefono.data, 
              form.email.data, form.ciudad.data))
        conn.commit()
        conn.close()
        flash('✅ Cliente creado correctamente', 'success')
        return redirect(url_for('clientes'))
    return render_template('formularios/cliente_form.html', 
                          form=form, 
                          titulo='Nuevo Cliente',
                          empresa=NOMBRE_EMPRESA)

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def cliente_editar(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes WHERE id = ?', (id,))
    cliente = cursor.fetchone()
    conn.close()
    
    if not cliente:
        flash('❌ Cliente no encontrado', 'danger')
        return redirect(url_for('clientes'))
    
    form = ClienteForm(data=dict(cliente))
    if form.validate_on_submit():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE clientes 
            SET nombre = ?, empresa = ?, telefono = ?, email = ?, ciudad = ?
            WHERE id = ?
        ''', (form.nombre.data, form.empresa.data, form.telefono.data, 
              form.email.data, form.ciudad.data, id))
        conn.commit()
        conn.close()
        flash('✅ Cliente actualizado correctamente', 'success')
        return redirect(url_for('clientes'))
    
    return render_template('formularios/cliente_form.html', 
                          form=form, 
                          titulo='Editar Cliente',
                          empresa=NOMBRE_EMPRESA)

@app.route('/clientes/eliminar/<int:id>')
def cliente_eliminar(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('✅ Cliente eliminado correctamente', 'success')
    return redirect(url_for('clientes'))

# ============================================================
# CRUD - PROVEEDORES (SQLite)
# ============================================================

@app.route('/proveedores')
def proveedores():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM proveedores ORDER BY id DESC')
    proveedores = cursor.fetchall()
    conn.close()
    return render_template('proveedores.html', 
                          proveedores=proveedores,
                          empresa=NOMBRE_EMPRESA)

@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def proveedor_nuevo():
    form = ProveedorForm()
    if form.validate_on_submit():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO proveedores (nombre, especialidad, contacto, telefono, pais)
            VALUES (?, ?, ?, ?, ?)
        ''', (form.nombre.data, form.especialidad.data, form.contacto.data, 
              form.telefono.data, form.pais.data))
        conn.commit()
        conn.close()
        flash('✅ Proveedor creado correctamente', 'success')
        return redirect(url_for('proveedores'))
    return render_template('formularios/proveedor_form.html', 
                          form=form, 
                          titulo='Nuevo Proveedor',
                          empresa=NOMBRE_EMPRESA)

@app.route('/proveedores/editar/<int:id>', methods=['GET', 'POST'])
def proveedor_editar(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM proveedores WHERE id = ?', (id,))
    proveedor = cursor.fetchone()
    conn.close()
    
    if not proveedor:
        flash('❌ Proveedor no encontrado', 'danger')
        return redirect(url_for('proveedores'))
    
    form = ProveedorForm(data=dict(proveedor))
    if form.validate_on_submit():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE proveedores 
            SET nombre = ?, especialidad = ?, contacto = ?, telefono = ?, pais = ?
            WHERE id = ?
        ''', (form.nombre.data, form.especialidad.data, form.contacto.data, 
              form.telefono.data, form.pais.data, id))
        conn.commit()
        conn.close()
        flash('✅ Proveedor actualizado correctamente', 'success')
        return redirect(url_for('proveedores'))
    
    return render_template('formularios/proveedor_form.html', 
                          form=form, 
                          titulo='Editar Proveedor',
                          empresa=NOMBRE_EMPRESA)

@app.route('/proveedores/eliminar/<int:id>')
def proveedor_eliminar(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM proveedores WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('✅ Proveedor eliminado correctamente', 'success')
    return redirect(url_for('proveedores'))

# ============================================================
# CRUD - FACTURAS (SQLite)
# ============================================================

@app.route('/facturacion')
def facturacion():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM facturas ORDER BY id DESC')
    facturas = cursor.fetchall()
    conn.close()
    return render_template('facturacion.html', 
                          facturas=facturas,
                          empresa=NOMBRE_EMPRESA)

@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
def factura_nueva():
    form = FacturaForm()
    if form.validate_on_submit():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO facturas (numero, cliente, equipo, inicio, fin, total)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (form.numero.data, form.cliente.data, form.equipo.data,
              form.inicio.data.strftime('%Y-%m-%d'),
              form.fin.data.strftime('%Y-%m-%d'),
              form.total.data))
        conn.commit()
        conn.close()
        flash('✅ Factura creada correctamente', 'success')
        return redirect(url_for('facturacion'))
    return render_template('formularios/factura_form.html', 
                          form=form, 
                          titulo='Nueva Factura',
                          empresa=NOMBRE_EMPRESA)

@app.route('/facturacion/editar/<int:id>', methods=['GET', 'POST'])
def factura_editar(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM facturas WHERE id = ?', (id,))
    factura = cursor.fetchone()
    conn.close()
    
    if not factura:
        flash('❌ Factura no encontrada', 'danger')
        return redirect(url_for('facturacion'))
    
    # Convertir strings a date para el formulario
    factura_dict = dict(factura)
    from datetime import datetime
    factura_dict['inicio'] = datetime.strptime(factura_dict['inicio'], '%Y-%m-%d').date()
    factura_dict['fin'] = datetime.strptime(factura_dict['fin'], '%Y-%m-%d').date()
    
    form = FacturaForm(data=factura_dict)
    if form.validate_on_submit():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE facturas 
            SET numero = ?, cliente = ?, equipo = ?, inicio = ?, fin = ?, total = ?
            WHERE id = ?
        ''', (form.numero.data, form.cliente.data, form.equipo.data,
              form.inicio.data.strftime('%Y-%m-%d'),
              form.fin.data.strftime('%Y-%m-%d'),
              form.total.data, id))
        conn.commit()
        conn.close()
        flash('✅ Factura actualizada correctamente', 'success')
        return redirect(url_for('facturacion'))
    
    return render_template('formularios/factura_form.html', 
                          form=form, 
                          titulo='Editar Factura',
                          empresa=NOMBRE_EMPRESA)

@app.route('/facturacion/eliminar/<int:id>')
def factura_eliminar(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM facturas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('✅ Factura eliminada correctamente', 'success')
    return redirect(url_for('facturacion'))

# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)