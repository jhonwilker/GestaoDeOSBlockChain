# pip install --user flask sqlalchemy flask-sqlalchemy
#ESTRUTURA
# blockchain_app/
#   templates/ 
#       -home.html
#   ar_manager.py
# 
#Depois que instalar o flask e copiar o projeto
#cmd > python
#>> from ar_manager import db
#>> db.create_all()
#>> exit()
import os
import sys
import mcrpc
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

import json
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "arosdatabase.db"))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
#comandos

#multichain-util create sysod
#multichaind sysod -daemon
#multichain-cli sysod getinfo
#multichain-cli sysod create stream ordemservicos "{\"restrict\":\"write\"}"
#inserção terminal do windows #multichain-cli sysod publish ordemservicos ordens "{\"json\":{\"tecnico\":\"Marcos Andre\",\"equipamento\":\"arCondicionado\",\"idEquipamento\":\"01844\",\"descricaoOS\":\"foi feito somente a reabastecimenteo de gas\"}}"
#multichain-cli sysod subscribe ordemservicos                
#multichain-cli sysod liststreamkeyitems ordemservicos ordens

#------------------------------BLOCKCHAIN-------------------------------------
c = mcrpc.RpcClient('127.0.0.1','2918','multichainrpc','FNnDkkYTuD6b5z31n6K5ChkamwMZHKcRcCqrQCT2yeeC')

def informacaoBlockChain():#retorna ultima
    return c.getblockchaininfo()
#inserção via cliente.py
@app.route('/update_os', methods=['POST', 'GET'])

def publishBlockchain(tecnico,equipamento,idEquipamento,descricaoOS):
    obj={
    "tecnico":tecnico,
    "equipamento":equipamento,
    "idEquipamento":idEquipamento,
    "descricaoOS":descricaoOS
    }
    return c.publish('ordemservicos','ordens',{"json":obj}), redirect("/")

def informacoesPublicacoes():#retorna ultima
    return c.liststreamkeyitems("ordemservicos","ordens")

#a=informacoesPublicacoes
#print(informacoesPublicacoes())
#print(publishBlockchain("Jhon","arcondicionado","1123456","feita limpeza"))

#-----------------------------------------------------------------------------
class Os(db.Model):
    tecnico = db.Column(db.String(100),nullable=False)
    equipamento = db.Column(db.String(100),nullable=False)
    idEquipamento = db.Column(db.Integer, primary_key=True)
    descricaoOS = db.Column(db.String(100),nullable=False)

    def __init__(self, tecnico, equipamento, idEquipamento, descricaoOS):
        self.tecnico = tecnico
        self.equipamento = equipamento
        self.idEquipamento = idEquipamento
        self.descricaoOS = descricaoOS

    


@app.route("/", methods=["GET", "POST"])
def home():
 
    addresses = None
    if request.form:
        try:
            if request.method == 'POST':
                address = Os(tecnico=request.form.get("tecnico"),equipamento=request.form.get("equipamento"), idEquipamento=request.form.get("idEquipamento"), descricaoOS=request.form.get("descricaoOS"))
                publishBlockchain(address.tecnico, address.equipamento,address.idEquipamento,address.descricaoOS )
                print("passou pelo POST")
        except Exception as e:
            print("Failed to add OS")
            print(e)
    addresses = Os.query.all()
    return render_template("home.html",addresses = addresses )

@app.route("/ordens", methods=["GET", "POST"])
def ordens():
    resultado = None
    if request.form:
        try:
            if request.method == 'GET':
                resultado=informacoesPublicacoes()
                print("passou pelo GET")
        except Exception as e:
            resultado="ZERO"
            print("Failed to add OS")
            print(e)
    resultado = Os.query.all()
    #return render_template("ordens.html",resultado = resultado )
    return jsonify(informacoesPublicacoes())

if __name__ == "__main__":
    app.run(debug=True)
