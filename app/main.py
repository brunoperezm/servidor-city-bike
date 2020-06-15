import sys

from flask import Flask,abort,render_template,Response,request

app = Flask(__name__)

alumnosDb = {
    1 : "Jere Benitez",
    2 : "Brunito pe"
}


@app.route("/alumnos",methods=['GET'])
def getAllAlumnos():
    return render_template("alumnos.html", alumnos = alumnosDb)

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
