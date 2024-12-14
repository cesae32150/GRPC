import psycopg2
import grpc
import pokemons_pb2
import pokemons_pb2_grpc

DATABASE_URL = "postgresql://neondb_owner:oY6xwyDWJhs2@ep-red-mode-a5r5pez0.us-east-2.aws.neon.tech/neondb?sslmode=require"

class PokemonsService(pokemons_pb2_grpc.PokemonsServiceServicer):
    def CreatePokemon(self, request, context):
        try:
            connection = psycopg2.connect(DATABASE_URL)
            cursor = connection.cursor()

            query = "INSERT INTO pokemon (nombre, descripcion, edad, poder) VALUES (%s, %s, %s, %s) RETURNING id"
            cursor.execute(query, (request.nombre, request.descripcion, request.edad, request.poder))
            pokemon_id = cursor.fetchone()[0]
            connection.commit()

            return pokemons_pb2.Pokemon(
                id=pokemon_id,
                nombre=request.nombre,
                descripcion=request.descripcion,
                edad=request.edad,
                poder=request.poder
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return pokemons_pb2.Pokemon()
        finally:
            cursor.close()
            connection.close()

    def ReadPokemon(self, request, context):
        try:
            connection = psycopg2.connect(DATABASE_URL)
            cursor = connection.cursor()

            query = "SELECT id, nombre, descripcion, edad, poder FROM pokemon WHERE id = %s"
            cursor.execute(query, (request.id,))
            result = cursor.fetchone()

            if result:
                return pokemons_pb2.Pokemon(
                    id=result[0],
                    nombre=result[1],
                    descripcion=result[2],
                    edad=result[3],
                    poder=result[4]
                )
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Pokemon no encontrado")
                return pokemons_pb2.Pokemon()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return pokemons_pb2.Pokemon()
        finally:
            cursor.close()
            connection.close()

    def UpdatePokemon(self, request, context):
        try:
            connection = psycopg2.connect(DATABASE_URL)
            cursor = connection.cursor()

            query = """
                UPDATE pokemon
                SET nombre = %s, descripcion = %s, edad = %s, poder = %s
                WHERE id = %s
            """
            cursor.execute(query, (request.nombre, request.descripcion, request.edad, request.poder, request.id))
            connection.commit()

            if cursor.rowcount > 0:
                return pokemons_pb2.Pokemon(
                    id=request.id,
                    nombre=request.nombre,
                    descripcion=request.descripcion,
                    edad=request.edad,
                    poder=request.poder
                )
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Pokemon no encontrado")
                return pokemons_pb2.Pokemon()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return pokemons_pb2.Pokemon()
        finally:
            cursor.close()
            connection.close()

    def DeletePokemon(self, request, context):
        try:
            connection = psycopg2.connect(DATABASE_URL)
            cursor = connection.cursor()

            query = "DELETE FROM pokemon WHERE id = %s"
            cursor.execute(query, (request.id,))
            connection.commit()

            if cursor.rowcount > 0:
                return pokemons_pb2.Empty()
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Pokemon no encontrado")
                return pokemons_pb2.Empty()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return pokemons_pb2.Empty()
        finally:
            cursor.close()
            connection.close()
