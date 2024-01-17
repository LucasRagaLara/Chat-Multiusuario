import socket
import threading
import logging

class Servidor:
    def __init__(self, HOST='localhost', PORT=65432):
        self.HOST = HOST
        self.PORT = PORT
        self.logger = logging.getLogger(__name__)
        # Inicializamos el log
        logging_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(filename='./logs/server.logs', level=logging.DEBUG, format=logging_format)
        # Obtenemos objeto logger
        # Creamos un StreamHandler (el manejador) para llevar los registros
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(logging_format))
        # Agregamos el manejador al objeto logger
        self.logger.addHandler(console_handler)
        self.logger.info('Configurado el log')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientes = []

    def iniciar_servidor(self):
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen()
        self.logger.info("Servidor conectado en el puerto {}".format(self.PORT))
        while True:
            conn, addr = self.sock.accept()
            #hilo para el cliente
            nombre_cliente = self.recibir_nombre_usuario(conn)
            self.logger.info("El cliente: {}, se ha conectado.".format(nombre_cliente))
            print("El cliente: {}, se ha conectado.".format(nombre_cliente.decode()))
            self.logger.info("Iniciado el hilo para cada cliente")
            cliente_enviar = threading.Thread(target=self.redireccionar_Mensaje, args=((conn, addr, nombre_cliente)))
            cliente_enviar.start()

    def recibir_nombre_usuario(self, conn):
        self.logger.info("Pedimos nombre de usuario al cliente")
        while True:
            conn.sendall("Introduce tu nombre de usuario: ".encode())
            nombre = conn.recv(1024)
            if not nombre or nombre.decode() in self.clientes:
                conn.sendall("Nombre inválido. Inténtalo de nuevo: ".encode())
            else:
                self.clientes.append((nombre.decode(), conn))
                return nombre
            
    def redireccionar_Mensaje(self, conn, addr, nombre_cliente):
        self.logger.info("Inicio envío de mensajes")
        with conn:
            self.logger.debug("Entra en el with conn de 'EnviarMensaje' ")
            while True:
                mensaje_cliente = conn.recv(1024)
                mensaje = "{}: {}".format(nombre_cliente.decode(), mensaje_cliente.decode())
                if not mensaje_cliente:
                    break
                for nombre, conexion in self.clientes:
                    if conexion != conn:
                        conexion.sendall(mensaje.encode())
                self.logger.info("Mensaje a los clientes enviado.")
# Instanciamos el objeto
servidor1 = Servidor()
servidor1.iniciar_servidor()