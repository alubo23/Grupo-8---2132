from datetime import date, datetime
from flask import Flask, jsonify, render_template, url_for, request, redirect, flash, session
import controlador
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)

app.secret_key='Mi clave Secreta'+str(datetime.now)

@app.route('/prueba')
def prueba():
    return True

@app.route('/consultarmail',methods=['GET','POST'])
def consulta_mail():
    if request.method=='POST':
        datos=request.get_json()
        usu=datos['username']
        tipo=datos['tipo']
        if tipo==1:
            resultado=controlador.listar_mensajes(1,'')
        else:
            resultado=controlador.listar_mensajes(2,usu)    
    else:
        resultado=controlador.listar_mensajes(1,'')      
    return jsonify(resultado)

@app.route('/consultamensajes')
def consulta_mensajes():
    usu='equipo_g8@outlook.com'
    resultado=controlador.listar_mensajes(usu)
    return jsonify(resultado)

@app.route('/consultamensajesind',methods=['POST'])
def consulta_mensajes_ind():
    datos=request.get_json()
    usu=datos['username']
    resultado=controlador.listar_mensajes(usu)
    return jsonify(resultado)

@app.route('/enviarmensaje', methods=['POST'])
def enviar_mensaje():
    datos=request.form
    usu=session['username']
    rem=session['email']
    dest=datos['destinatario']
    asu=datos['asunto']
    mens=datos['cuerpo']
    resultado=controlador.adicionar_mensajes(usu,rem,dest,asu,mens)
    if resultado:
        flash('Mensaje Enviado Exitosamente...')
    else:
        flash('Error Enviando Mensaje...')
    print(resultado)
    listaruser=controlador.listar_usuario(rem)
    return redirect(url_for('bandeja'))
    #return render_template('bandeja.html', datauser=listaruser)

@app.route('/activarCuenta', methods=['POST'])
def activarCuenta():
    datos=request.form
    Usuario=datos['Usuario']
    Cod_Verificacion=datos['Codigo']
    if Usuario=='' and Cod_Verificacion=='':
        flash('Datos Incompletos')
        return redirect('/validar')
    else:
        resultado=controlador.activar_cuenta(Usuario, Cod_Verificacion)
        if resultado==True:
            flash('Cuenta Activada Safisfactoriamente')
            return redirect('/login')   
        else:
            flash('Error en la activación de la activación')
            return redirect('/validar')
                                
@app.route('/verificar', methods=['POST'])
def validarlogin():
    datos=request.form
    Usu=datos['Usuario']
    Contraseña=datos['Contraseña']
    if Usu==''and Contraseña=='':
       flash('Datos Incompletos')
       return redirect(url_for('login'))
    elif len(Contraseña)<=6:    
       flash('La contraseña debe tener minimo 6 caracteres')
       return redirect(url_for('login'))
    else:
        resultado=controlador.validacion_login(Usu)
        if resultado==False:
            flash('Usuario/Contraseña Incorrectos')
            return redirect(url_for('login'))
        else:
            if check_password_hash(resultado[0]['Contraseña'],Contraseña):
                if resultado[0]['Verificado']==1:
                    session['username']=Usu
                    session['email']=resultado[0]['Email']
                    listaruser=controlador.listar_usuario(Usu)
                    print(listaruser)
                    return render_template('bandeja.html', datauser=listaruser)
                else:
                    return redirect(url_for('validar'))
            else:
                flash('Contraseña Incorrecta')
                return redirect(url_for('login'))
            
@app.route('/addregistro', methods=['POST'])
def add_registro():
    datos=request.form
    Usuario=datos['Usuario']
    Contraseña=datos['Contraseña']
    Email=datos['Email']
    ContraseñaEnc=generate_password_hash(Contraseña)
    if Usuario==''and Contraseña=='' and Email=='':
        flash('Datos Incompletos')
    elif len(Contraseña)<=6:    
        flash('La contraseña debe tener minimo 6 caracteres')
    else:
        resultado=controlador.adicionar_registros(Usuario,ContraseñaEnc,Email)
        if resultado:
            flash('Registro Almacenado Correctamente')
            return redirect(url_for('login'))
        else:
            flash('Ha ocurrido un error')
    return redirect(url_for('registro'))   
    
@app.route('/recuperarcontra', methods=['POST'])
def recuperarcontra():
    datos=request.form
    Email=datos['Email']
    if  Email=='':
        flash('Ingrese un correo')     
    else:
        resultado = controlador.validarcorreo(Email)
        if resultado=='SI':
            flash('Usuario Encontrado: Mensaje enviado al correo')
        elif resultado=='NO':
            flash('Usuario NO Existe en la base de datos')    
        else:
            flash('No se Puede ejecutar la consulta, intente mas tarde')
    return redirect(url_for('restablecer'))   

@app.route('/actualizarcontra', methods=['POST'])
def actualizarcontra():
    datos=request.form
    Usuario=datos['Usuario']
    Contraseña1=datos['Contraseña1']
    Contraseña2=datos['Contraseña2']
    if Usuario=="" or Contraseña1=="" or Contraseña2=="":
        flash('Datos Incompletos')
    elif len(Contraseña1)<=6:    
        flash('La contraseña debe tener minimo 6 caracteres')
    elif Contraseña1 != Contraseña2:
        flash('Las contraseñas no son iguales')
        redirect(url_for('/nueva-contra'))
    else:
        ContraseñaEnc=generate_password_hash(Contraseña1)
        resultado=controlador.actualizar_contra(Usuario,ContraseñaEnc)
        if resultado:
            flash('Actualización realizada correctamente')
            return redirect(url_for('login'))
        else:
            flash('Ha ocurrido un error')
    return redirect(url_for('login'))

### RUTAS DE NAVEGACIÓN ###  
@app.route('/')
def index():
    return render_template('login.html')
 
@app.route('/bandeja')
def bandeja():
    listaruser=controlador.listar_usuario(session['username'])
    return render_template('bandeja.html', datauser=listaruser)

@app.route('/login')
def login():
    session.clear()
    return render_template('login.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/nueva-contra')
def nueva_contra():
    return render_template('nueva-contra.html')

@app.route('/restablecer')
def restablecer():
    return render_template('restablecer.html')

@app.route('/validar')
def validar():
    return render_template('validar.html')

@app.route('/politicas')
def politicas():
    return render_template('politicas.html')

if  __name__=='__main__':
     app.run(debug=True) 