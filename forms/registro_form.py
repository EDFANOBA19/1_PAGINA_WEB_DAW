from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

class RegistroForm(FlaskForm):
    usuario = StringField('Nombre de Usuario', validators=[
        DataRequired(message='⚠️ El usuario es obligatorio'),
        Length(min=3, max=50, message='⚠️ El usuario debe tener entre 3 y 50 caracteres'),
        Regexp(r'^[a-zA-Z0-9_]+$', message='⚠️ Solo se permiten letras, números y guiones bajos')
    ])
    
    email = StringField('Correo Electrónico', validators=[
        DataRequired(message='⚠️ El correo es obligatorio'),
        Email(message='⚠️ Ingrese un correo electrónico válido (ejemplo@correo.com)'),
        Length(max=100, message='⚠️ El correo no puede tener más de 100 caracteres')
    ])
    
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='⚠️ La contraseña es obligatoria'),
        Length(min=6, max=100, message='⚠️ La contraseña debe tener al menos 6 caracteres')
    ])
    
    confirmar = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message='⚠️ Debe confirmar la contraseña'),
        EqualTo('password', message='⚠️ Las contraseñas no coinciden')
    ])
    
    submit = SubmitField('Registrarse')