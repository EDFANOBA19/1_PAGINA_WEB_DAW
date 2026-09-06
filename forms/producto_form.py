from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del Equipo', validators=[
        DataRequired(message='⚠️ El nombre es obligatorio'),
        Length(min=3, max=100, message='⚠️ El nombre debe tener entre 3 y 100 caracteres'),
        Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message='⚠️ Solo se permiten letras y espacios')
    ])
    
    capacidad = StringField('Capacidad', validators=[
        DataRequired(message='⚠️ La capacidad es obligatoria'),
        Length(min=2, max=50, message='⚠️ La capacidad debe tener entre 2 y 50 caracteres')
    ])
    
    precio = FloatField('Precio por Día (USD)', validators=[
        DataRequired(message='⚠️ El precio es obligatorio'),
        NumberRange(min=0.01, message='⚠️ El precio debe ser mayor a 0')
    ])
    
    stock = IntegerField('Stock Disponible', validators=[
        DataRequired(message='⚠️ El stock es obligatorio'),
        NumberRange(min=0, message='⚠️ El stock no puede ser negativo')
    ])
    
    categoria = SelectField('Categoría', choices=[
        ('generadores', 'Generadores'),
        ('iluminacion', 'Iluminación'),
        ('compresores', 'Compresores'),
        ('otros', 'Otros')
    ], validators=[DataRequired(message='⚠️ Seleccione una categoría')])
    
    submit = SubmitField('Guardar Producto')