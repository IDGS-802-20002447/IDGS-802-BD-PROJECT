from wtforms import Form
from wtforms import StringField, IntegerField
from wtforms import EmailField
from wtforms import validators

class UseForm(Form):
    id=IntegerField('Id')
    nombre=StringField('Nombre',[validators.DataRequired(message='Nombre requerido')])
    apellidos=StringField('Apellidos',[validators.DataRequired(message='Apellido requerido')])
    email=EmailField('Correo',[validators.DataRequired(message='Correo requerido')])