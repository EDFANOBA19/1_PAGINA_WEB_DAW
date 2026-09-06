from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp

class ProveedorForm(FlaskForm):
    nombre = StringField('Nombre del Proveedor', validators=[
        DataRequired(message='⚠️ El nombre es obligatorio'),
        Length(min=3, max=100, message='⚠️ El nombre debe tener entre 3 y 100 caracteres'),
        Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message='⚠️ Solo se permiten letras y espacios')
    ])
    
    especialidad = StringField('Especialidad', validators=[
        DataRequired(message='⚠️ La especialidad es obligatoria'),
        Length(min=3, max=100, message='⚠️ La especialidad debe tener entre 3 y 100 caracteres'),
        Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message='⚠️ Solo se permiten letras y espacios')
    ])
    
    contacto = StringField('Correo de Contacto', validators=[
        DataRequired(message='⚠️ El correo es obligatorio'),
        Email(message='⚠️ Ingrese un correo electrónico válido (ejemplo@correo.com)')
    ])
    
    telefono = StringField('Teléfono', validators=[
        DataRequired(message='⚠️ El teléfono es obligatorio'),
        Length(min=7, max=20, message='⚠️ El teléfono debe tener entre 7 y 20 caracteres'),
        Regexp(r'^[0-9+\-\s]+$', message='⚠️ Solo se permiten números, +, - y espacios')
    ])
    
    pais = StringField('País', validators=[
        DataRequired(message='⚠️ El país es obligatorio'),
        Length(min=2, max=50, message='⚠️ El país debe tener entre 2 y 50 caracteres'),
        Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message='⚠️ Solo se permiten letras y espacios')
    ])
    
    submit = SubmitField('Guardar Proveedor')