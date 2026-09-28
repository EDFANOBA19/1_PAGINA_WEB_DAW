from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, Regexp, ValidationError

class FacturaForm(FlaskForm):
    numero = StringField('Número de Factura', validators=[
        DataRequired(message='⚠️ El número es obligatorio'),
        Length(min=3, max=20, message='⚠️ Entre 3 y 20 caracteres'),
        Regexp(r'^[A-Za-z0-9\-]+$', message='⚠️ Solo letras, números y guiones')
    ])
    
    id_cliente = SelectField('Cliente', coerce=int, validators=[
        DataRequired(message='⚠️ Seleccione un cliente')
    ])
    
    id_producto = SelectField('Equipo/Servicio', coerce=int, validators=[
        DataRequired(message='⚠️ Seleccione un equipo')
    ])
    
    fecha_inicio = DateField('Fecha de Inicio', validators=[
        DataRequired(message='⚠️ La fecha de inicio es obligatoria')
    ])
    
    fecha_fin = DateField('Fecha de Fin', validators=[
        DataRequired(message='⚠️ La fecha de fin es obligatoria')
    ])
    
    forma_pago = SelectField('Forma de Pago', choices=[
        ('Efectivo', '💵 Efectivo'),
        ('Transferencia', '🏦 Transferencia Bancaria'),
        ('Cheque', '📝 Cheque'),
        ('Tarjeta de Crédito', '💳 Tarjeta de Crédito'),
        ('Crédito Directo', '📅 Crédito Directo')
    ], validators=[DataRequired(message='⚠️ Seleccione una forma de pago')])
    
    tipo_tarjeta = SelectField('Tipo de Tarjeta', choices=[
        ('', '-- Seleccione --'),
        ('Visa', 'Visa'),
        ('Mastercard', 'Mastercard'),
        ('American Express', 'American Express'),
        ('Diners Club', 'Diners Club'),
        ('Otra', 'Otra')
    ], validators=[Optional()])
    
    meses_diferidos = IntegerField('Diferir a (meses)', validators=[
        Optional(),
        NumberRange(min=0, max=36, message='⚠️ El máximo permitido es 36 meses')
    ], default=0)
    
    observaciones = TextAreaField('Observaciones', validators=[
        Optional(),
        Length(max=500, message='⚠️ Máximo 500 caracteres')
    ])
    
    submit = SubmitField('Guardar Factura')
    
    # Validación personalizada: Fecha fin debe ser mayor a fecha inicio
    def validate_fecha_fin(self, field):
        if self.fecha_inicio.data and field.data:
            if field.data <= self.fecha_inicio.data:
                raise ValidationError('⚠️ La fecha de fin debe ser mayor a la fecha de inicio')
    
    # Validación personalizada: Si es Crédito Directo, meses debe ser >= 1
    def validate_meses_diferidos(self, field):
        if self.forma_pago.data == 'Crédito Directo':
            if not field.data or field.data < 1:
                raise ValidationError('⚠️ El crédito directo debe ser mínimo 1 mes')
            if field.data > 36:
                raise ValidationError('⚠️ El crédito directo no puede superar 36 meses')
        
        if self.forma_pago.data == 'Tarjeta de Crédito':
            if field.data and field.data > 36:
                raise ValidationError('⚠️ El diferido de tarjeta no puede superar 36 meses')
    
    # Validación personalizada: Si es Tarjeta de Crédito, debe seleccionar tipo
    def validate_tipo_tarjeta(self, field):
        if self.forma_pago.data == 'Tarjeta de Crédito':
            if not field.data:
                raise ValidationError('⚠️ Debe seleccionar el tipo de tarjeta')