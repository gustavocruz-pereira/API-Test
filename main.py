from flask import Flask, make_response, jsonify, request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="banco_schema"
)

cursor = db.cursor()

def select_all():
    cursor.execute("SELECT * FROM carros")
    dados = cursor.fetchall()
    return dados

#CREATE
@app.route('/carros', methods=['POST'])
def create_carros():
    carro = request.json

    try:
        cursor.execute(
            f"INSERT INTO carros (carro_marca, carro_nome, carro_ano, carro_cor) VALUES (%s, %s, %s, %s)",
            (carro[0], carro[1], carro[2], carro[3])
        )
        
        db.commit()
        dados = select_all()
        cursor.close()
        return jsonify(dados)

    except Exception as e:
        print("Ocorreu um erro: ", e)
        return jsonify({"mensagem":"Ocorreu um erro durante a inserção dos dados"})
    
    

#READ
@app.route('/carros', methods=['GET'])
def get_carros():
    dados = select_all()
    cursor.close()
    return jsonify(dados)

#DELETE
@app.route('/carros/<int:id>', methods=['DELETE'])
def delete_carros(id):
    try:
        cursor.execute(
            "DELETE FROM carros WHERE carro_id = %s", (id,)
        )
        db.commit()

        return jsonify({"mensagem ": f"ID {id} deletado com sucesso"})

    except Exception as e:
        return jsonify({"mensagem" : f"Ocorreu um erro: {e}"})

#UPDATE
@app.route('/carros/update', methods=['UPDATE'])
def update_carros():
    pass



if __name__ == '__main__':
    app.run()

