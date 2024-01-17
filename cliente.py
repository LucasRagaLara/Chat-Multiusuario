import socket
import threading
import logging
import os 

class Cliente:
    def __init__(self, HOST='localhost', PORT=65432):
        self.HOST = HOST
        self.PORT = PORT
        self.logger = logging.getLogger(__name__)
        logging_format = '%(asctime)s - %(levelname)s - %(message)s'
        # logging.basicConfig(filename="C:\\Users\\lucas\\Downloads\\a_practicas_examen\\dws\\ejercicio_chat_multiusuario\\logs\\client.logs", level=logging.DEBUG, format=logging_format)
        script_dir = os.path.dirname(__file__)
# Construye la ruta relativa para el archivo de registro en el directorio 'logs'
        log_file_path = os.path.join(script_dir, 'logs', 'client.log')
        logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format=logging_format)
        #muestra los logs en la consola
        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(logging.INFO)
        # console_handler.setFormatter(logging.Formatter(logging_format))
        # self.logger.addHandler(console_handler)
        self.logger.info('Configurado el log')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.info("Creado el socket")
    def iniciar_cliente(self):
        try:
            self.sock.connect((self.HOST, self.PORT))
            self.logger.info("Conectado el socket con el servidor en el puerto {} y en la dirección {} ".format(self.PORT, self.HOST))
            enviar_threading = threading.Thread(target=self.enviar_mensaje, args=(()))
            enviar_threading.start()
            recibir_threading = threading.Thread(target=self.recibir_mensaje)
            #Inicio de hilo para enviar un mensaje
            recibir_threading.start()
        except Exception as e:
            print(e)
            self.logger.debug("Ha ocurrido un error en iniciar_cliente()")
    def enviar_mensaje(self):
        while True:
            mensaje = input("-> ")
            self.sock.sendall(mensaje.encode())
            self.logger.info("Envío del mensaje: {}".format(mensaje))
    def recibir_mensaje(self):
        while True:
            mensaje_recibido = self.sock.recv(1024)
            if not mensaje_recibido:
                break
            else:
                print(mensaje_recibido.decode())
                self.logger.info("Recepción del mensaje {}".format(mensaje_recibido.decode()))
cliente1 = Cliente()
cliente1.iniciar_cliente()