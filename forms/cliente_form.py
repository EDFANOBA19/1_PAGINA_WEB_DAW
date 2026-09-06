from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[
        DataRequired(message='⚠️ El nombre es obligatorio'),
        Length(min=3, max=100, message='⚠️ El nombre debe tener entre 3 y 100 caracteres'),
        Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message='⚠️ Solo se permiten letras y espacios')
    ])
    
    empresa = StringField('Empresa', validators=[
        DataRequired(message='⚠️ La empresa es obligatoria'),
        Length(min=2, max=100, message='⚠️ La empresa debe tener entre 2 y 100 caracteres')
    ])
    
    telefono = StringField('Teléfono', validators=[
        DataRequired(message='⚠️ El teléfono es obligatorio'),
        Length(min=7, max=20, message='⚠️ El teléfono debe tener entre 7 y 20 caracteres'),
        Regexp(r'^[0-9+\-\s]+$', message='⚠️ Solo se permiten números, +, - y espacios')
    ])
    
    email = StringField('Correo Electrónico', validators=[
        DataRequired(message='⚠️ El correo es obligatorio'),
        Email(message='⚠️ Ingrese un correo electrónico válido (ejemplo@correo.com)')
    ])
    
    ciudad = StringField('Ciudad', validators=[
        DataRequired(message='⚠️ La ciudad es obligatoria'),
        Length(min=2, max=50, message='⚠️ La ciudad debe tener entre 2 y 50 caracteres'),
        Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message='⚠️ Solo se permiten letras y espacios')
    ])
    
    submit = SubmitField('Guardar Cliente')