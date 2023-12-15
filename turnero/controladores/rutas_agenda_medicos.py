from flask import Blueprint, jsonify, request
from modelos.agenda_medicos import obtener_lista_agenda, agregar_horario, modificar_horarios_medico, borrar_horario

agenda_medicos_blueprint = Blueprint("agenda_medicos", __name__)

#id_medico,dia_numero,hora_inicio,hora_fin,fecha_actualizacion

@agenda_medicos_blueprint.route("/agenda_medicos/", methods=["GET"])
def get_agenda():
    if obtener_lista_agenda():
        return jsonify(obtener_lista_agenda()), 200
    else: 
        return jsonify({"Error":"Hubo un Error al buscar el archivo de los datos"}), 500

@agenda_medicos_blueprint.route("/agenda_medicos/", methods=["POST"])
def post_agregar_horario():
    if request.is_json:
        required_keys = ["id_medico", "dia_numero", "hora_inicio","hora_fin"]
        if all(key in request.json for key in required_keys):
            nuevo_horario = request.get_json()
            response = agregar_horario(nuevo_horario["id_medico"],nuevo_horario["dia_numero"],nuevo_horario["hora_inicio"],nuevo_horario["hora_fin"])
            if response == True:
                return jsonify({"Listo":"Nuevo horario agregado correctamente"}), 200
            elif response == 404:
                return jsonify({"Error":"No existe un medico con ese ID"}), 404
            elif response == None:
                return jsonify({"Error":"Hubo un Error al buscar el archivo de los datos"}), 500
            elif response == 400:
                return jsonify({"Error": "Datos incorrectos"}), 400
            elif response == False:
                return jsonify({"Error":"Ese medico ya tiene ese dia ocupado"}), 400
        else:
            return jsonify({"Error":"Faltan datos"}), 400
    else:
        return jsonify({"Error","Formato no aceptado"}), 406

@agenda_medicos_blueprint.route("/agenda_medicos/id/<int:id>", methods=["PUT"])
def put_modificar_horarios(id):
    if request.is_json:
        horario_a_editar = request.json
        resultado = modificar_horarios_medico(id,horario_a_editar)
        if resultado == 404:
            return jsonify({"Error":"No existe un medico con ese ID"}), 404
        elif resultado == None:
            return jsonify({"Error":"Hubo un Error al buscar el archivo de los datos"}), 500
        elif resultado == 400:
            return jsonify({"Error":"Datos incorrectos"}) ,400
        else:
            return jsonify({"Listo": "Horario actualizado"}), 200
    else: 
        return jsonify({"Error","Formato no aceptado"}), 406

@agenda_medicos_blueprint.route("/agenda_medicos/id/<int:id>", methods=["DELETE"])
def delete_horarios(id):
    resultado = borrar_horario(id)
    if resultado == None:
        return jsonify({"Error":"Hubo un Error al buscar el archivo de los datos"}), 500
    elif resultado == 404:
        return jsonify({"Error":"No existe un medico con ese ID"}), 404
    else: 
        return jsonify({"Listo":"Horario/s borrados correctamente"})