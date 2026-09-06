from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf.csrf import CSRFProtect
from datetime import datetime # <--- CAMBIO 1: Importación necesaria para manejar fechas

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
# DATOS DE EJEMPLO (SIMULAN BASE DE DATOS)
# ============================================================

EQUIPOS = [
    {'id': 1, 'nombre': 'Generador Diésel', 'capacidad': '20 kW', 'precio': 150.00, 'stock': 8, 'categoria': 'generadores'},
    {'id': 2, 'nombre': 'Generador Diésel', 'capacidad': '50 kW', 'precio': 280.00, 'stock': 5, 'categoria': 'generadores'},
    {'id': 3, 'nombre': 'Generador Diésel', 'capacidad': '100 kW', 'precio': 450.00, 'stock': 0, 'categoria': 'generadores'},
    {'id': 4, 'nombre': 'Torre de Iluminación', 'capacidad': '4x1000W', 'precio': 120.00, 'stock': 10, 'categoria': 'iluminacion'},
    {'id': 5, 'nombre': 'Torre de Iluminación', 'capacidad': '4x1500W', 'precio': 180.00, 'stock': 3, 'categoria': 'iluminacion'},
    {'id': 6, 'nombre': 'Compresor de Aire', 'capacidad': '150 CFM', 'precio': 200.00, 'stock': 6, 'categoria': 'compresores'},
    {'id': 7, 'nombre': 'Compresor de Aire', 'capacidad': '300 CFM', 'precio': 350.00, 'stock': 0, 'categoria': 'compresores'}
]

CLIENTES = [
    {'id': 1, 'nombre': 'Carlos Mendoza', 'empresa': 'Construcciones Mendoza', 'telefono': '0987654321', 'email': 'carlos@mail.com', 'ciudad': 'Quito'},
    {'id': 2, 'nombre': 'María Fernández', 'empresa': 'Eventos Luz y Sonido', 'telefono': '0976543210', 'email': 'maria@mail.com', 'ciudad': 'Guayaquil'},
    {'id': 3, 'nombre': 'José Ramírez', 'empresa': 'Petrolera Amazonas', 'telefono': '0965432109', 'email': 'jose@mail.com', 'ciudad': 'Lago Agrio'},
    {'id': 4, 'nombre': 'Ana Torres', 'empresa': 'Energía del Sur', 'telefono': '0954321098', 'email': 'ana@mail.com', 'ciudad': 'Cuenca'}
]

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
# FUNCIÓN PARA OBTENER SIGUIENTE ID
# ============================================================

def obtener_siguiente_id(lista):
    if not lista:
        return 1
    return max(item['id'] for item in lista) + 1

# ============================================================
# RUTAS PRINCIPALES (SEMANA 9 y 10)
# ============================================================

@app.route('/')
def index():
    return render_template('index.html', 
                          empresa=NOMBRE_EMPRESA.upper(),
                          anio=ANIO_FUNDACION)

@app.route('/productos')
def productos():
    return render_template('productos.html', 
                          equipos=EQUIPOS,
                          empresa=NOMBRE_EMPRESA)

@app.route('/clientes')
def clientes():
    return render_template('clientes.html', 
                          clientes=CLIENTES)

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html', 
                          proveedores=PROVEEDORES)

@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html', 
                          facturas=FACTURAS)

# ============================================================
# CRUD - PRODUCTOS
# ============================================================

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def producto_nuevo():
    form = ProductoForm()
    if form.validate_on_submit():
        nuevo_id = obtener_siguiente_id(EQUIPOS)
        EQUIPOS.append({
            'id': nuevo_id,
            'nombre': form.nombre.data,
            'capacidad': form.capacidad.data,
            'precio': form.precio.data,
            'stock': form.stock.data,
            'categoria': form.categoria.data
        })
        flash('✅ Producto creado correctamente', 'success')
        return redirect(url_for('productos'))
    return render_template('formularios/producto_form.html', 
                          form=form, 
                          titulo='Nuevo Producto',
                          empresa=NOMBRE_EMPRESA)

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def producto_editar(id):
    producto = next((p for p in EQUIPOS if p['id'] == id), None)
    if not producto:
        flash('❌ Producto no encontrado', 'danger')
        return redirect(url_for('productos'))
    
    form = ProductoForm(data=producto)
    if form.validate_on_submit():
        producto['nombre'] = form.nombre.data
        producto['capacidad'] = form.capacidad.data
        producto['precio'] = form.precio.data
        producto['stock'] = form.stock.data
        producto['categoria'] = form.categoria.data
        flash('✅ Producto actualizado correctamente', 'success')
        return redirect(url_for('productos'))
    
    return render_template('formularios/producto_form.html', 
                          form=form, 
                          titulo='Editar Producto',
                          empresa=NOMBRE_EMPRESA)

@app.route('/productos/eliminar/<int:id>')
def producto_eliminar(id):
    producto = next((p for p in EQUIPOS if p['id'] == id), None)
    if producto:
        EQUIPOS.remove(producto)
        flash('✅ Producto eliminado correctamente', 'success')
    else:
        flash('❌ Producto no encontrado', 'danger')
    return redirect(url_for('productos'))

# ============================================================
# CRUD - CLIENTES
# ============================================================

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def cliente_nuevo():
    form = ClienteForm()
    if form.validate_on_submit():
        nuevo_id = obtener_siguiente_id(CLIENTES)
        CLIENTES.append({
            'id': nuevo_id,
            'nombre': form.nombre.data,
            'empresa': form.empresa.data,
            'telefono': form.telefono.data,
            'email': form.email.data,
            'ciudad': form.ciudad.data
        })
        flash('✅ Cliente creado correctamente', 'success')
        return redirect(url_for('clientes'))
    return render_template('formularios/cliente_form.html', 
                          form=form, 
                          titulo='Nuevo Cliente',
                          empresa=NOMBRE_EMPRESA)

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def cliente_editar(id):
    cliente = next((c for c in CLIENTES if c['id'] == id), None)
    if not cliente:
        flash('❌ Cliente no encontrado', 'danger')
        return redirect(url_for('clientes'))
    
    form = ClienteForm(data=cliente)
    if form.validate_on_submit():
        cliente['nombre'] = form.nombre.data
        cliente['empresa'] = form.empresa.data
        cliente['telefono'] = form.telefono.data
        cliente['email'] = form.email.data
        cliente['ciudad'] = form.ciudad.data
        flash('✅ Cliente actualizado correctamente', 'success')
        return redirect(url_for('clientes'))
    
    return render_template('formularios/cliente_form.html', 
                          form=form, 
                          titulo='Editar Cliente',
                          empresa=NOMBRE_EMPRESA)

@app.route('/clientes/eliminar/<int:id>')
def cliente_eliminar(id):
    cliente = next((c for c in CLIENTES if c['id'] == id), None)
    if cliente:
        CLIENTES.remove(cliente)
        flash('✅ Cliente eliminado correctamente', 'success')
    else:
        flash('❌ Cliente no encontrado', 'danger')
    return redirect(url_for('clientes'))

# ============================================================
# CRUD - PROVEEDORES
# ============================================================

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
# CRUD - FACTURAS (CORREGIDO)
# ============================================================

@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
def factura_nueva():
    form = FacturaForm()
    if form.validate_on_submit():
        nuevo_id = obtener_siguiente_id(FACTURAS)
        # Aquí convertimos los datetime del formulario a string para guardarlos en la lista
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
    
    # --- CORRECCIÓN CLAVE AQUÍ ---
    # Hacemos una copia para no modificar el original todavía
    factura_para_form = factura.copy() 
    # Convertimos los strings de fecha a objetos datetime para que WTForms los entienda
    factura_para_form['inicio'] = datetime.strptime(factura['inicio'], '%Y-%m-%d')
    factura_para_form['fin'] = datetime.strptime(factura['fin'], '%Y-%m-%d')
    
    form = FacturaForm(data=factura_para_form)
    # ------------------------------

    if form.validate_on_submit():
        factura['numero'] = form.numero.data
        factura['cliente'] = form.cliente.data
        factura['equipo'] = form.equipo.data
        # Volvemos a convertir los datetime del form a string para guardarlos
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