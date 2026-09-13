from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp

class FacturaForm(FlaskForm):
    numero = StringField('Número de Factura', validators=[
        DataRequired(message='⚠️ El número de factura es obligatorio'),
        Length(min=3, max=20, message='⚠️ El número debe tener entre 3 y 20 caracteres'),
        Regexp(r'^[A-Za-z0-9\-]+$', message='⚠️ Solo se permiten letras, números y guiones')
    ])
    
    id_cliente = SelectField('Cliente', coerce=int, validators=[
        DataRequired(message='⚠️ Seleccione un cliente')
    ])
    
    equipo = StringField('Equipo', validators=[
        DataRequired(message='⚠️ El equipo es obligatorio'),
        Length(min=3, max=100, message='⚠️ El equipo debe tener entre 3 y 100 caracteres')
    ])
    
    inicio = DateField('Fecha de Inicio', validators=[
        DataRequired(message='⚠️ La fecha de inicio es obligatoria')
    ])
    
    fin = DateField('Fecha de Fin', validators=[
        DataRequired(message='⚠️ La fecha de fin es obligatoria')
    ])
    
    total = FloatField('Total (USD)', validators=[
        DataRequired(message='⚠️ El total es obligatorio'),
        NumberRange(min=0.01, message='⚠️ El total debe ser mayor a 0')
    ])
    
    submit = SubmitField('Guardar Factura')