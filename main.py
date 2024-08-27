import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import sqlalchemy
import os
from dotenv import load_dotenv, dotenv_values


load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": ""}})

db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_DATABASE')
}




def insert_drawer(nome, descricao, estado, rack_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "INSERT INTO Gaveta (nome, descricao, estado, Rack_idRack) VALUES (%s, %s, %s, %s)"
        values = (nome, descricao, estado, rack_id)
        cursor.execute(query, values)
        connection.commit()
        return True
    except Exception as e:
        print('Error inserting drawer information:', str(e))
        return False
    finally:
        cursor.close()
        connection.close()

@app.route('/')
def hello():
    return jsonify({'message': 'Welcome to the API'})

def insert_rack(nome, localizacao, descricao):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "INSERT INTO Rack (nome, localizacao, descricao) VALUES (%s, %s, %s)"
        values = (nome, localizacao, descricao)
        cursor.execute(query, values)
        connection.commit()
        rack_id = cursor.lastrowid  # Obtém o ID do Rack recém-inserido
        return rack_id
    except Exception as e:
        print('Error inserting rack information:', str(e))
        return None
    finally:
        cursor.close()
        connection.close()

@app.route('/add_rack', methods=['POST'])
def add_rack():
    data = request.get_json()
    if 'nome' in data and 'localizacao' in data and 'descricao' in data:
        nome = data['nome']
        localizacao = data['localizacao']
        descricao = data['descricao']
        rack_id = insert_rack(nome, localizacao, descricao)
        if rack_id is not None:
            gaveta_data = data.get('gavetas', [])
            for gaveta in gaveta_data:
                if 'nome' in gaveta and 'descricao' in gaveta and 'estado' in gaveta:
                    gaveta_nome = gaveta['nome']
                    gaveta_descricao = gaveta['descricao']
                    gaveta_estado = gaveta['estado']
                    if insert_drawer(gaveta_nome, gaveta_descricao, gaveta_estado, rack_id):
                        print(f"Gaveta inserida com sucesso para o Rack ID {rack_id}")
                    else:
                        print("Falha ao inserir a gaveta.")
            return jsonify({'message': 'Rack e gavetas associadas inseridos com sucesso'}), 201
        else:
            return jsonify({'message': 'Failed to add the rack'}), 500
    else:
        return jsonify({'message': 'Invalid data'}), 400

@app.route('/add_drawer', methods=['POST'])
def add_drawer():
    data = request.get_json()
    if 'nome' in data and 'descricao' in data and 'estado' in data and 'Rack_idRack' in data:
        nome = data['nome']
        descricao = data['descricao']
        estado = data['estado']
        rack_id = data['Rack_idRack']
        if insert_drawer(nome, descricao, estado, rack_id):
            return jsonify({'message': 'Drawer added successfully'}), 201
        else:
            return jsonify({'message': 'Failed to add the drawer'}), 500
    else:
        return jsonify({'message': 'Invalid data'}), 400


@app.route('/update_gaveta/<int:gaveta_id>', methods=['PUT'])
def update_gaveta(gaveta_id):
    data = request.get_json()
    if 'nome' in data and 'descricao' in data and 'estado' in data:
        updated_name = data['nome']
        updated_description = data['descricao']
        updated_estado = data['estado']
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            # Buscar o estado atual da gaveta
            cursor.execute("SELECT estado FROM Gaveta WHERE idGaveta = %s", (gaveta_id,))
            current_state = cursor.fetchone()
            if current_state:
                estado_anterior = current_state[0]
            else:
                return jsonify({'message': 'Gaveta não encontrada'}), 404

            # Verificar se a gaveta está sendo selecionada
            if updated_estado == 'Selecionado':
                # Verificar se já existe uma gaveta selecionada para o mesmo rack
                cursor.execute("SELECT idGaveta FROM Gaveta WHERE estado = 'Selecionado' AND Rack_idRack IN (SELECT Rack_idRack FROM Gaveta WHERE idGaveta = %s)", (gaveta_id,))
                selected_gaveta = cursor.fetchone()
                if selected_gaveta and selected_gaveta[0] != gaveta_id:
                    return jsonify({'message': 'Já existe uma gaveta selecionada para o mesmo rack'}), 400

            # Atualizar a gaveta
            query_gaveta = "UPDATE Gaveta SET nome = %s, descricao = %s, estado = %s WHERE idGaveta = %s"
            values_gaveta = (updated_name, updated_description, updated_estado, gaveta_id)
            cursor.execute(query_gaveta, values_gaveta)

            # Verificar se houve mudança na cor ou observação
            cor_atual = request.args.get('cor')
            observacao_atual = request.args.get('observacao')

            if cor_atual != updated_estado or observacao_atual != updated_estado:
                # Criar um novo registro na tabela Registro
                query_registro = "INSERT INTO Registro (data, hora, cor, observacao, Gaveta_idGaveta) VALUES (CURDATE(), CURTIME(), %s, %s, %s)"
                values_registro = (updated_estado, updated_description, gaveta_id)
                cursor.execute(query_registro, values_registro)

            connection.commit()
            return jsonify({'message': 'Gaveta atualizada com sucesso', 'estado_anterior': estado_anterior}), 200
        except Exception as e:
            print('Erro ao atualizar a gaveta:', str(e))
            return jsonify({'message': 'Falha ao atualizar a gaveta'}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({'message': 'Dados inválidos'}), 400




@app.route('/rack_details/<int:rack_id>', methods=['GET'])
def rack_details(rack_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Rack WHERE idRack = %s"
        cursor.execute(query, (rack_id,))
        rack = cursor.fetchone()
        if rack:
            return jsonify({'rack': rack}), 200
        else:
            return jsonify({'message': 'Rack not found'}), 404
    except Exception as e:
        print('Error fetching rack details:', str(e))
        return jsonify({'message': 'Failed to fetch rack details'}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_gaveta/<int:gaveta_id>', methods=['DELETE'])
def delete_gaveta(gaveta_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT idGaveta FROM Gaveta WHERE idGaveta = %s", (gaveta_id,))
        result = cursor.fetchone()
        if result is None:
            return jsonify({'message': 'Gaveta not found'}), 404
        cursor.execute("DELETE FROM Gaveta WHERE idGaveta = %s", (gaveta_id,))
        connection.commit()
        return jsonify({'message': 'Gaveta deleted successfully'}), 200
    except Exception as e:
        print('Error deleting gaveta:', str(e))
        return jsonify({'message': 'Failed to delete the gaveta'}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_rack/<int:rack_id>', methods=['DELETE'])
def delete_rack(rack_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Registro WHERE Gaveta_idGaveta IN (SELECT idGaveta FROM Gaveta WHERE Rack_idRack = %s)", (rack_id,))
        cursor.execute("DELETE FROM Gaveta WHERE Rack_idRack = %s", (rack_id,))
        cursor.execute("DELETE FROM Rack WHERE idRack = %s", (rack_id,))
        connection.commit()
        return jsonify({'message': 'Rack and associated gavetas and registros deleted successfully'}), 200
    except Exception as e:
        print('Error deleting rack:', str(e))
        return jsonify({'message': 'Failed to delete the rack'}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_gaveta', methods=['GET'])
def get_gavetas():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Gaveta"
        cursor.execute(query)
        gavetas = cursor.fetchall()
        return jsonify({'data': gavetas}), 200
    except Exception as e:
        print('Error fetching gavetas:', str(e))
        return jsonify({'message': 'Failed to fetch gavetas'}), 500
    finally:
        cursor.close()
        connection.close()




@app.route('/get_gavetas_por_rack/<int:rack_id>', methods=['GET'])
def get_gavetas_por_rack(rack_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT G.* FROM Gaveta G INNER JOIN Rack R ON G.Rack_idRack = R.idRack WHERE R.idRack = %s"
        cursor.execute(query, (rack_id,))
        gavetas = cursor.fetchall()
        return jsonify({'data': gavetas}), 200
    except Exception as e:
        print('Error fetching gavetas:', str(e))
        return jsonify({'message': 'Failed to fetch gavetas'}), 500
    finally:
        cursor.close()
        connection.close()







@app.route('/get_racks', methods=['GET'])
def get_racks():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT idRack, nome, localizacao, descricao FROM Rack"
        cursor.execute(query)
        racks = cursor.fetchall()
        return jsonify({'data': racks}), 200
    except Exception as e:
        print('Error fetching racks:', str(e))
        return jsonify({'message': 'Failed to fetch racks'}), 500
    finally:
        cursor.close()
        connection.close()



@app.route('/registro', methods=['POST'])
def create_registro():
    data = request.json
    if data:
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            # Verificar se a gaveta existe
            gaveta_id = data['Gaveta_idGaveta']
            cursor.execute("SELECT idGaveta FROM Gaveta WHERE idGaveta = %s", (gaveta_id,))
            gaveta = cursor.fetchone()
            if not gaveta:
                return jsonify({'message': 'Gaveta não encontrada'}), 404

            # Inserção no banco de dados
            query = "INSERT INTO Registro (data, hora, cor, observacao, Gaveta_idGaveta) VALUES (%s, %s, %s, %s, %s)"
            values = (data['data'], data['hora'], data['cor'], data['observacao'], gaveta_id)
            cursor.execute(query, values)
            connection.commit()

            return jsonify({'message': 'Registro criado com sucesso'}), 201
        except mysql.connector.Error as e:
            print("Erro ao inserir no banco de dados:", e)
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({'message': 'Dados inválidos'}), 400






@app.route('/registro', methods=['GET'])
def list_registros():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Registro"
        cursor.execute(query)
        registros = cursor.fetchall()
        return jsonify({'data': registros}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/registro/<int:registro_id>', methods=['DELETE'])
def delete_registro(registro_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Registro WHERE idRegistro = %s", (registro_id,))
        registro = cursor.fetchone()
        if not registro:
            return jsonify({'message': 'Registro não encontrado'}), 404
        cursor.execute("DELETE FROM Registro WHERE idRegistro = %s", (registro_id,))
        connection.commit()
        return jsonify({'message': 'Registro excluído com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_registros_por_gaveta_data/<int:gaveta_id>/<string:data>', methods=['GET'])
def get_registros_por_gaveta_data(gaveta_id, data):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT cor, observacao FROM Registro WHERE Gaveta_idGaveta = %s AND data = %s"
        cursor.execute(query, (gaveta_id, data))
        registros = cursor.fetchall()
        if registros:
            return jsonify({'data': registros}), 200
        else:
            return jsonify({'message': 'Nenhum registro encontrado para a gaveta e data especificadas'}), 404
    except mysql.connector.Error as err:
        print('Erro ao buscar registros:', err)
        return jsonify({'message': 'Erro ao buscar registros'}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/rack_estado_anterior/<int:rack_id>', methods=['GET'])
def rack_estado_anterior(rack_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        # Query para obter o estado mais recente antes da data atual para todas as gavetas associadas ao rack
        query = """
            SELECT G.idGaveta, R.estado, R.cor, R.observacao
            FROM Registro R
            INNER JOIN Gaveta G ON R.Gaveta_idGaveta = G.idGaveta
            WHERE G.Rack_idRack = %s
            ORDER BY R.data DESC, R.hora DESC
        """
        cursor.execute(query, (rack_id,))
        registros = cursor.fetchall()
        if registros:
            # Agrupar registros por gaveta e pegar o mais recente para cada gaveta
            gavetas = {}
            for registro in registros:
                gaveta_id = registro['idGaveta']
                if gaveta_id not in gavetas:
                    gavetas[gaveta_id] = registro
            return jsonify({'estado_anterior_rack': list(gavetas.values())}), 200
        else:
            return jsonify({'message': 'Nenhum estado anterior encontrado para o rack'}), 404
    except Exception as e:
        print('Erro ao buscar o estado anterior do rack:', str(e))
        return jsonify({'message': 'Falha ao buscar o estado anterior do rack'}), 500
    finally:
        cursor.close()
        connection.close()








@app.route('/get_registros_anteriores_por_rack_data/<int:rackId>/<string:formattedDate>', methods=['GET'])
def get_registros_anteriores_por_rack_data(rackId, formattedDate):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT R.*
            FROM Registro R
            INNER JOIN Gaveta G ON R.Gaveta_idGaveta = G.idGaveta
            WHERE G.Rack_idRack = %s AND R.data <= %s
                AND R.cor = %s AND R.observacao = %s
            ORDER BY R.data DESC
        """

        cor = request.args.get('cor')
        observacao = request.args.get('observacao')

        cursor.execute(query, (rackId, formattedDate, cor, observacao))
        registros = cursor.fetchall()
        return jsonify({'data': registros}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()



@app.route('/verificar_rack/<int:rack_id>/<int:gaveta_id>/<string:data>', methods=['GET'])
def verificar_rack(rack_id, gaveta_id, data):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Primeiro, verificar se existem registros para o rack
        query_rack = """
            SELECT G.idGaveta, R.estado, R.cor, R.observacao
            FROM Registro R
            INNER JOIN Gaveta G ON R.Gaveta_idGaveta = G.idGaveta
            WHERE G.Rack_idRack = %s
            ORDER BY R.data DESC, R.hora DESC
        """
        cursor.execute(query_rack, (rack_id,))
        registros_rack = cursor.fetchall()

        if registros_rack:
            # Agrupar registros por gaveta e pegar o mais recente para cada gaveta
            gavetas = {}
            for registro in registros_rack:
                gaveta_id = registro['idGaveta']
                if gaveta_id not in gavetas:
                    gavetas[gaveta_id] = registro
            return jsonify({'estado_anterior_rack': list(gavetas.values())}), 200
        else:
            # Caso não existam registros para o rack, buscar registros específicos para a gaveta e data
            query_gaveta = "SELECT cor, observacao FROM Registro WHERE Gaveta_idGaveta = %s AND data = %s"
            cursor.execute(query_gaveta, (gaveta_id, data))
            registros_gaveta = cursor.fetchall()

            if registros_gaveta:
                return jsonify({'data': registros_gaveta}), 200
            else:
                return jsonify({'message': 'Nenhum registro encontrado para a gaveta e data especificadas'}), 404
    except mysql.connector.Error as err:
        print('Erro ao buscar registros:', err)
        return jsonify({'message': 'Erro ao buscar registros'}), 500
    finally:
        cursor.close()
        connection.close()


def update_registro(registro_id, data, hora, cor, observacao, gaveta_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Verificar se o registro existe
        cursor.execute("SELECT idRegistro FROM Registro WHERE idRegistro = %s", (registro_id,))
        registro = cursor.fetchone()
        if not registro:
            return False, jsonify({'message': 'Registro não encontrado'}), 404

        # Atualizar o registro
        query = "UPDATE Registro SET data = %s, hora = %s, cor = %s, observacao = %s, Gaveta_idGaveta = %s WHERE idRegistro = %s"
        values = (data, hora, cor, observacao, gaveta_id, registro_id)
        cursor.execute(query, values)
        connection.commit()

        return True, jsonify({'message': 'Registro atualizado com sucesso'}), 200
    except Exception as e:
        print('Erro ao atualizar o registro:', str(e))
        return False, jsonify({'message': 'Falha ao atualizar o registro'}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/update_registro', methods=['PUT'])
def update_registro_route():
    data = request.get_json()
    if 'id' in data and 'data' in data and 'hora' in data and 'cor' in data and 'observacao' in data and 'Gaveta_idGaveta' in data:
        registro_id = data['id']
        data_registro = data['data']
        hora_registro = data['hora']
        cor = data['cor']
        observacao = data['observacao']
        gaveta_id = data['Gaveta_idGaveta']

        success, response, status_code = update_registro(registro_id, data_registro, hora_registro, cor, observacao,
                                                         gaveta_id)
        return response, status_code
    else:
        return jsonify({'message': 'Dados inválidos'}), 400

@app.route('/check_records/<int:rack_id>', methods=['GET'])
def check_records(rack_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT COUNT(*) as record_count 
            FROM Gaveta 
            WHERE Rack_idRack = %s AND descricao IS NOT NULL AND descricao != ''
        """
        cursor.execute(query, (rack_id,))
        result = cursor.fetchone()
        has_records = result['record_count'] > 0
        return jsonify({'hasRecords': has_records}), 200
    except Exception as e:
        print('Error checking records:', str(e))
        return jsonify({'message': 'Failed to check records'}), 500
    finally:
        cursor.close()
        connection.close()



if __name__ == '__main__':
    app.run(debug=True)