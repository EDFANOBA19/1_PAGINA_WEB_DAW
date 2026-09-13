from flask import Flask, render_template, redirect, url_for, flash
import mysql.connector

# Importar formularios
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturaForm

# Importar conexión
from conexion.conexion import get_db_connection

app = Flask(__name__)

# ============================================================
# CONFIGURACIÓN
# ============================================================

app.config['SECRET_KEY'] = 'maquirenthal-secret-key-2026'

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'  # <-- CAMBIA ESTO
app.config['MYSQL_DATABASE'] = 'maquirenthal_db'

# ============================================================
# VARIABLES SIMPLES
# ============================================================

NOMBRE_EMPRESA = "maquirenthal"
ANIO_FUNDACION = 2023

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def obtener_proveedores():
    """Obtiene la lista de proveedores para los selects"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, nombre FROM proveedores ORDER BY nombre')
    proveedores = cursor.fetchall()
    cursor.close()
    conn.close()
    return proveedores

def obtener_clientes():
    """Obtiene la lista de clientes para los selects"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, nombre FROM clientes ORDER BY nombre')
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return clientes

# ============================================================
# RUTAS PRINCIPALES
# ============================================================

@app.route('/')
def index():
    return render_template('index.html', 
                          empresa=NOMBRE_EMPRESA.upper(),
                          anio=ANIO_FUNDACION)

# ============================================================
# CRUD - PRODUCTOS (MySQL)
# ============================================================

@app.route('/productos')
def productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT p.*, pr.nombre AS proveedor_nombre 
        FROM productos p
        LEFT JOIN proveedores pr ON p.id_proveedor = pr.id
        ORDER BY p.id_producto DESC
    ''')
    equipos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('productos.html', 
                          equipos=equipos,
                          empresa=NOMBRE_EMPRESA)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def producto_nuevo():
    form = ProductoForm()
    form.id_proveedor.choices = [(p['id'], p['nombre']) for p in obtener_proveedores()]
    
    if form.validate_on_submit():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO productos (nombre, capacidad, precio, stock, categoria, id_proveedor)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (form.nombre.data, form.capacidad.data, form.precio.data, 
              form.stock.data, form.categoria.data, form.id_proveedor.data))
        conn.commit()
        cursor.close()
        conn.close()
        flash('✅ Producto creado correctamente', 'success')
        return redirect(url_for('productos'))
    return render_template('formulario_producto.html', 
                          form=form, 
                          titulo='Nuevo Producto',
                          empresa=NOMBRE_EMPRESA)

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def producto_editar(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos WHERE id_producto = %s', (id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not producto:
        flash('❌ Producto no encontrado', 'danger')
        return redirect(url_for('productos'))
    
    form = ProductoForm(data=producto)
    form.id_proveedor.choices = [(p['id'], p['nombre']) for p in obtener_proveedores()]
    
    if form.validate_on_submit():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE productos 
            SET nombre = %s, capacidad = %s, precio = %s, stock = %s, categoria = %s, id_proveedor = %s
            WHERE id_producto = %s
        ''', (form.nombre.data, form.capacidad.data, form.precio.data, 
              form.stock.data, form.categoria.data, form.id_proveedor.data, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('✅ Producto actualizado correctamente', 'success')
        return redirect(url_for('productos'))
    
    return render_template('formulario_producto.html', 
                          form=form, 
                          titulo='Editar Producto',
                          empresa=NOMBRE_EMPRESA)

@app.route('/productos/eliminar/<int:id>')
def producto_eliminar(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id_producto = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('✅ Producto eliminado correctamente', 'success')
    return redirect(url_for('productos'))

# ============================================================
# CRUD - CLIENTES (MySQL)
# ============================================================

@app.route('/clientes')
def clientes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM clientes ORDER BY id DESC')
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clientes.html', 
                          clientes=clientes,
                          empresa=NOMBRE_EMPRESA)

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def cliente_nuevo():
    form = ClienteForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (nombre, empresa, telefono, email, ciudad)
            VALUES (%s, %s, %s, %s, %s)
        ''', (form.nombre.data, form.empresa.data, form.telefono.data, 
              form.email.data, form.ciudad.data))
        conn.commit()
        cursor.close()
        conn.close()
        flash('✅ Cliente creado correctamente', 'success')
        return redirect(url_for('clientes'))
    return render_template('formulario_cliente.html', 
                          form=form, 
                          titulo='Nuevo Cliente',
                          empresa=NOMBRE_EMPRESA)

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def cliente_editar(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM clientes WHERE id = %s', (id,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not cliente:
        flash('❌ Cliente no encontrado', 'danger')
        return redirect(url_for('clientes'))
    
    form = ClienteForm(data=cliente)
    if form.validate_on_submit():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE clientes 
            SET nombre = %s, empresa = %s, telefono = %s, email = %s, ciudad = %s
            WHERE id = %s
        ''', (form.nombre.data, form.empresa.data, form.telefono.data, 
              form.email.data, form.ciudad.data, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('✅ Cliente actualizado correctamente', 'success')
        return redirect(url_for('clientes'))
    
    return render_template('formulario_cliente.html', 
                          form=form, 
                          titulo='Editar Cliente',
                          empresa=NOMBRE_EMPRESA)

@app.route('/clientes/eliminar/<int:id>')
def cliente_eliminar(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('✅ Cliente eliminado correctamente', 'success')
    return redirect(url_for('clientes'))

# ============================================================
# CRUD - PROVEEDORES (MySQL)
# ============================================================

@app.route('/proveedores')
def proveedores():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM proveedores ORDER BY id DESC')
    proveedores = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('proveedores.html', 
                          proveedores=proveedores,
                          empresa=NOMBRE_EMPRESA)

@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def proveedor_nuevo():
    form = ProveedorForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO proveedores (nombre, especialidad, contacto, telefono, pais)
            VALUES (%s, %s, %s, %s, %s)
        ''', (form.nombre.data, form.especialidad.data, form.contacto.data, 
              form.telefono.data, form.pais.data))
        conn.commit()
        cursor.close()
        conn.close()
        flash('✅ Proveedor creado correctamente', 'success')
        return redirect(url_for('proveedores'))
    return render_template('formulario_proveedor.html', 
                          form=form, 
                          titulo='Nuevo Proveedor',
                          empresa=NOMBRE_EMPRESA)

@app.route('/proveedores/editar/<int:id>', methods=['GET', 'POST'])
def proveedor_editar(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM proveedores WHERE id = %s', (id,))
    proveedor = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not proveedor:
        flash('❌ Proveedor no encontrado', 'danger')
        return redirect(url_for('proveedores'))
    
    form = ProveedorForm(data=proveedor)
    if form.validate_on_submit():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE proveedores 
            SET nombre = %s, especialidad = %s, contacto = %s, telefono = %s, pais = %s
            WHERE id = %s
        ''', (form.nombre.data, form.especialidad.data, form.contacto.data, 
              form.telefono.data, form.pais.data, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('✅ Proveedor actualizado correctamente', 'success')
        return redirect(url_for('proveedores'))
    
    return render_template('formulario_proveedor.html', 
                          form=form, 
                          titulo='Editar Proveedor',
                          empresa=NOMBRE_EMPRESA)

@app.route('/proveedores/eliminar/<int:id>')
def proveedor_eliminar(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM proveedores WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('✅ Proveedor eliminado correctamente', 'success')
    return redirect(url_for('proveedores'))

# ============================================================
# CRUD - FACTURAS (MySQL)
# ============================================================

@app.route('/facturacion')
def facturacion():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT f.*, c.nombre AS cliente_nombre 
        FROM facturas f
        LEFT JOIN clientes c ON f.id_cliente = c.id
        ORDER BY f.id DESC
    ''')
    facturas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('facturacion.html', 
                          facturas=facturas,
                          empresa=NOMBRE_EMPRESA)

@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
def factura_nueva():
    form = FacturaForm()
    form.id_cliente.choices = [(c['id'], c['nombre']) for c in obtener_clientes()]
    
    if form.validate_on_submit():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO facturas (numero, id_cliente, equipo, inicio, fin, total)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (form.numero.data, form.id_cliente.data, form.equipo.data,
              form.inicio.data, form.fin.data, form.total.data))
        conn.commit()
        cursor.close()
        conn.close()
        flash('✅ Factura creada correctamente', 'success')
        return redirect(url_for('facturacion'))
    return render_template('formulario_facturacion.html', 
                          form=form, 
                          titulo='Nueva Factura',
                          empresa=NOMBRE_EMPRESA)

@app.route('/facturacion/editar/<int:id>', methods=['GET', 'POST'])
def factura_editar(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM facturas WHERE id = %s', (id,))
    factura = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not factura:
        flash('❌ Factura no encontrada', 'danger')
        return redirect(url_for('facturacion'))
    
    form = FacturaForm(data=factura)
    form.id_cliente.choices = [(c['id'], c['nombre']) for c in obtener_clientes()]
    
    if form.validate_on_submit():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE facturas 
            SET numero = %s, id_cliente = %s, equipo = %s, inicio = %s, fin = %s, total = %s
            WHERE id = %s
        ''', (form.numero.data, form.id_cliente.data, form.equipo.data,
              form.inicio.data, form.fin.data, form.total.data, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('✅ Factura actualizada correctamente', 'success')
        return redirect(url_for('facturacion'))
    
    return render_template('formulario_facturacion.html', 
                          form=form, 
                          titulo='Editar Factura',
                          empresa=NOMBRE_EMPRESA)

@app.route('/facturacion/eliminar/<int:id>')
def factura_eliminar(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM facturas WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('✅ Factura eliminada correctamente', 'success')
    return redirect(url_for('facturacion'))

# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)