import sys

from flask import Flask,abort,render_template,Response,request

app = Flask(__name__)

estacionesTabla = {
    # idEstacion : [Nombre, Descr, Lat, Long]
    204 : ["Estacion Barrio Parque","Estacion barrial situada en la casa de Bruno Perez", -31.433727, -64.213417],
    870 : ["Estación Buen Pastor" , "Estacion en el corazón de nueva cordoba",-31.423703, -64.186863 ]
}

userTabla = {
    # idUser : [nombre, mail ,passwd]
    500 : ["Bruno Perez", "bruno178pm@gmail.com" ,"abc123"],
    600 : ["Lucas Pardina", "lucaspardina@gmail.com" ,"123abc"]
}

slotsTabla = {
    # idSlot : [idEstacion, userId]
    1 : [204, 500],
    2 : [204, None],
    3 : [204, 600],
    4 : [870, None],
    5 : [870, None],
    6 : [870, None]
}


@app.route("/estaciones",methods=['GET'])
def getAllAlumnos():
    return render_template("alumnos.html", estaciones = estacionesTabla)

@app.route("/login",methods=['POST'])
def login():
    if (request.is_json): 
        email = str(request.get_json()["email"])
        password = str(request.get_json()["password"])

        for user in userTabla.values():
            if (user[1] == email and user[2] == password):
                return "ok"
            else:
                return "Credenciales inválidas."
        return email      
    
    else:
        abort(500, "No se envio un objeto json")



@app.route("/alumnos",methods=['POST'])
def saveAlumno():
    if (request.is_json): 
        id = (request.get_json()["id"])
        nombre = str(request.get_json()["nombre"])
        alumnosDb[id] = nombre
        return "Se insertó un elemento."
    else:
        abort(500, "No se envio un objeto json")

@app.route("/alumnos/<int:id>",methods=['DELETE'])
def deleteAlumno(id):
    if (id in alumnosDb):
        alumnosDb.pop(id)
        return "Se borro el elemento " + str(id) 
    else:
        abort(500,"No existe id a borrar")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
