from flask import Flask, render_template

app = Flask(__name__)

# ============================================================
# DATOS DE EJEMPLO (SEMANA 10)
# ============================================================

EQUIPOS = [
    {'nombre': 'Generador Diésel', 'capacidad': '20 kW', 'precio': 150.00, 'stock': 8, 'categoria': 'generadores'},
    {'nombre': 'Generador Diésel', 'capacidad': '50 kW', 'precio': 280.00, 'stock': 5, 'categoria': 'generadores'},
    {'nombre': 'Generador Diésel', 'capacidad': '100 kW', 'precio': 450.00, 'stock': 0, 'categoria': 'generadores'},
    {'nombre': 'Torre de Iluminación', 'capacidad': '4x1000W', 'precio': 120.00, 'stock': 10, 'categoria': 'iluminacion'},
    {'nombre': 'Torre de Iluminación', 'capacidad': '4x1500W', 'precio': 180.00, 'stock': 3, 'categoria': 'iluminacion'},
    {'nombre': 'Compresor de Aire', 'capacidad': '150 CFM', 'precio': 200.00, 'stock': 6, 'categoria': 'compresores'},
    {'nombre': 'Compresor de Aire', 'capacidad': '300 CFM', 'precio': 350.00, 'stock': 0, 'categoria': 'compresores'}
]

CLIENTES = [
    {'nombre': 'Carlos Mendoza', 'empresa': 'Construcciones Mendoza', 'telefono': '0987654321', 'equipos': 'Generador 50kW', 'ciudad': 'QUITO'},
    {'nombre': 'María Fernández', 'empresa': 'Eventos Luz y Sonido', 'telefono': '0976543210', 'equipos': 'Torres de Iluminación', 'ciudad': 'guayaquil'},
    {'nombre': 'José Ramírez', 'empresa': 'Petrolera Amazonas', 'telefono': '0965432109', 'equipos': 'Compresor 150 CFM', 'ciudad': 'lago agrio'},
    {'nombre': 'Ana Torres', 'empresa': 'Energía del Sur', 'telefono': '0954321098', 'equipos': 'Generador 100kW', 'ciudad': 'cuenca'}
]

PROVEEDORES = [
    {'nombre': 'Caterpillar', 'especialidad': 'GENERADORES', 'contacto': 'ventas@cat.com', 'equipos': 'Generadores Diésel', 'pais': 'EE.UU.'},
    {'nombre': 'Cummins', 'especialidad': 'MOTORES Y GENERADORES', 'contacto': 'info@cummins.com', 'equipos': 'Generadores', 'pais': 'EE.UU.'},
    {'nombre': 'Atlas Copco', 'especialidad': 'COMPRESORES', 'contacto': 'ventas@atlascopco.com', 'equipos': 'Compresores de Aire', 'pais': 'SUECIA'},
    {'nombre': 'Generac', 'especialidad': 'TORRES DE ILUMINACIÓN', 'contacto': 'info@generac.com', 'equipos': 'Torres de Iluminación', 'pais': 'EE.UU.'}
]

FACTURAS = [
    {'numero': 'FAC-001', 'cliente': 'Carlos Mendoza', 'equipo': 'Generador 50kW', 'inicio': '2026-07-01', 'fin': '2026-07-07', 'total': 1960.00},
    {'numero': 'FAC-002', 'cliente': 'María Fernández', 'equipo': 'Torres de Iluminación', 'inicio': '2026-07-05', 'fin': '2026-07-06', 'total': 360.00},
    {'numero': 'FAC-003', 'cliente': 'José Ramírez', 'equipo': 'Compresor 150 CFM', 'inicio': '2026-07-10', 'fin': '2026-07-15', 'total': 1000.00},
    {'numero': 'FAC-004', 'cliente': 'Ana Torres', 'equipo': 'Generador 100kW', 'inicio': '2026-07-12', 'fin': '2026-07-19', 'total': 3150.00}
]

# ============================================================
# VARIABLES SIMPLES
# ============================================================

NOMBRE_EMPRESA = "maquirenthal"
ANIO_FUNDACION = 2023

# ============================================================
# RUTAS
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
# EJECUCIÓN
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)