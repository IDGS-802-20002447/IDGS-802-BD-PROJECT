from flask import Blueprint
from flask import Flask, redirect, render_template
from flask import request
from flask import url_for
import forms
from flask import jsonify
from config import DevelopmentConfig
from flask_wtf.csrf import CSRFProtect
from models import db #ORM SQLAlquime
from models import Alumnos
alumnos=Blueprint('alumnos',__name__)
app=Flask(__name__)
app.config['DEBUG']=True
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

@alumnos.route('/getalum',methods=['GET'])
def getalum():
    create_form=forms.UseForm(request.form)
    alumnos=Alumnos.query.all()
    #alumnos = Alumnos.query.filter(Alumnos.nombre.like('%CO%')).all()
    return render_template('ABCompleto.html',form=create_form,alumnos=alumnos)


@alumnos.route("/agregar", methods=['GET','POST'])
def agregar():
    create_form=forms.UseForm(request.form)
    if request.method=='POST' and create_form.validate():
        alum=Alumnos(nombre=create_form.nombre.data,
                    apellidos=create_form.apellidos.data,
                    email=create_form.email.data)
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('alumnos.getalum'))
    return render_template('agregar.html',form=create_form)

@alumnos.route("/modificar",methods=['GET','POST'])
def modificar():
    create_form=forms.UseForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data=alum1.nombre
        create_form.apellidos.data=alum1.apellidos
        create_form.email.data=alum1.email
    if request.method=='POST' and create_form.validate():
        id=create_form.id.data
        alum=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum.nombre=create_form.nombre.data
        alum.apellidos=create_form.apellidos.data
        alum.email=create_form.email.data
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('alumnos.getalum'))
    return render_template('modificar.html',form=create_form)

@alumnos.route("/eliminar",methods=['GET','POST'])
def eliminar():
    create_form=forms.UseForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data=alum1.nombre
        create_form.apellidos.data=alum1.apellidos
        create_form.email.data=alum1.email
    if request.method=='POST':
        id=create_form.id.data
        alum=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum.nombre=create_form.nombre.data
        alum.apellidos=create_form.apellidos.data
        alum.email=create_form.email.data
        db.session.delete(alum)
        db.session.commit()
        return redirect(url_for('alumnos.getalum'))
    return render_template('eliminar.html',form=create_form)  