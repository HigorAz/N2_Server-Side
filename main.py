# libs que iremos utilizar neste projeto
import heapq
import json
import time
import ujson #Biblioteca "estilziada" para trabalhar com dados em JSON

from flask import Flask, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates') # integra a pasta dos templates, torna a rota padrão
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # conexao com o banco de dados
app.config['SECRET_KEY'] = "random string" # para criptografar as sessões
# desde que você tem as classes relaciandas ao banco, o ORM faz o processo de criar, recuperar e converter
db = SQLAlchemy(app)

# abre a rota do indice na rota padrão, que direcionará as funções criadas
@app.route('/')
def indice():
    return render_template('index.html') #retorna o template criado para o index em html, que contém os redirecionamentos

#Função para ordenação utilizada, ordenação padrão do Python, que utiliza o método TimSort
def sort(vetor):
    x = sorted(vetor) #auxiliar x recebe o valor ordenado do vetor
    return x #Retorna o valor ordenado

#Rota para o problema de ordenação
@app.route('/ordenacao', methods=['GET', 'POST'])
def ordena():
    resultado = "" #Resultado recebe um valor sem valor para que consiga receber o valor do if e retornar fora do if
    if request.method == 'POST': #Verifica se recebeu um valor no form do html.
        vetor_ordenacao = request.form["vetor"] #Entrada de dados do formulário em html
        if not vetor_ordenacao: #Se não recebeu, retorna erro
            flash("Nada digitado!", "Error")
        else: #Se receber, entra no algoritmo:
            vetor = list(map(int, vetor_ordenacao.split(","))) #Faz a separação do vetor pelo delimitador ","
            inicio = time.time() #Inicia o tempo do cronômetro da função time
            ordenado = sort(vetor) #Utiliza a função sort declarada anteriormente para ordenar o vetor digitado
            fim = time.time() #Finaliza o temporizador da função time

            retorno = ujson.dumps(ordenado) #Transforma o valor do vetor ordenado em json
            tempo_total = ((fim - inicio) * 1000) #Calcula o tempo do temporizador inciado e finalizado
            flash(f"Tempo: {tempo_total}\n{retorno}", "Sucesso") # retorna mensagem de sucesso
            resultado = str(tempo_total) + '  ' + retorno #Concatena o resultado a ser apresentado no return
    return render_template('ordena.html', resultado = resultado) #Retorna o template em html de ordenação e o resultado declarado anteriormente


class Users(db.Model): #Declara classe do banco de dados
    # definição dos tipos de dados do banco
    id = db.Column('user_id', db.Integer, primary_key = True) #Coluna de id como chave primária e inteiro
    nome = db.Column(db.String(100)) #Coluna de nome como string de 100 caracteres
    email = db.Column(db.String(100)) #Coluna de email como string de 100 caracteres
    telefone = db.Column(db.Integer) #Coluna de telefone como inteiro
    observacao = db.Column(db.String(100)) #Coluna de observação como string de 100 caracteres

    # Construtor que chama a classe
    def __init__(self, nome, email, telefone, observacao):
        self.nome = nome #atribui o valor de nome para o atributo nome instanciado
        self.email = email #atribui o valor de email para o atributo email instanciado
        self.telefone = telefone #atribui o valor de telefone para o atributo telefone instanciado
        self.observacao = observacao #atribui o valor de observacao para o atributo observacao instanciado

    def to_dict(self): # função to_dict para transformar os valores recebidos anteriormente em json
        return {
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'observacao': self.observacao
        }


# Rota para consultar os usuários
@app.route('/consulta')
def consulta():
    # for x in range(10000): #Laço de repetição para a criação de 10000 usuários
    #     user = Users("nome " + str(x), "email " + str(x), "tel " + str(x), "obs " + str(x)) # define o usuários com nome, email, telefone e observação
    #     db.session.add(user)  # salva no banco
    # db.session.commit() # commit da operação

    inicio = time.time() #Inicia o temporizador

    user = Users.query.all() #Consulta e armazena os registros com SQLAlchemy
    user_to_dict = [] #Inicia a lista vazia
    for u in user: #Laço de repetição para transformar os usuários em json
        user_to_dict.append(u.to_dict()) #Utiliza o to_dict para transformar os dados em json
    aux = ujson.dumps(user_to_dict) #Converte a lista to_dict anterior em json

    fim = time.time() #Finaliza o temporizador

    tempo_total = ((fim-inicio)*1000) #Calcula o tempo total cronometrado
    resultado = str(tempo_total) + '   ' + aux #Retorna o tempo total em string e o valor auxiliar em json
    return render_template('crud.html', resultado=resultado) #Retorna o template em html com o resultado armazenado


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

#Rota para a resolução do grafo
@app.route('/grafo', methods=['GET', 'POST'])
def grafo():
    resultado = "" #Resultado recebe um valor sem valor para que consiga receber o valor do if e retornar fora do if
    if request.method == 'POST': #Verifica se recebeu um valor no form do html.
        grafo_input = request.form["grafo"] #Entrada de dados através do formulário html
        if not grafo_input: #Se não recebeu, retorna erro
            flash("Nada digitado!", "Error")
        else: #Se receber, entra no algoritmo:
            grafo = ujson.loads(grafo_input) #Função para armazenar a string em json recebida em grafo_input e converter em uma estrutura python
            inicio = time.time() # Inicia o cronometro
            menorCaminho = dijkstra(grafo, "A") #Identifica o menor caminho utilizando a função de dijkstra utilizando o ponto A como start
            fim = time.time() # Finaliza o cronometro

            retorno = ujson.dumps(menorCaminho) # Converte e retorna o valor de menor caminho em json
            tempo_total = ((fim - inicio) * 1000) #Calcula o tempo total do cronometro
            flash(f"Tempo: {tempo_total}\n{retorno}", "Sucesso") #Retorno de mensagem de sucesso
            resultado = str(tempo_total) + '  ' + retorno #Armazena o resultado do tempo total e do retorno em json do menor caminho
    return render_template('grafo.html', resultado=resultado) #Retorna o template em html com o resultado armazenado anteriormente

if __name__ == '__main__':
    app.app_context().push()  # recupera o contexto da aplicação que está usando o banco
    db.create_all()  # cria todas as instâncias da database se não existirem
    app.run(host="0.0.0.0", port="5000", debug=True)