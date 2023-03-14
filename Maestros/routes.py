from flask import Blueprint
from flask import Flask, redirect, render_template
from flask import request
from flask import url_for
import forms
from flask import jsonify
from config import DevelopmentConfig
from flask_wtf.csrf import CSRFProtect
from db import get_connection
from models import Maestros
app=Flask(__name__)
app.config['DEBUG']=True
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

maestros=Blueprint('maestros',__name__)

@maestros.route('/getmaestros',methods=['GET'])
def getmaestros():
    create_form=forms.UseForm(request.form)
    maestros=[]
    try:
        connection=get_connection()
        with connection.cursor() as cursor:
            cursor.execute("CALL get_maestros()")
            resutset=cursor.fetchall()
            for row in resutset:
                maes=Maestros(id=row[0],
                    nombre=row[1],
                    apellidos=row[2],
                    email=row[3])
                maestros.append(maes)
    except Exception as ex:
        print(ex)
    return render_template('ABCompletoM.html',form=create_form,maestros=maestros)


@maestros.route("/agregar_maestro", methods=['GET','POST'])
def agregar_maestro():
    create_form=forms.UseForm(request.form)
    if request.method=='POST' and create_form.validate():
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                cursor.execute('CALL insert_maestro(%s,%s,%s)',(create_form.nombre.data,create_form.apellidos.data,create_form.email.data))
            connection.commit()
            connection.close()
        except Exception as ex:
            print('ERROR')
        return redirect(url_for('maestros.getmaestros'))
    return render_template('agregar_maestro.html',form=create_form)

@maestros.route("/modificar_maestro",methods=['GET','POST'])
def modificar_maestro():
    create_form=forms.UseForm(request.form)
    maestro = None  
    if request.method=='GET':
        id=request.args.get('id')
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                cursor.execute('CALL consultar_maestro(%s)',(id,))
                resutset=cursor.fetchall()
                for row in resutset:
                    maestro=Maestros(id=row[0],
                        nombre=row[1],
                        apellidos=row[2],
                        email=row[3])
        except Exception as ex:
            print('ERROR')
        if maestro is not None:
            create_form.id.data=request.args.get('id')
            create_form.nombre.data=maestro.nombre
            create_form.apellidos.data=maestro.apellidos
            create_form.email.data=maestro.email
    if request.method=='POST' and create_form.validate():
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                cursor.execute('CALL update_maestro(%s,%s,%s,%s)',(create_form.id.data,create_form.nombre.data,create_form.apellidos.data,create_form.email.data))
            connection.commit()
            connection.close()
        except Exception as ex:
            print('ERROR')
        return redirect(url_for('maestros.getmaestros'))
    return render_template('modificar_maestro.html',form=create_form)


@maestros.route("/eliminar_maestro",methods=['GET','POST'])
def eliminar_maestro():
    create_form=forms.UseForm(request.form)
    maestro = None  # inicializar maestro con un valor nulo
    if request.method=='GET':
        id=request.args.get('id')
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                cursor.execute('CALL consultar_maestro(%s)',(id,))
                resutset=cursor.fetchall()
                for row in resutset:
                    maestro=Maestros(id=row[0],
                        nombre=row[1],
                        apellidos=row[2],
                        email=row[3])
        except Exception as ex:
            print(ex)
        if maestro is not None:
            create_form.id.data=request.args.get('id')
            create_form.nombre.data=maestro.nombre
            create_form.apellidos.data=maestro.apellidos
            create_form.email.data=maestro.email
    if request.method=='POST':
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                cursor.execute('CALL delete_maestro(%s)',(create_form.id.data))
            connection.commit()
            connection.close()
        except Exception as ex:
            print('ERROR')
        return redirect(url_for('maestros.getmaestros'))
    return render_template('eliminar_maestro.html',form=create_form)  