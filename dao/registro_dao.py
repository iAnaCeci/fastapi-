# from config import get_connection
#
# class RegistroDAO:
#     @staticmethod
#     def insert_registro(descricao, data_hora, usuario_id):
#         try:
#             connection = get_connection()
#             cursor = connection.cursor()
#             query = "INSERT INTO Registro (descricao, data_hora, usuario_id) VALUES (%s, %s, %s)"
#             values = (descricao, data_hora, usuario_id)
#             cursor.execute(query, values)
#             connection.commit()
#             registro_id = cursor.lastrowid
#             return registro_id
#         except Exception as e:
#             print('Error inserting registro:', str(e))
#             return None
#         finally:
#             cursor.close()
#             connection.close()
#
#     @staticmethod
#     def update_registro(registro_id, descricao, data_hora):
#         try:
#             connection = get_connection()
#             cursor = connection.cursor()
#             query = "UPDATE Registro SET descricao = %s, data_hora = %s WHERE idRegistro = %s"
#             values = (descricao, data_hora, registro_id)
#             cursor.execute(query, values)
#             connection.commit()
#             return True
#         except Exception as e:
#             print('Error updating registro:', str(e))
#             return False
#         finally:
#             cursor.close()
#             connection.close()
#
#     @staticmethod
#     def delete_registro(registro_id):
#         try:
#             connection = get_connection()
#             cursor = connection.cursor()
#             query = "DELETE FROM Registro WHERE idRegistro = %s"
#             cursor.execute(query, (registro_id,))
#             connection.commit()
#             return True
#         except Exception as e:
#             print('Error deleting registro:', str(e))
#             return False
#         finally:
#             cursor.close()
#             connection.close()
#
#     @staticmethod
#     def get_registro_by_id(registro_id):
#         try:
#             connection = get_connection()
#             cursor = connection.cursor(dictionary=True)
#             query = "SELECT * FROM Registro WHERE idRegistro = %s"
#             cursor.execute(query, (registro_id,))
#             registro = cursor.fetchone()
#             return registro
#         except Exception as e:
#             print('Error fetching registro:', str(e))
#             return None
#         finally:
#             cursor.close()
#             connection.close()
#
#     @staticmethod
#     def get_all_registros():
#         try:
#             connection = get_connection()
#             cursor = connection.cursor(dictionary=True)
#             query = "SELECT * FROM Registro"
#             cursor.execute(query)
#             registros = cursor.fetchall()
#             return registros
#         except Exception as e:
#             print('Error fetching registros:', str(e))
#             return None
#         finally:
#             cursor.close()
#             connection.close()
