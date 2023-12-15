from flask import Flask
from modelos.medicos import inicializado_datos_medicos
from modelos.medicos import importar_desde_csv as importar_csv_medicos
from controladores.rutas_medicos import medicos_blueprint
from modelos.pacientes import inicializado_datos_pacientes
from modelos.pacientes import importar_desde_csv as importar_csv_pacientes
from controladores.rutas_pacientes import pacientes_blueprint
from modelos.agenda_medicos import asignacion_horarios_medicos
from modelos.agenda_medicos import importar_desde_csv as importar_csv_agenda
from controladores.rutas_agenda_medicos import agenda_medicos_blueprint
from modelos.turnos import asignacion_turnos
from modelos.turnos import importar_desde_csv as importar_csv_turnos
from controladores.rutas_turnos import turnos_blueprint

app = Flask(__name__) #creamos una instancia de la clase Flask

# registramos el blueprint

app.register_blueprint(medicos_blueprint)
app.register_blueprint(pacientes_blueprint)
app.register_blueprint(agenda_medicos_blueprint)
app.register_blueprint(turnos_blueprint)


inicializado_datos_medicos()
importar_csv_medicos()

inicializado_datos_pacientes()
importar_csv_pacientes()

asignacion_horarios_medicos()
importar_csv_agenda()

asignacion_turnos()
importar_csv_turnos()

if __name__ == '__main__':
    app.run(debug=True) #iniciamos la aplicación