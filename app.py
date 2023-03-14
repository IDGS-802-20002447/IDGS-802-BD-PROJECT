from flask import Flask, redirect, render_template
from flask import request
from flask import url_for
import forms

from flask import jsonify
from config import DevelopmentConfig
from flask_wtf.csrf import CSRFProtect
from models import db #ORM SQLAlquime
from models import Alumnos
from Alumnos.routes import alumnos
from Maestros.routes import maestros

app=Flask(__name__)
app.config['DEBUG']=True
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()
app.register_blueprint(alumnos)
app.register_blueprint(maestros)


    
@app.route("/", methods=['GET','POST'])
def index():
    create_form=forms.UseForm(request.form)
    return render_template('ABCompletoM.html',form=create_form)

if __name__=='__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=3000)