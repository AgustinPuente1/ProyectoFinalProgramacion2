import os
import csv
from modelos.medicos import id_medicos_horarios
import random
import datetime
from datetime import datetime

directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_csv_agenda = os.path.join(directorio_actual, 'agenda_medicos.csv')

agenda = []
#id_medico,dia_numero,hora_inicio,hora_fin,fecha_actualizacion
medicos = [] #para cuando se importen los medicos para ver que id de medico usar para crear los horarios

def importar_desde_csv():
    global agenda 
    if verificador_ruta() == False:
        return None

    agenda = []  # Limpiamos la lista de agenda antes de importar desde el archivo CSV
    with open(ruta_csv_agenda, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convertimos el ID de cadena a entero
            row['id_medico'] = int(row['id_medico'])
            agenda.append(row) 

def exportar_a_csv():
    global agenda
    ordenar_agenda() #por si fue agregado un nuevo horario
    #reescribe el archivo
    if verificador_ruta() == True:
        with open(ruta_csv_agenda, 'w', newline='') as csvfile:
            campo_nombres = ['id_medico','dia_numero','hora_inicio','hora_fin','fecha_actualizacion']
            writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
            writer.writeheader()
            for horario in agenda:
                writer.writerow(horario)
    else: 
        return None

def verificador_ruta(): #verifica si la ruta es correcta
    if os.path.exists(ruta_csv_agenda):
        return True
    else:
        print("no se encontro el archivo")
        return False
    
def ordenar_agenda():
    global agenda
    agenda = sorted(agenda, key=lambda x: (x['id_medico'], int(x['dia_numero'])))

def asignacion_horarios_medicos():
    global medicos
    global agenda

    importar_desde_csv()
    #si ya hay una agenda sale de la funcion
    if agenda:
        return 

    #se agarran las id de los medicos
    ids_disponibles = id_medicos_horarios()

    #horarios random a ser asignados aleatoriamente a las distintas id
    horarios = [["08:00","13:00"],["09:00","14:00"],["14:00","19:00"],["13:00","18:00"],["07:30","12:30"],["09:30","13:30"],["13:30","19:30"],["12:00","17:00"],["07:00","11:30"],["8:30","12:00"]]

    for id in ids_disponibles: 
        dias_semana = [1,2,3,4,5] #dias a ser elimandos para elegir los dias que trabaja el medico
        cantidad_dias_no_trabajados = random.randint(1,4)

        #elimina los dias que no va a trabajar
        for i in range(cantidad_dias_no_trabajados):
            dia_eliminar = random.choice(dias_semana)
            dias_semana.remove(dia_eliminar)

        for dia in dias_semana:
            #suponiendo que cada medico tiene su propio consultorio y que no importa si 
            #medicos diferentes en el mismo dia comparten horario
            horario_random = random.randint(0,9) #para sacar que horas va a trabajar
            hora_a_trabajar = horarios[horario_random]
            fecha_actual = datetime.now()
            fecha = fecha_actual.strftime("%d/%m/%Y")

            id_medico = id
            dia_numero = dia
            hora_inicio = hora_a_trabajar[0]
            hora_fin = hora_a_trabajar[1]
            fecha_actualizacion = fecha

            horario_a_trabajar = {"id_medico":id_medico,"dia_numero":dia_numero,"hora_inicio":hora_inicio,"hora_fin":hora_fin,"fecha_actualizacion":fecha_actualizacion}
            agenda.append(horario_a_trabajar)
    
    exportar_a_csv()
    
def obtener_lista_agenda():#GET
    global agenda
    importar_desde_csv()
    if verificador_ruta() == True:
        return agenda
    else: 
        return None
    
def termina_en_minutos(hora):
    #convierte la cadena de hora a un objeto datetime
    formato_hora = "%H:%M"  # Formato de hora de 24 horas
    objeto_hora = datetime.strptime(hora, formato_hora)
    
    #obtiene los minutos de la hora
    minutos = objeto_hora.minute
    
    if minutos in [0, 15, 30, 45]:
        return True
    else:
        return False

def comparar_horas(hora1, hora2):
    formato_hora = "%H:%M"  # Formato de hora de 24 horas
    
    # Convertir las cadenas de hora a objetos datetime
    objeto_hora1 = datetime.strptime(hora1, formato_hora)
    objeto_hora2 = datetime.strptime(hora2, formato_hora)

    if objeto_hora1 < objeto_hora2:
        return True
    else: 
        return False

def agregar_horario(id_medico,nuevo_dia_numero,nueva_hora_inicio,nueva_hora_fin): #POST
    global agenda

    if verificador_ruta() == False:
        return None
    importar_desde_csv()
    if termina_en_minutos(nueva_hora_inicio) == False or termina_en_minutos(nueva_hora_fin) == False or comparar_horas(nueva_hora_inicio, nueva_hora_fin) == False:
        return 400  # Datos incorrectos
    
    for horario in agenda:
        if (int(horario["id_medico"]) == int(id_medico)) and (int(horario["dia_numero"]) == int(nuevo_dia_numero)):
            return False

    ids_disponibles = id_medicos_horarios()
    #en las id disponibles busca si esta la id del medico que se ingreso
    #luego busca en la agenda si la id del medico ingresado esta en la agenda
    #luego busca en los dia_numero si el horario ya existe o tiene que agregar uno nuevo
    for id in ids_disponibles:
        if int(id_medico) == int(id):
            fecha_actual = datetime.now()
            fecha = fecha_actual.strftime("%d/%m/%Y")
            nuevo_horario = {"id_medico": id_medico, "dia_numero": nuevo_dia_numero, "hora_inicio": nueva_hora_inicio, "hora_fin": nueva_hora_fin, "fecha_actualizacion": fecha}
            agenda.append(nuevo_horario)
            exportar_a_csv()
            return True

    return 404 #la id ingresada no corresponde a la id de un medico        

def modificar_horarios_medico(id_medico, horarios_nuevos): #PUT
    global agenda

    if verificador_ruta() == False:
        return None
    
    ids_disponibles = id_medicos_horarios()

    for id in ids_disponibles:
        if int(id_medico) == int(id):
            for nuevo_horario in horarios_nuevos:
                if ("hora_inicio" not in nuevo_horario) or ("hora_fin" not in nuevo_horario) or ("dia" not in nuevo_horario):
                    return 400 #faltan datos

                if termina_en_minutos(nuevo_horario["hora_inicio"]) == False:
                    return 400 #datos incorrectos
                if termina_en_minutos(nuevo_horario["hora_fin"]) == False:
                    return 400 #datos incorrectos
                if comparar_horas(nuevo_horario["hora_inicio"],nuevo_horario["hora_fin"]) == False:
                    return 400 #datos incorrectos
                dia_modificar = nuevo_horario["dia"]
                hora_inicio_mod = nuevo_horario["hora_inicio"]
                hora_fin_mod = nuevo_horario["hora_fin"]
                
                # Verifica que el día a modificar esté dentro de los días laborales del médico
                for horario in agenda:
                    if int(horario["id_medico"]) == int(id_medico) and int(horario["dia_numero"]) == int(dia_modificar):
                        horario["hora_inicio"] = hora_inicio_mod
                        horario["hora_fin"] = hora_fin_mod
                        fecha_actual = datetime.now()
                        fecha = fecha_actual.strftime("%d/%m/%Y")
                        horario["fecha_actualizacion"] = fecha
                        break  # Termina el bucle interno cuando se encuentra y modifica el día
            exportar_a_csv()
            return True         
    return 404

def borrar_horario(id_medico): #DELETE
    if verificador_ruta() == False:
        return None

    efectividad_borrado = False
    horarios_a_borrar = []
    for horario in agenda:
        if int(horario["id_medico"]) == int(id_medico):
                horarios_a_borrar.append(horario)
                efectividad_borrado = True

    for borrar in horarios_a_borrar:
        agenda.remove(borrar)

    if efectividad_borrado == False:
        return 404
    else:
        exportar_a_csv()
        return True


#print(agregar_medico(10,3,"12:00","13:00"))
#sas = [{"dia":"4","hora_inicio":"10:13","hora_fin":"10:45"},{"dia":"5","hora_inicio":"10:15","hora_fin":"10:45"}]
#print(modificar_horarios_medico(10,sas))
#print(id_medicos_horarios())
#borrar_horario(10)


