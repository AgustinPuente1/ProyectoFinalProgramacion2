import csv
import requests
import os
from flask import jsonify
from datetime import datetime

pacientes = []
#id,dni,nombre,apellido,telefono,email,direccion_calle,direccion_numero
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_csv_pacientes = os.path.join(directorio_actual, 'pacientes.csv')


def obtener_datos_pacientes(cantidad):
    url = f'https://randomuser.me/api/?results={cantidad}&nat=us&inc=dni,name,last,phone,email,id,location'
    response = requests.get(url)

    if response.status_code == 200:
        datos = response.json()['results']
        return datos 
    else:
        print('Error al obtener los datos de medicos')
        return None

def inicializado_datos_pacientes():
    global pacientes
    datos = obtener_datos_pacientes(40)

    if datos == None: #Si no se obtuvo de la API da error 
        return False 
    
    if verificador_ruta() == True:
        nueva_id = 1
        importar_desde_csv()
        if pacientes:
            return True
        else:
            for dato in datos: 
                id = nueva_id
                nueva_id += 1
                dni = dato["id"]["value"]
                dni = dni.replace(" ","")
                dni = dni.replace("-","")
                nombre = dato["name"]["first"]
                apellido = dato["name"]["last"]
                telefono = dato["phone"]
                email = dato["email"]
                direccion_calle = dato["location"]["street"]["name"]
                direccion_numero = dato["location"]["street"]["number"]

                nuevo_paciente = {"id":int(id),"dni":dni,"nombre":nombre,"apellido":apellido,"telefono":telefono,"email":email,"direccion_calle":direccion_calle,"direccion_numero":direccion_numero}
                pacientes.append(nuevo_paciente)
                exportar_a_csv()
            return True
    else:
        return None

def exportar_a_csv():
    global pacientes
    if verificador_ruta() == True:
        with open(ruta_csv_pacientes, 'w', newline='') as csvfile:
            campo_nombres = ['id','dni','nombre','apellido','telefono','email','direccion_calle','direccion_numero']
            writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
            writer.writeheader()
            for paciente in pacientes:
                writer.writerow(paciente)
    else: 
        return None

def importar_desde_csv():
    global pacientes 
    if verificador_ruta() == True:
        pacientes = []  # Limpiamos la lista de pacientes antes de importar desde el archivo CSV
        with open(ruta_csv_pacientes, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convertimos el ID de cadena a entero
                row['id'] = int(row['id'])
                pacientes.append(row) 
    else:
        return None
   
def verificador_ruta(): #verifica si la ruta es correcta
    if os.path.exists(ruta_csv_pacientes):
        return True
    else:
        print("no se encontro el archivo")
        return False

def obtener_lista_pacientes():
    global pacientes
    importar_desde_csv()
    if verificador_ruta() == True:
        return pacientes
    else: 
        return None

def obtener_paciente_xid(id):
    global pacientes
    if verificador_ruta() == True:
        for paciente in pacientes:
            if int(id) == int(paciente["id"]):
                return paciente 
        return 404
    else:
        return None
    
def agregar_paciente(nuevo_dni,nuevo_nombre,nuevo_apellido,nuevo_telefono,nuevo_email,nueva_direccion_calle,nueva_direccion_numero):
    global pacientes
    if verificador_ruta() == True:
        nueva_id = 1
        for paciente in pacientes:
            if nueva_id != int(paciente["id"]):
                break
            else: 
                nueva_id += 1
        pacientes.append({
            "id":nueva_id,
            "dni":nuevo_dni,
            "nombre":nuevo_nombre,
            "apellido":nuevo_apellido,
            "telefono":nuevo_telefono,
            "email":nuevo_email,
            "direccion_calle":nueva_direccion_calle,
            "direccion_numero":nueva_direccion_numero
        })
        exportar_a_csv()
        return True
    else:    
        return None

def actualizar_paciente_xid(id,nuevo_dni=None,nuevo_nombre=None,nuevo_apellido=None,nuevo_telefono=None,nuevo_email=None,nueva_direccion_calle=None,nueva_direccion_numero=None):
    global pacientes
    if verificador_ruta() == True:
        for paciente in pacientes:
            if int(paciente["id"]) == int(id):
                if not nuevo_dni == None:
                    paciente["dni"] = nuevo_dni
                if not nuevo_nombre == None:
                    paciente["nombre"] = nuevo_nombre
                if not nuevo_apellido == None:
                    paciente["apellido"] = nuevo_apellido
                if not nuevo_telefono == None:
                    paciente["telefono"] = nuevo_telefono 
                if not nuevo_email == None:
                    paciente["email"] = nuevo_email
                if not nueva_direccion_calle == None:
                    paciente["direccion_calle"] = nueva_direccion_calle
                if not nueva_direccion_numero == None:
                    paciente["direccion_numero"] = nueva_direccion_numero
                exportar_a_csv()
                return True
        return 404
    else:
        return None

def borrar_paciente_xid(id):
    global pacientes
    if verificador_ruta() == False:
        return None
    
    #tuve que importarlo aca porque si no me daba un error de importacion circular
    from modelos.turnos import obtener_lista_turnos

    turnos = obtener_lista_turnos()
    turnos_paciente_a_eliminar = []
    paciente_tiene_turno = False
    paciente_existe = False

    #busca si el id esta en la lista de pacientes
    #luego si la id del paciente tiene un turno
    #si tiene son agregados a una lista
    for paciente in pacientes:
        if int(paciente["id"]) == int(id):
            paciente_existe = True
            for turno in turnos:
                if int(turno["id_paciente"]) == int(id):
                    turnos_paciente_a_eliminar.append(turno)
                    paciente_tiene_turno = True

    #si no tiene es eliminado          
    #si tiene se analiza si puede ser eliminado          
    if paciente_existe == False:
        return 404
    if paciente_tiene_turno == False:
        for paciente in pacientes:
            if int(paciente["id"]) == int(id):
                pacientes.remove(paciente)
                exportar_a_csv()
                return True
    else:
        for turno in turnos_paciente_a_eliminar:
            fecha_turno = datetime.strptime(turno["fecha_solicitud"] + ' ' + turno["hora_turno"], '%d/%m/%Y %H:%M')
            fecha_actual = datetime.now()
            if fecha_actual < fecha_turno:
                return False
        for paciente in pacientes:
            if int(paciente["id"]) == int(id):
                pacientes.remove(paciente)
                exportar_a_csv()
                return True

    



