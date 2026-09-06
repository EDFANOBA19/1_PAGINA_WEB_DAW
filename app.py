from flask import Flask, render_template, redirect, url_for, flash, request
import sqlite3
import os
from datetime import datetime

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
    """Crea las tablas si no existen"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Tabla de productos
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

    # Tabla de clientes
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

    conn.commit()
    conn.close()
    print("✅ Base de datos 'maquirenthal.db' creada correctamente")
    print("✅ Tabla 'productos' creada correctamente")
    print("✅ Tabla 'clientes' creada correctamente")

# Inicializar la base de datos al iniciar la aplicación
init_db()

# ============================================================
# DATOS DE EJEMPLO (PROVEEDORES, FACTURAS - EN MEMORIA)
# ============================================================

PROVEEDORES = [
    {'id': 1, 'nombre': 'Caterpillar', 'especialidad': 'Generadores', 'contacto': 'ventas@cat.com', 'telefono': '123456789', 'pais': 'EE.UU.'},
    {'id': 2, 'nombre': 'Cummins', 'especialidad': 'Motores y Generadores', 'contacto': 'info@cummins.com', 'telefono': '987654321', 'pais': 'EE.UU.'},
    {'id': 3, 'nombre': 'Atlas Copco', 'especialidad': 'Compresores', 'contacto': 'ventas@atlascopco.com', 'telefono': '456789123', 'pais': 'Suecia'},
    {'id': 4, 'nombre': 'Generac', 'especialidad': 'Torres de Iluminación', 'contacto': 'info@generac.com', 'telefono': '789123456', 'pais': 'EE.UU.'}
]

FACTURAS = [
    {'id': 1, 'numero': 'FAC-001', 'cliente': 'Carlos Mendoza', 'equipo': 'Generador 50kW', 'inicio': '2026-07-01', 'fin': '2026-07-07', 'total': 1960.00},
    {'id': 2, 'numero': 'FAC-002', 'cliente': 'María Fernández', 'equipo': 'Torres de Iluminación', 'inicio': '2026-07-05', 'fin': '2026-07-06', 'total': 360.00},
    {'id': 3, 'numero': 'FAC-003', 'cliente': 'José Ramírez', 'equipo': 'Compresor 150 CFM', 'inicio': '2026-07-10', 'fin': '2026-07-15', 'total': 1000.00},
    {'id': 4, 'numero': 'FAC-004', 'cliente': 'Ana Torres', 'equipo': 'Generador 100kW', 'inicio': '2026-07-12', 'fin': '2026-07-19', 'total': 3150.00}
]

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

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html', 
                          proveedores=PROVEEDORES)

@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html', 
                          facturas=FACTURAS)

# ============================================================
# CRUD - PRODUCTOS (CON SQLITE)
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
# CRUD - CLIENTES (AHORA CON SQLITE - CORREGIDO)
# ============================================================

@app.route('/clientes')
def clientes():
    """Lista todos los clientes desde SQLite"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes ORDER BY id DESC')
    lista_clientes = cursor.fetchall()
    conn.close()
    return render_template('clientes.html', 
                          clientes=lista_clientes,
                          empresa=NOMBRE_EMPRESA)

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def cliente_nuevo():
    """Crea un nuevo cliente en SQLite"""
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
    """Edita un cliente existente en SQLite"""
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
    """Elimina un cliente de SQLite"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('✅ Cliente eliminado correctamente', 'success')
    return redirect(url_for('clientes'))

# ============================================================
# CRUD - PROVEEDORES (EN MEMORIA)
# ============================================================

def obtener_siguiente_id(lista):
    if not lista:
        return 1
    return max(item['id'] for item in lista) + 1

@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def proveedor_nuevo():
    form = ProveedorForm()
    if form.validate_on_submit():
        nuevo_id = obtener_siguiente_id(PROVEEDORES)
        PROVEEDORES.append({
            'id': nuevo_id,
            'nombre': form.nombre.data,
            'especialidad': form.especialidad.data,
            'contacto': form.contacto.data,
            'telefono': form.telefono.data,
            'pais': form.pais.data
        })
        flash('✅ Proveedor creado correctamente', 'success')
        return redirect(url_for('proveedores'))
    return render_template('formularios/proveedor_form.html', 
                          form=form, 
                          titulo='Nuevo Proveedor',
                          empresa=NOMBRE_EMPRESA)

@app.route('/proveedores/editar/<int:id>', methods=['GET', 'POST'])
def proveedor_editar(id):
    proveedor = next((p for p in PROVEEDORES if p['id'] == id), None)
    if not proveedor:
        flash('❌ Proveedor no encontrado', 'danger')
        return redirect(url_for('proveedores'))
    
    form = ProveedorForm(data=proveedor)
    if form.validate_on_submit():
        proveedor['nombre'] = form.nombre.data
        proveedor['especialidad'] = form.especialidad.data
        proveedor['contacto'] = form.contacto.data
        proveedor['telefono'] = form.telefono.data
        proveedor['pais'] = form.pais.data
        flash('✅ Proveedor actualizado correctamente', 'success')
        return redirect(url_for('proveedores'))
    
    return render_template('formularios/proveedor_form.html', 
                          form=form, 
                          titulo='Editar Proveedor',
                          empresa=NOMBRE_EMPRESA)

@app.route('/proveedores/eliminar/<int:id>')
def proveedor_eliminar(id):
    proveedor = next((p for p in PROVEEDORES if p['id'] == id), None)
    if proveedor:
        PROVEEDORES.remove(proveedor)
        flash('✅ Proveedor eliminado correctamente', 'success')
    else:
        flash('❌ Proveedor no encontrado', 'danger')
    return redirect(url_for('proveedores'))

# ============================================================
# CRUD - FACTURAS (EN MEMORIA)
# ============================================================

@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
def factura_nueva():
    form = FacturaForm()
    if form.validate_on_submit():
        nuevo_id = obtener_siguiente_id(FACTURAS)
        FACTURAS.append({
            'id': nuevo_id,
            'numero': form.numero.data,
            'cliente': form.cliente.data,
            'equipo': form.equipo.data,
            'inicio': form.inicio.data.strftime('%Y-%m-%d'),
            'fin': form.fin.data.strftime('%Y-%m-%d'),
            'total': form.total.data
        })
        flash('✅ Factura creada correctamente', 'success')
        return redirect(url_for('facturacion'))
    return render_template('formularios/factura_form.html', 
                          form=form, 
                          titulo='Nueva Factura',
                          empresa=NOMBRE_EMPRESA)

@app.route('/facturacion/editar/<int:id>', methods=['GET', 'POST'])
def factura_editar(id):
    factura = next((f for f in FACTURAS if f['id'] == id), None)
    if not factura:
        flash('❌ Factura no encontrada', 'danger')
        return redirect(url_for('facturacion'))
    
    # Convertir strings a datetime antes de pasarlos al formulario
    factura_para_form = factura.copy()
    factura_para_form['inicio'] = datetime.strptime(factura['inicio'], '%Y-%m-%d')
    factura_para_form['fin'] = datetime.strptime(factura['fin'], '%Y-%m-%d')
    
    form = FacturaForm(data=factura_para_form)
    
    if form.validate_on_submit():
        factura['numero'] = form.numero.data
        factura['cliente'] = form.cliente.data
        factura['equipo'] = form.equipo.data
        factura['inicio'] = form.inicio.data.strftime('%Y-%m-%d')
        factura['fin'] = form.fin.data.strftime('%Y-%m-%d')
        factura['total'] = form.total.data
        flash('✅ Factura actualizada correctamente', 'success')
        return redirect(url_for('facturacion'))
    
    return render_template('formularios/factura_form.html', 
                          form=form, 
                          titulo='Editar Factura',
                          empresa=NOMBRE_EMPRESA)

@app.route('/facturacion/eliminar/<int:id>')
def factura_eliminar(id):
    factura = next((f for f in FACTURAS if f['id'] == id), None)
    if factura:
        FACTURAS.remove(factura)
        flash('✅ Factura eliminada correctamente', 'success')
    else:
        flash('❌ Factura no encontrada', 'danger')
    return redirect(url_for('facturacion'))

# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)