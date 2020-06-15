import sys

from flask import Flask,abort,render_template,Response,request,jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


estacionesTabla = {
    # idEstacion : [Nombre, Descr, Lat, Long, BtAddr]
    204 : ["Estacion Barrio Parque","Estacion barrial situada en la casa de Bruno Perez", -31.433727, -64.213417, "bluetoohaddre"],
    870 : ["Estación Buen Pastor" , "Estacion en el corazón de nueva cordoba",-31.423703, -64.186863 , "bt addre"]
}

userTabla = {
    # idUser : [nombre, mail ,passwd, saldo]
    500 : ["Bruno Perez", "bruno178pm@gmail.com" ,"abc123", 150],
    600 : ["Lucas Pardina", "lucaspardina@gmail.com" ,"123abc", 150]
}

slotsTabla = {
    # idSlot : [idEstacion, userId, posicion]
    1 : [204, 500, 0],
    2 : [204, None, 1],
    3 : [204, 600, 2],
    4 : [870, None, 0],
    5 : [870, None, 1],
    6 : [870, None, 2]
}


@app.route("/app/estaciones",methods=['GET'])
def estaciones():
    return render_template("alumnos.html", estaciones = estacionesTabla)

@app.route("/app/slots",methods=['GET'])
def slots():
    slotsLista = []
    for slot in slotsTabla.values():
        usuarioUsandolo = "Ninguno"
        if (slot[1] != None):
            usuarioUsandolo = userTabla[slot[1]][0]
        slotsLista.append([estacionesTabla[slot[0]][0], usuarioUsandolo, slot[2]])
    return render_template("slots.html", slotsList = slotsLista)

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


@app.route("/unlock",methods=['POST'])
def unlock():
    if (request.is_json):
        userId = (request.get_json()["userId"])
        slotId = (request.get_json()["slotId"])
        if (userId in userTabla and slotId in slotsTabla):
            if (userTabla[userId][3] > 0):
                if (slotsTabla[slotId][1] == None):
                    slotsTabla[slotId][1] = userId
                    return "ok"
                else:
                    return "Slot ya ocupado"
            else:
                return "Saldo insuficiente."
        else:
            return "Usuario o bicicleta inexistente."
    else:
        abort(500, "No se envio un objeto json")


@app.route("/estaciones",methods=['GET'])
def getEstaciones():
    lista_estaciones = []
    for estacionId in estacionesTabla:
        item = estacionesTabla[estacionId]
        lista_estaciones.append({"idEstacion":estacionId,"nombre":item[0],"lat":item[2],"lon":item[3], "btAddress" : item[4]})
    return jsonify(lista_estaciones)

@app.route("/estaciones/<int:estacionId>/slots",methods=['GET'])
def getSlotsByEstacion(estacionId):
    lista_slots = []
    for slotId in slotsTabla:
        item = slotsTabla[slotId]
        if (item[0] == estacionId):
            estaOcupado = True
            if (item[1] == None):
                estaOcupado = False
            lista_slots.append({"slotId" : slotId, "estaOcupado" : estaOcupado, "posicion" : item[2]})
    return jsonify(lista_slots)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
