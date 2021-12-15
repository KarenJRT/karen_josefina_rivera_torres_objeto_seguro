from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

class ObjetoSeguro:
    def __init__(self, nombre: str):
        # Atributos
        self.nombre = nombre
        self.__gen_llaves()  #debe ser metodo privado
        self.__llavePrivada, self.llavePublica = self.__gen_llaves() #llave privada debe ser privada
        self.__id= 0 #para guardar mensajes
        self.__mensajeRecibido = "" #mensaje recibido
        self.__registro = {}

        # Generamos un archivo vacio cada vez que se inicia la clase.
        archivo = "RegistroMsj_" + self.nombre + ".txt"
        archivo = open(archivo, 'w')
        archivo.close()

    # Metodos
    # metodo generar llaves, debe ser privado ya que las llaves solo pertenecen a uno
    def __gen_llaves(self):
        llaveprivada = RSA.generate(1024).exportKey()
        llavepublica = RSA.generate(1024).publickey().exportKey()
        return llaveprivada, llavepublica

    # metodo saludar, el aludo se debe cifrar con la llave publica del destinatario receptor
    def saludar(self, name: str, msj: str):
        Kpublicadestinatario = self.llave_publica() #llave del destinatario
        self.__mensajeRecibido = msj #almacenanmos el mensaj recibido, recordar que es privado
        print(f"Hola soy {name} y te mande un mensaje") #anuncio quien mando mensjae
        return self.__cifrar_msj(Kpublicadestinatario, msj) #cifrar mensaje con la llave publica

    #metodo para responder, se debe codificar el mensaje respuesta
    def responder(self, msj: str) -> bytes:
        print((f"Hola {msj} recibi tu mensaje"))
        return self.__mensajeRecibido + self.__codificar64("MensajeRespuesta")

    #metodo llamar la llave publica
    def llave_publica(self) -> str:
            return self.llavePublica

    # metodo cifrar mensaje, el mensaje debe esta codificado en base 64
    def __cifrar_msj(self, pub_key: str, msj: str) -> bytes:
        llavePublica = RSA.importKey(pub_key)
        llavePublica =PKCS1_OAEP.new(llavePublica)
        msjCifrado = llavePublica.encrypt(self.__codificar64(msj))
        return msjCifrado

    # metodo descifrar mensaje, el mensaje debe esta decodificado en base 64
    def __descifrar_msj(self, msj: bytes) -> bytes:
        llavePrivada = RSA.importKey(self.__llavePrivada)
        llavePrivada = PKCS1_OAEP.new(llavePrivada)
        msjDescifrado = self.__decodificar64(llavePrivada.decrypt(msj))
        return msjDescifrado

    # metodo codificar en base 64 el mensaje
    def __codificar64(self, msj: str) -> bytes:
        msjcodificado = base64.b64encode(msj.encode('ascii')) #usamos el encoded para codificar con ascii
        return msjcodificado

    # metodo decodificar en base 64 el mensaje
    def __decodificar64(self, msj: bytes) -> str:
        msjdecodificado = base64.b64decode(msj)
        return msjdecodificado.decode("ascii") #usamos el encoded para codificar con ascii

    # metodo almacenar mensaje, lo guardamos en un archivo .txt
    def almacenar_msj(self, msj: str) -> dict:
        archivo = "RegistroMsj_" + self.nombre + ".txt"
        self.__registro[self.__id] = {
            "ID": self.__id,
            "MSJ": msj
            }
        with open(archivo, 'a') as f:
            f.write(str(self.__registro[self.__id]) + str("\n"))
        self.__id += 1
        return {"ID": self.__id}

    # metodo consultar mensaje, aqui buscaremos los mensajes en el archivo generado
    def consultar_msj(self, id: int):
        archivo = "RegistroMsj_" + self.nombre + ".txt"
        inicio = 0
        with open(archivo, 'r') as buscar:
            for line in buscar:
                if inicio == id:
                    print(line)
                    return (line)
                inicio += 1
        return "No se encontro la consula"  # opcinal

    # metodo esperar respuesta, aqui esperamos la respuesta del objeto, y el mensaje debe almacenarse
    def esperar_respuesta(self, msj: bytes):
        print("Mensaje recibido, esperando respuesta", msj)
