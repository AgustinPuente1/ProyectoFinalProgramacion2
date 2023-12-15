from flask import Blueprint, jsonify, request
from modelos.pacientes import obtener_lista_pacientes, obtener_paciente_xid, agregar_paciente, actualizar_paciente_xid, borrar_paciente_xid

pacientes_blueprint = Blueprint("pacientes", __name__)

@pacientes_blueprint.route("/pacientes/", methods=["GET"])
def get_pacientes():
    if obtener_lista_pacientes():
        return jsonify(obtener_lista_pacientes()), 200
    else: 
        return jsonify({"Error":"Hubo un Error al buscar el archivo de los datos"}), 500

@pacientes_blueprint.route("/pacientes/id/<int:id>", methods=["GET"])
def get_paciente_xid(id):
    paciente = obtener_paciente_xid(id)
    if isinstance(paciente, dict): 
        return jsonify(paciente), 200
    elif paciente == 404:
        return jsonify({"Error":"No existe un paciente con ese ID"}), 404
    else:
        return jsonify({"Error":"Hubo un Error al buscar el archivo de los datos"}), 500

@pacientes_blueprint.route("/pacientes/", methods=["POST"])
def post_agregar_paciente():
    if request.is_json:
        required_keys = ["dni", "nombre", "apellido", "telefono", "email", "direccion_calle", "direccion_numero"]
        if all(key in request.json for key in required_keys):
            nuevo_paciente = request.get_json()
            if agregar_paciente(nuevo_paciente["dni"],nuevo_paciente["nombre"],nuevo_paciente["apellido"],nuevo_paciente["telefono"],nuevo_paciente["email"],nuevo_paciente["direccion_calle"],nuevo_paciente["direccion_numero"]) == True:
                return jsonify({"Listo":"Nuevo paciente agregado correctamente"}), 200
            else:
                return jsonify({"Error":"Hubo un Error al buscar el archivo de los datos"}), 500
        else:
            return jsonify({"Error":"Faltan datos"}), 400
    else:
        return jsonify({"Error","Formato no aceptado"}), 406

@pacientes_blueprint.route("/pacientes/id/<int:id>", methods=["PUT"])
def put_actualizar_paciente_xid(id):
    if request.is_json:
        if ("dni" in request.json) or ("nombre" in request.json) or ("apellido" in request.json) or ("telefono" in request.json) or ("email" in request.json) or ("direccion_calle" in request.json) or ("direccion_numero" in request.json):
            try:
                paciente_a_editar = request.json

                dni = paciente_a_editar.get("dni")
                nombre = paciente_a_editar.get("nombre")
                apellido = paciente_a_editar.get("apellido")
                telefono = paciente_a_editar.get("telefono")
                email = paciente_a_editar.get("email")
                direccion_calle = paciente_a_editar.get("direccion_calle")
                direccion_numero = paciente_a_editar.get("direccion_numero")

                resultado = actualizar_paciente_xid(id,dni,nombre,apellido,telefono,email,direccion_calle,direccion_numero)
                if resultado == 404:
                    return jsonify({"Error":"No existe un paciente con ese ID"}), 404
                elif resultado == None:
                    return jsonify({"Error":"Hubo un Error al buscar el archivo de los datos"}), 500
                else:
                    return jsonify({"Listo": "Paciente actualizado"}), 200
            except TypeError:
                return jsonify({"Error": "Datos incorrectos"}), 400
        else: 
            return jsonify({"Error": "Ninguno de los datos ingresados corresponde a los datos de los pacientes"}), 400
    else: 
        return jsonify({"Error","Formato no aceptado"}), 406
    
@pacientes_blueprint.route("/pacientes/id/<int:id>", methods=["DELETE"])
def delete_paciente_sin_turnos_xid(id):
    resultado = borrar_paciente_xid(id)
    if resultado == True:
        return jsonify({"Listo":"Se borro correctamente ese paciente"}), 200
    elif resultado == 404:
        return jsonify({"Error":"No existe un paciente con ese ID"}), 404
    elif resultado == False:
        return jsonify({"Error":"No se puede eliminar este paciente porque tiene turnos pendientes"}), 400
    else:
        return jsonify({"Error":"Hubo un Error al buscar el archivo de los datos"}), 500