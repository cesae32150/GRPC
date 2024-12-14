from concurrent import futures
import grpc
import pokemons_pb2_grpc
from pokemons_service import PokemonsService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Agregar el servicio al servidor
    pokemons_pb2_grpc.add_PokemonsServiceServicer_to_server(PokemonsService(), server)
    server.add_insecure_port('[::]:8000')
    print("Servidor gRPC corriendo en el puerto 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
