import csv
import requests
import os
from flask import jsonify

medicos = []
#id,dni,nombre,apellido,matricula,telefono,email,habilitado
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_csv_medicos = os.path.join(directorio_actual, 'medicos.csv')


def obtener_datos_medicos(cantidad):
    url = f'https://randomuser.me/api/?results={cantidad}&nat=us&inc=dni,name,last,phone,email,id,login'
    response = requests.get(url)
    #agarra la url, le pide los datos del final y los pasa a una variables comun
    if response.status_code == 200:
        datos = response.json()['results']
        return datos 
    else:
        print('Error al obtener los datos de medicos')
        return None

def inicializado_datos_medicos():
    global medicos
    datos = obtener_datos_medicos(10)

    if datos == None: #Si no se obtuvo de la API da error 
        return False 
    
    if verificador_ruta() == True:
        nueva_id = 1
        importar_desde_csv()
        if medicos:
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
                matricula = dato["login"]["password"]
                telefono = dato["phone"]
                email = dato["email"]

                nuevo_medico = {"id":int(id),"dni":dni,"nombre":nombre,"apellido":apellido,"matricula":matricula,"telefono":telefono,"email":email,"habilitado":True}
                medicos.append(nuevo_medico)
                exportar_a_csv()
            return True
    else:
        return None

def exportar_a_csv():
    global medicos
    #reescribe el archivo
    if verificador_ruta() == True:
        with open(ruta_csv_medicos, 'w', newline='') as csvfile:
            campo_nombres = ['id','dni','nombre','apellido','matricula','telefono','email','habilitado']
            writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
            writer.writeheader()
            for medico in medicos:
                writer.writerow(medico)
    else: 
        return None

def importar_desde_csv():
    global medicos 
    if verificador_ruta() == True:
        medicos = []  # Limpiamos la lista de medicos antes de importar desde el archivo CSV
        with open(ruta_csv_medicos, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convertimos el ID de cadena a entero
                row['id'] = int(row['id'])
                medicos.append(row) 
    else:
        return None
    
def verificador_ruta(): #verifica si la ruta es correcta
    if os.path.exists(ruta_csv_medicos):
        return True
    else:
        print("no se encontro el archivo")
        return False

def obtener_lista_medicos():#GET
    global medicos
    if verificador_ruta() == True:
        return medicos
    else: 
        return None

def obtener_medico_xid(id):#GET
    global medicos
    if verificador_ruta() == True:
        for medico in medicos:
            if int(id) == int(medico["id"]):
                return medico 
        return 404
    else:
        return None
    
def agregar_medico(nuevo_dni,nuevo_nombre,nuevo_apellido,nueva_matricula,nuevo_telefono,nuevo_email):#POST
    global medicos
    if verificador_ruta() == True:
        nueva_id = 1
        for medico in medicos:
            if nueva_id != int(medico["id"]):
                break
            else: 
                nueva_id += 1
        medicos.append({
            "id":nueva_id,
            "dni":nuevo_dni,
            "nombre":nuevo_nombre,
            "apellido":nuevo_apellido,
            "matricula":nueva_matricula,
            "telefono":nuevo_telefono,
            "email":nuevo_email,
            "habilitado":True
        })
        exportar_a_csv()
        return True
    else:    
        return None

def actualizar_medico_xid(id,nuevo_dni=None,nuevo_nombre=None,nuevo_apellido=None,nueva_matricula=None,nuevo_telefono=None,nuevo_email=None): #PUT
    global medicos
    if verificador_ruta() == True:
        for medico in medicos:
            if int(medico["id"]) == int(id):
                if not nuevo_dni == None:
                    medico["dni"] = nuevo_dni
                if not nuevo_nombre == None:
                    medico["nombre"] = nuevo_nombre
                if not nuevo_apellido == None:
                    medico["apellido"] = nuevo_apellido
                if not nueva_matricula == None:
                    medico["matricula"] = nueva_matricula
                if not nuevo_telefono == None:
                    medico["telefono"] = nuevo_telefono 
                if not nuevo_email == None:
                    medico["email"] = nuevo_email
                exportar_a_csv()
                return True
        return 404
    else:
        return None
    
def habilitacion_medico_xid(id,habilitacion):#PUT
    global medicos
    if verificador_ruta() == True:
        for medico in medicos:
            #si coinciden las id se fija que fue mandado para habilitar o deshabilitar
            if int(medico["id"]) == int(id):
                if habilitacion == True:
                    medico["habilitado"] = habilitacion
                    exportar_a_csv()
                    return True
                else:
                    medico["habilitado"] = habilitacion
                    exportar_a_csv()
                    return False
        return 404
    else:
        return None
 
def id_medicos_horarios():
    #esta funcion es usada en el archivo de agenda_medicos.py
    #para poder ver que id de medicos estan disponibles para crear los horarios
    if verificador_ruta() == True:
        importar_desde_csv()
        lista_ids = []
        for ids in medicos:
            lista_ids.append(ids["id"])
        return lista_ids
    else:
        return None

    

#id,dni,nombre,apellido,matricula,telefono,email,habilitado



