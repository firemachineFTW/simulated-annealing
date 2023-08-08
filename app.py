from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
#TSP con templado simulado
import math, random

app = Flask(__name__)
CORS(app)

def distancia(coord1, coord2):
    lat1=coord1[0]
    lon1=coord1[1]
    lat2=coord2[0]
    lon2=coord2[1]
    return math.sqrt((lat1-lat2)**2 + (lon1-lon2)**2)

#Calcula la distancia cubierta por una ruta
def evalua_ruta(ruta):
    total = 0
    for i in range(0, len(ruta)-1):
        ciudad1 = ruta[i]
        ciudad2 = ruta[i + 1]
        total = total + distancia(coord[ciudad1], coord[ciudad2])
    ciudad1 = ruta[i + 1]
    ciudad2 = ruta[0]
    total = total + distancia(coord[ciudad1], coord[ciudad2])
    return total

def simulated_annealing(ruta):
    T = 20
    T_MIN = 0
    V_enfriamineto = 100

    while T > T_MIN:
        dist_actual = evalua_ruta(ruta)
        for i in range(1, V_enfriamineto):
            #intercambio de dos ciudades aleatoriamente
            i = random.randint(0, len(ruta) - 1)
            j = random.randint(0, len(ruta) - 1)
            ruta_tmp = ruta[:]
            ciudad_tmp = ruta_tmp[i]
            ruta_tmp[i] = ruta_tmp[j]
            ruta_tmp[j] = ciudad_tmp
            dist = evalua_ruta(ruta_tmp)
            delta = dist_actual - dist
            if(dist < dist_actual):
                ruta = ruta_tmp[:]
                break
            elif random.random() < math.exp(delta/T):
                ruta = ruta_tmp[:]
                break
        #enfriar a T linealmente
        T = T - 0.005

    return ruta
  
#crear una ruta inicial aleatoria


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/templado_simulado", methods=['GET', 'POST'])
def calcular_simulated_annealing():
    data = request.get_json()
    coord = data["coord"]

    ruta = []
    for ciudad in coord:
        ruta.append(ciudad)
        random.shuffle(ruta)
    
    ruta = simulated_annealing(ruta)

    templado_simulado = simulated_annealing(ruta)

    return jsonify(templado_simulado) 



if __name__ == "__main__":
    app.run(debug = True)