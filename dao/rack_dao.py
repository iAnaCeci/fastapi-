# from config import get_connection
#
# class RackDAO:
#     @staticmethod
#     def insert_rack(nome, localizacao, descricao):
#         try:
#             connection = get_connection()
#             cursor = connection.cursor()
#             query = "INSERT INTO Rack (nome, localizacao, descricao) VALUES (%s, %s, %s)"
#             values = (nome, localizacao, descricao)
#             cursor.execute(query, values)
#             connection.commit()
#             rack_id = cursor.lastrowid
#             return rack_id
#         except Exception as e:
#             print('Error inserting rack information:', str(e))
#             return None
#         finally:
#             cursor.close()
#             connection.close()
#
#     @staticmethod
#     def get_rack_by_id(rack_id):
#         try:
#             connection = get_connection()
#             cursor = connection.cursor(dictionary=True)
#             query = "SELECT * FROM Rack WHERE idRack = %s"
#             cursor.execute(query, (rack_id,))
#             rack = cursor.fetchone()
#             return rack
#         except Exception as e:
#             print('Error fetching rack details:', str(e))
#             return None
#         finally:
#             cursor.close()
#             connection.close()
#
#     @staticmethod
#     def delete_rack(rack_id):
#         try:
#             connection = get_connection()
#             cursor = connection.cursor()
#             cursor.execute("DELETE FROM Gaveta WHERE Rack_idRack = %s", (rack_id,))
#             cursor.execute("DELETE FROM Rack WHERE idRack = %s", (rack_id,))
#             connection.commit()
#         except Exception as e:
#             print('Error deleting rack:', str(e))
#             return False
#         finally:
#             cursor.close()
#             connection.close()
#         return True
