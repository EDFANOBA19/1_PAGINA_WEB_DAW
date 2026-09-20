from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[
        DataRequired(message='⚠️ El correo es obligatorio'),
        Length(min=5, max=100, message='⚠️ El correo debe tener entre 5 y 100 caracteres')
    ])
    
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='⚠️ La contraseña es obligatoria'),
        Length(min=6, max=100, message='⚠️ La contraseña debe tener al menos 6 caracteres')
    ])
    
    submit = SubmitField('Iniciar Sesión')