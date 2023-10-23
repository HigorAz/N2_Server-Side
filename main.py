# libs que iremos utilizar neste projeto
import heapq
import json
import time
import ujson #Biblioteca "estilziada" para trabalhar com dados em JSON

from flask import Flask, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # conexao com o banco de dados
app.config['SECRET_KEY'] = "random string" # para criptografar as sessões
# desde que você tem as classes relaciandas ao banco, o ORM faz o processo de criar, recuperar e converter
db = SQLAlchemy(app)


@app.route('/')
def indice():
    return render_template('index.html')


def sort(vetor):
    x = sorted(vetor)
    return x


@app.route('/ordenacao', methods=['GET', 'POST'])
def ordena():
    resultado = ""
    if request.method == 'POST':
        vetor_ordenacao = request.form["vetor"]
        if not vetor_ordenacao:
            flash("Nada digitado!", "Error")
        else:
            vetor = list(map(int, vetor_ordenacao.split(",")))
            inicio = time.time()
            ordenado = sort(vetor)
            fim = time.time()

            retorno = ujson.dumps(ordenado)
            tempo_total = ((fim - inicio) * 1000)
            flash(f"Tempo: {tempo_total}\n{retorno}", "Sucesso")
            resultado = str(tempo_total) + '  ' + retorno
    return render_template('ordena.html', resultado = resultado)


class Users(db.Model):
    # definição dos tipos de dados do banco
    id = db.Column('user_id', db.Integer, primary_key = True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.Integer)
    observacao = db.Column(db.String(100))

    # objeto
    def __init__(self, nome, email, telefone, observacao):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.observacao = observacao

    def to_dict(self):
        return {
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'observacao': self.observacao
        }


# lista todos os usuarios
@app.route('/consulta')
def consulta():

    # for x in range(10000):
    #     user = Users("nome " + str(x), "email " + str(x), "tel " + str(x), "obs " + str(x))
    #     db.session.add(user)  # salva no banco
    # db.session.commit() # commit da operação

    inicio = time.time()

    user = Users.query.all()
    user_to_dict = []
    for u in user:
        user_to_dict.append(u.to_dict())
    aux = ujson.dumps(user_to_dict)

    fim = time.time()

    tempo_total = ((fim-inicio)*1000)

    return str(tempo_total) + '   ' + aux


# Função Dijkstra para encontrar menor caminho no grafo
def dijkstra(grafo, begin):
    distance = {v: float('infinity') for v in grafo}
    distance[begin] = 0
    pq = [(0, begin)]

    while len(pq) > 0:
        current_distance, current_vertex = heapq.heappop(pq)
        if current_distance > distance[current_vertex]:
            continue
        for neighbor, weight in grafo[current_vertex].items():
            dist = current_distance + weight
            if dist < distance[neighbor]:
                distance[neighbor] = dist
                heapq.heappush(pq, (dist, neighbor))

    return distance

#Exemplo de grafo:
#{"A": {"B": 5, "C": 3, "D": 2}, "B": {"A": 5, "C": 2, "E": 4}, "C": {"A": 3, "B": 2, "D": 1}, "D": {"A": 2, "C": 1, "E": 7}, "E": {"B": 4, "D": 7}}
@app.route('/grafo', methods=['GET', 'POST'])
def grafo():
    resultado = ""
    if request.method == 'POST':
        grafo_input = request.form["grafo"]
        if not grafo_input:
            flash("Nada digitado!", "Error")
        else:
            grafo = ujson.loads(grafo_input)
            inicio = time.time()
            menorCaminho = dijkstra(grafo, "A")
            fim = time.time()

            retorno = ujson.dumps(menorCaminho)
            tempo_total = ((fim - inicio) * 1000)
            flash(f"Tempo: {tempo_total}\n{retorno}", "Sucesso")
            resultado = str(tempo_total) + '  ' + retorno
    return render_template('grafo.html', resultado=resultado)

if __name__ == '__main__':
    app.app_context().push()  # recupera o contexto da aplicação que está usando o banco
    db.create_all()  # cria todas as instâncias da database se não existirem
    app.run(host="0.0.0.0", port="5000", debug=True)