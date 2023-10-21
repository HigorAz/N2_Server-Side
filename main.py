# libs que iremos utilizar neste projeto
import json
import time

from flask import Flask, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # conexao com o banco de dados
app.config['SECRET_KEY'] = "random string" # para criptografar as sessões

# desde que você tem as classes relaciandas ao banco, o ORM faz o processo de criar, recuperar e converter
db = SQLAlchemy(app)
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

@app.route('/')
def indice():
    return render_template('index.html')

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
    aux = json.dumps(user_to_dict)

    fim = time.time()

    tempo_total = ((fim-inicio)*1000)

    return str(tempo_total) + '   ' + aux


# def vector():
#     if request.method == 'POST':
#         vetor_str = request.form['vet_to']
#
#         return json.dumps (retorno)
#
#     grafo = json.loads(grafo-str)
#
#     string, converter para json, chamar o algoritmo de texto

if __name__ == '__main__':
    app.app_context().push()  # recupera o contexto da aplicação que está usando o banco
    db.create_all()  # cria todas as instâncias da database se não existirem
    app.run(host="0.0.0.0", port="5000", debug=True)