import csv
import requests
import os
from flask import jsonify
from datetime import datetime,  timedelta
import random
from modelos.agenda_medicos import termina_en_minutos, obtener_lista_agenda
from modelos.pacientes import obtener_lista_pacientes

turnos = []
agenda = []
pacientes = []
#id_medico,id_paciente,hora_turno,fecha_solicitud 
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_csv_turnos = os.path.join(directorio_actual, 'turnos.csv')

def exportar_a_csv():
    global turnos
    #reescribe el archivo
    if verificador_ruta() == True:
        with open(ruta_csv_turnos, 'w', newline='') as csvfile:
            campo_nombres = ['id_medico','id_paciente','hora_turno','fecha_solicitud']
            writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
            writer.writeheader()
            for turno in turnos:
                writer.writerow(turno)
    else: 
        return None

def importar_desde_csv():
    global turnos 
    if verificador_ruta() == True:
        turnos = []  # Limpiamos la lista de turnos antes de importar desde el archivo CSV
        with open(ruta_csv_turnos, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convertimos el ID de cadena a entero
                row['id_medico'] = int(row['id_medico'])
                turnos.append(row) 
    else:
        return None
    
def verificador_ruta(): #verifica si la ruta es correcta
    if os.path.exists(ruta_csv_turnos):
        return True
    else:
        print("no se encontro el archivo")
        return False
    
def verificar_formatos(hora, fecha):
    try:
        datetime.strptime(hora, '%H:%M')
        datetime.strptime(fecha, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def obtener_lista_turnos():
    global turnos
    if verificador_ruta() == True:
        return turnos
    else: 
        return None

def obtener_turno_medico_xid(id): #GET
    global turnos
    if verificador_ruta() == False:
        return None
    turnos_solicitados = []
    for turno in turnos:
        if int(id) == int(turno["id_medico"]):
            turnos_solicitados.append(turno)
    
    if turnos_solicitados:
        return turnos_solicitados
    else:
        return 404

def obtener_turnos_pendientes_xid(id): #GET
    global turnos
    if verificador_ruta() == False:
        return None
    
    turnos_pendientes = []
    medico_encontrado = False

    for turno in turnos:
        if int(id) == int(turno["id_medico"]):
            medico_encontrado = True
            fecha_turno = datetime.strptime(turno["fecha_solicitud"] + ' ' + turno["hora_turno"], '%d/%m/%Y %H:%M')
            fecha_actual = datetime.now()
            if fecha_actual < fecha_turno:
                turnos_pendientes.append(turno)
    
    if medico_encontrado == False:
        return 404
    
    return turnos_pendientes

def agregar_turno(id_medico,id_paciente,hora_turno,fecha_solicitud): #POST
    global turnos
    if verificador_ruta() == False:
        return None
    
    if verificar_formatos(hora_turno,fecha_solicitud) == False:
        return 400

    fecha_nuevo_turno = datetime.strptime(fecha_solicitud, "%d/%m/%Y")
    fecha_nuevo_turno_numero = fecha_nuevo_turno.strftime('%w')

    agenda = obtener_lista_agenda()
    if agenda == None:
        return None
    
    if termina_en_minutos(hora_turno) == False:
        return 400
    
    pacientes = obtener_lista_pacientes()
    if pacientes == None:
        return
    paciente_encontrado = False
    for paciente in pacientes:
        if int(paciente["id"]) == int(id_paciente):
            paciente_encontrado = True

    if paciente_encontrado == False:
        return 404

    #busca en agenda
    #si la id buscada esta en agenda
    #si el dia numero esta dentro de los dias laborales
    #y si esta dentro de su horario
    for horario in agenda:
        if int(id_medico) == int(horario["id_medico"]):
            if int(fecha_nuevo_turno_numero) == int(horario["dia_numero"]):
                hora_a_comparar = datetime.strptime(hora_turno, '%H:%M').time()
                hora_inicio = datetime.strptime(horario["hora_inicio"], '%H:%M').time()
                hora_fin = datetime.strptime(horario["hora_fin"], '%H:%M').time()
                for turno in turnos:
                    hora_turno_a_comparar = datetime.strptime(turno["hora_turno"], '%H:%M').time()
                    if hora_turno_a_comparar == hora_a_comparar and (turno["id_medico"] == id_medico):
                        return 400
                if (hora_inicio <= hora_a_comparar) and (hora_a_comparar <= hora_fin):
                    nuevo_turno = {"id_medico":id_medico,"id_paciente":id_paciente,"hora_turno":hora_turno,"fecha_solicitud":fecha_solicitud}
                    turnos.append(nuevo_turno)
                    exportar_a_csv()
                    return True
                else: 
                    return 400
    return 404

def borrar_turno(id_medico,id_paciente,hora_turno,fecha_solicitud): #DELETE
    global turnos
    if verificador_ruta() == False:
        return None
    
    if verificar_formatos(hora_turno,fecha_solicitud) == False:
        return 400
    
    for turno in turnos:
        if (int(turno["id_medico"]) == int(id_medico)) and (int(turno["id_paciente"]) == int(id_paciente)) and (turno["hora_turno"] == hora_turno) and (turno["fecha_solicitud"] == fecha_solicitud):
            turnos.remove(turno)
            exportar_a_csv()
            return True
    return 404

def asignacion_turnos():
    global turnos
    importar_desde_csv()
    if turnos:
        return

    agenda = obtener_lista_agenda()
    pacientes = obtener_lista_pacientes()

    # Definir la fecha actual y la fecha límite dentro de los próximos 30 días
    fecha_actual = datetime.now()
    fecha_limite = fecha_actual + timedelta(days=30)

    for _ in range(250):
        # Seleccionar aleatoriamente un médico y un paciente
        medico = random.choice(agenda)
        paciente = random.choice(pacientes)

        # Generar una fecha de solicitud aleatoria entre hoy y 30 días después
        fecha_solicitud = fecha_actual + timedelta(days=random.randint(0, 30))

        # Elegir una hora entre la hora_inicio y hora_fin del médico en intervalos de 15 minutos
        hora_inicio = datetime.strptime(medico["hora_inicio"], "%H:%M")
        hora_fin = datetime.strptime(medico["hora_fin"], "%H:%M")
        diferencia_horas = (hora_fin - hora_inicio).total_seconds() / 3600
        num_intervalos = int(diferencia_horas * 4)  # 4 intervalos por hora (00, 15, 30, 45 minutos)
        hora_turno = hora_inicio + timedelta(minutes=random.randint(0, num_intervalos - 1) * 15)
        hora_turno_str = hora_turno.strftime("%H:%M")

        # Verificar si la fecha de solicitud es válida
        fecha_solicitud_numero = fecha_solicitud.strftime('%w')
        if int(medico["dia_numero"]) == int(fecha_solicitud_numero):    
            if fecha_actual <= fecha_solicitud <= fecha_limite:
                nuevo_turno = {
                    "id_medico": medico["id_medico"],
                    "id_paciente": paciente["id"],
                    "hora_turno": hora_turno_str,
                    "fecha_solicitud": fecha_solicitud.strftime("%d/%m/%Y")
                }
                repeticion_de_turno = False
                for turno in turnos:
                    if turno == nuevo_turno:
                        repeticion_de_turno == True
                if repeticion_de_turno == False:
                    turnos.append(nuevo_turno)

    exportar_a_csv()

#print(asignacion_turnos())


#obtener_turnos_pendientes_xid(10)


