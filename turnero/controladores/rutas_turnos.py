from flask import Blueprint, jsonify, request
from modelos.turnos import obtener_turno_medico_xid, obtener_turnos_pendientes_xid, agregar_turno, borrar_turno

turnos_blueprint = Blueprint("turnos", __name__)

@turnos_blueprint.route("/turnos/id/<int:id>", methods=["GET"])
def get_obtener_turno_xid_medico(id):
    turno = obtener_turno_medico_xid(id)
    if (turno != 404) and (turno != None): 
        return jsonify(turno), 200
    elif turno == 404:
        return jsonify({"Error":"No existe un medico con turnos con ese ID o no tiene turnos"}), 404
    else:
        return jsonify({"Error":"Hubo un Error al buscar el archivo de los datos"}), 500

@turnos_blueprint.route("/turnos/id/<int:id>", methods=["GET"])
def get_obtener_turno_xid_medico_pendientes(id):
    turno = obtener_turnos_pendientes_xid(id)
    if isinstance(turno, dict): 
        return jsonify(turno), 200
    elif turno == 404:
        return jsonify({"Error":"No existe un medico con turnos pendientes con ese ID o no tiene turnos"}), 404
    else:
        return jsonify({"Error":"Hubo un Error al buscar el archivo de los datos"}), 500

@turnos_blueprint.route("/turnos/", methods=["POST"])
def post_agregar_turno():
    if request.is_json:
        required_keys = ["id_medico", "id_paciente", "hora_turno", "fecha_solicitud"]
        if all(key in request.json for key in required_keys):
            nuevo_turno = request.get_json()
            resultado = agregar_turno(nuevo_turno["id_medico"],nuevo_turno["id_paciente"],nuevo_turno["hora_turno"],nuevo_turno["fecha_solicitud"])
            if resultado == True:
                return jsonify({"Listo":"Nuevo turno agregado correctamente"}), 200
            elif resultado == 400:
                return jsonify({"Error":"Datos erroneos"}), 400
            elif resultado == 404:
                return jsonify({"Error":"Ningun paciente o medico fue encontrado con esas ID"}), 404
            elif resultado == None:
                return jsonify({"Error":"Hubo un Error al buscar el archivo de los datos"}), 500
        else:
            return jsonify({"Error":"Faltan datos"}), 400
    else:
        return jsonify({"Error","Formato no aceptado"}), 406
    
@turnos_blueprint.route("/turnos/", methods=["DELETE"])
def delete_turno():
    if request.is_json:
        required_keys = ["id_medico", "id_paciente", "hora_turno", "fecha_solicitud"]
        if all(key in request.json for key in required_keys):
            nuevo_turno = request.get_json()
            resultado = borrar_turno(nuevo_turno["id_medico"],nuevo_turno["id_paciente"],nuevo_turno["hora_turno"],nuevo_turno["fecha_solicitud"])
            if resultado == True:
                return jsonify({"Listo":"EL turno fue borrado correctamente"}), 200
            elif resultado == 404:
                return jsonify({"Error":"Datos erroneos"}), 404
            else:
                return jsonify({"Error":"Hubo un Error al buscar el archivo de los datos"}), 500
        else:
            return jsonify({"Error":"Faltan datos"}), 400
    else:
        return jsonify({"Error","Formato no aceptado"}), 406


