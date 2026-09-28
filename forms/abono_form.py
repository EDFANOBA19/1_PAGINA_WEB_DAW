from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

class AbonoForm(FlaskForm):
    monto = DecimalField('Monto a Abonar (USD)', validators=[
        DataRequired(message='⚠️ El monto es obligatorio'),
        NumberRange(min=0.01, message='⚠️ El monto debe ser mayor a 0')
    ])
    
    forma_pago = SelectField('Forma de Pago', choices=[
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
        ('Cheque', 'Cheque')
    ], validators=[DataRequired()])
    
    referencia = StringField('Referencia (N° Transacción)', validators=[Optional()])
    
    observaciones = TextAreaField('Observaciones', validators=[Optional()])
    
    submit = SubmitField('Registrar Abono')