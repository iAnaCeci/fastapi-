# from config import get_connection
#
# class GavetaDAO:
#     @staticmethod
#     def insert_gaveta(nome, descricao, estado, rack_id):
#         try:
#             connection = get_connection()
#             cursor = connection.cursor()
#             query = "INSERT INTO Gaveta (nome, descricao, estado, Rack_idRack) VALUES (%s, %s, %s, %s)"
#             values = (nome, descricao, estado, rack_id)
#             cursor.execute(query, values)
#             connection.commit()
#             return True
#         except Exception as e:
#             print('Error inserting drawer information:', str(e))
#             return False
#         finally:
#             cursor.close()
#             connection.close()
#
#     @staticmethod
#     def update_gaveta(gaveta_id, nome, descricao, estado):
#         try:
#             connection = get_connection()
#             cursor = connection.cursor()
#             query = "UPDATE Gaveta SET nome = %s, descricao = %s, estado = %s WHERE idGaveta = %s"
#             values = (nome, descricao, estado, gaveta_id)
#             cursor.execute(query, values)
#             connection.commit()
#             return True
#         except Exception as e:
#             print('Error updating drawer information:', str(e))
#             return False
#         finally:
#             cursor.close()
#             connection.close()
#
#     @staticmethod
#     def delete_gaveta(gaveta_id):
#         try:
#             connection = get_connection()
#             cursor = connection.cursor()
#             cursor.execute("DELETE FROM Gaveta WHERE idGaveta = %s", (gaveta_id,))
#             connection.commit()
#             return True
#         except Exception as e:
#             print('Error deleting drawer:', str(e))
#             return False
#         finally:
#             cursor.close()
#             connection.close()
#
#     @staticmethod
#     def get_gavetas_by_rack(rack_id):
#         try:
#             connection = get_connection()
#             cursor = connection.cursor(dictionary=True)
#             query = "SELECT * FROM Gaveta WHERE Rack_idRack = %s"
#             cursor.execute(query, (rack_id,))
#             gavetas = cursor.fetchall()
#             return gavetas
#         except Exception as e:
#             print('Error fetching drawers:', str(e))
#             return None
#         finally:
#             cursor.close()
#             connection.close()
#
#
#
#
# def get_all_gavetas(self):
#        try:
#            cursor = self.connection.cursor(dictionary=True)
#            query = "SELECT * FROM Gaveta"
#            cursor.execute(query)
#            gavetas = cursor.fetchall()
#            return gavetas
#        except Exception as e:
#            print('Error fetching gavetas:', str(e))
#            return None
#        finally:
#            cursor.close()