from flask import Blueprint, jsonify, request
from modelos.medicos import obtener_lista_medicos, obtener_medico_xid, agregar_medico, actualizar_medico_xid, habilitacion_medico_xid

medicos_blueprint = Blueprint("medicos", __name__)

@medicos_blueprint.route("/medicos/", methods=["GET"])
def get_medicos():
    if obtener_lista_medicos():
        return jsonify(obtener_lista_medicos()), 200
    else: 
        return jsonify({"Error":"Hubo un Error al buscar el archivo de los datos"}), 500

@medicos_blueprint.route("/medicos/id/<int:id>", methods=["GET"])
def get_medico_xid(id):
    medico = obtener_medico_xid(id)
    if isinstance(medico, dict): 
        return jsonify(medico), 200
    elif medico == 404:
        return jsonify({"Error":"No existe un medico con ese ID"}), 404
    else:
        return jsonify({"Error":"Hubo un Error al buscar el archivo de los datos"}), 500

@medicos_blueprint.route("/medicos/", methods=["POST"])
def post_agregar_medico():
    if request.is_json:
        required_keys = ["dni", "nombre", "apellido", "matricula", "telefono", "email"]
        if all(key in request.json for key in required_keys):
            nuevo_medico = request.get_json()
            if agregar_medico(nuevo_medico["dni"],nuevo_medico["nombre"],nuevo_medico["apellido"],nuevo_medico["matricula"],nuevo_medico["telefono"],nuevo_medico["email"]) == True:
                return jsonify({"Listo":"Nuevo medico agregado correctamente"}), 200
            else:
                return jsonify({"Error":"Hubo un Error al buscar el archivo de los datos"}), 500
        else:
            return jsonify({"Error":"Faltan datos"}), 400
    else:
        return jsonify({"Error","Formato no aceptado"}), 406

@medicos_blueprint.route("/medicos/id/<int:id>", methods=["PUT"])
def put_actualizar_medico_xid(id):
    if request.is_json:
        if ("dni" in request.json) or ("nombre" in request.json) or ("apellido" in request.json) or ("matricula" in request.json) or ("telefono" in request.json) or ("email" in request.json):
            try:
                medico_a_editar = request.json

                dni = medico_a_editar.get("dni")
                nombre = medico_a_editar.get("nombre")
                apellido = medico_a_editar.get("apellido")
                matricula = medico_a_editar.get("matricula")
                telefono = medico_a_editar.get("telefono")
                email = medico_a_editar.get("email")
                resultado = actualizar_medico_xid(id,dni,nombre,apellido,matricula,telefono,email)
                if resultado == 404:
                    return jsonify({"Error":"No existe un medico con ese ID"}), 404
                elif resultado == None:
                    return jsonify({"Error":"Hubo un Error al buscar el archivo de los datos"}), 500
                else:
                    return jsonify({"Listo": "Medico actualizado"}), 200
            except TypeError:
                return jsonify({"Error": "Datos incorrectos"}), 400
        else: 
            return jsonify({"Error": "Ninguno de los datos ingresados corresponde a los datos de los medicos"}), 400
    else: 
        return jsonify({"Error","Formato no aceptado"}), 406
    
@medicos_blueprint.route("/medicos/habilitacion/<int:id>", methods=["PUT"])
def put_habilitacion_medico_xid(id):
    if request.is_json:
        if "habilitado" in request.json:
            archivojson = request.json
            habilitacion = archivojson.get("habilitado")
            if (habilitacion != "True") and (habilitacion != "False"):
                return jsonify({"Error": "Datos incorrectos, la habitacion debe ser True o False"}), 400 
            else:
                habilitacion = True if habilitacion == "True" else False
                resultado = habilitacion_medico_xid(id,habilitacion)
                if resultado == True:
                    return jsonify({"Listo":"El medico {id} fue habilitado para recibir turnos"}), 200
                elif resultado == False:
                    return jsonify({"Listo":"El medico {id} fue inhabilitado para recibir turnos"}), 200
                elif resultado == 404:
                    return jsonify({"Error":"No existe un medico con ese ID"}), 404
                else:
                    return jsonify({"Error":"Hubo un Error al buscar el archivo de los datos"}), 500
        else:
            return jsonify({"Error": "Ninguno de los datos ingresados es la habilitacion"}), 400
    else: 
        return jsonify({"Error","Formato no aceptado"}), 406
                