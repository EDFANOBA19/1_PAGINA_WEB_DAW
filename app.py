from flask import Flask, render_template

app = Flask(__name__)

# ============================================================
# DATOS DE EJEMPLO
# ============================================================

EQUIPOS = [
    {'nombre': 'Generador Diésel', 'capacidad': '20 kW', 'precio': '$150', 'disponible': True},
    {'nombre': 'Generador Diésel', 'capacidad': '50 kW', 'precio': '$280', 'disponible': True},
    {'nombre': 'Generador Diésel', 'capacidad': '100 kW', 'precio': '$450', 'disponible': False},
    {'nombre': 'Torre de Iluminación', 'capacidad': '4x1000W', 'precio': '$120', 'disponible': True},
    {'nombre': 'Torre de Iluminación', 'capacidad': '4x1500W', 'precio': '$180', 'disponible': True},
    {'nombre': 'Compresor de Aire', 'capacidad': '150 CFM', 'precio': '$200', 'disponible': True},
    {'nombre': 'Compresor de Aire', 'capacidad': '300 CFM', 'precio': '$350', 'disponible': False}
]

CLIENTES = [
    {'nombre': 'Carlos Mendoza', 'empresa': 'Construcciones Mendoza', 'telefono': '0987654321', 'equipos': 'Generador 50kW'},
    {'nombre': 'María Fernández', 'empresa': 'Eventos Luz y Sonido', 'telefono': '0976543210', 'equipos': 'Torres de Iluminación'},
    {'nombre': 'José Ramírez', 'empresa': 'Petrolera Amazonas', 'telefono': '0965432109', 'equipos': 'Compresor 150 CFM'},
    {'nombre': 'Ana Torres', 'empresa': 'Energía del Sur', 'telefono': '0954321098', 'equipos': 'Generador 100kW'}
]

PROVEEDORES = [
    {'nombre': 'Caterpillar', 'especialidad': 'Generadores', 'contacto': 'ventas@cat.com', 'equipos': 'Generadores Diésel'},
    {'nombre': 'Cummins', 'especialidad': 'Motores y Generadores', 'contacto': 'info@cummins.com', 'equipos': 'Generadores'},
    {'nombre': 'Atlas Copco', 'especialidad': 'Compresores', 'contacto': 'ventas@atlascopco.com', 'equipos': 'Compresores de Aire'},
    {'nombre': 'Generac', 'especialidad': 'Torres de Iluminación', 'contacto': 'info@generac.com', 'equipos': 'Torres de Iluminación'}
]

FACTURAS = [
    {'numero': 'FAC-001', 'cliente': 'Carlos Mendoza', 'equipo': 'Generador 50kW', 'inicio': '2026-07-01', 'fin': '2026-07-07', 'total': '$1,960'},
    {'numero': 'FAC-002', 'cliente': 'María Fernández', 'equipo': 'Torres de Iluminación', 'inicio': '2026-07-05', 'fin': '2026-07-06', 'total': '$360'},
    {'numero': 'FAC-003', 'cliente': 'José Ramírez', 'equipo': 'Compresor 150 CFM', 'inicio': '2026-07-10', 'fin': '2026-07-15', 'total': '$1,000'},
    {'numero': 'FAC-004', 'cliente': 'Ana Torres', 'equipo': 'Generador 100kW', 'inicio': '2026-07-12', 'fin': '2026-07-19', 'total': '$3,150'}
]

# ============================================================
# RUTAS
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    return render_template('productos.html', equipos=EQUIPOS)

@app.route('/clientes')
def clientes():
    return render_template('clientes.html', clientes=CLIENTES)

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html', proveedores=PROVEEDORES)

@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html', facturas=FACTURAS)

# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)