import csv
from datetime import datetime
from random import randint
import time
import threading
import os
from bs4 import BeautifulSoup
from modulo3 import ArbolBB
from modulo1 import ArbolAVL
from modulo2 import NArbol
from modulo4 import BTreeCache

class Module4: # MODULO 4 CON SUS COMANDOS Y SUS METODOS
    def __init__(self):
        self.carpeta = r"src\paginas" # Indica la ruta de los archivos
        self.archivo_actual = None

    def listar_paginas(self,arg): # METODO PARA LISTAR LOS ARCHIVOS.HTML CONSEGUIDOS
        archivos = [f for f in os.listdir(self.carpeta) if f.endswith('.html')] # Busca los archivos que terminen en .html en la carpeta indicada
        print("\nPaginas encontradas:")
        for archivo in archivos:
            print(f"- {archivo}")
        print("")

    def mostrar_contenido(self, archivo, modo): # METODO PARA MOSTRAR EL CONTENIDO DE UN ARCHIVO.HTML
        try:
            if archivo != None:
                path = os.path.join(self.carpeta, archivo) # Crea una ruta en la que buscar el archivo indicado
                if os.path.exists(path): # Verifica que la ruta exista
                    self.archivo_actual = path
                else:
                    print(f"Archivo {archivo} no encontrado.")

                if not self.archivo_actual:
                    print("No hay ningún archivo cargado.")
                    return

            with open(self.archivo_actual, 'r', encoding='utf-8') as archivo: # Abre el archivo.html y lo lee
                contenido = archivo.read()

            if modo == "basico":
                print(f"\n{contenido}") # Imprime el contenido de forma basica
            elif modo == "texto_plano":
                soup = BeautifulSoup(contenido, 'html.parser')
                print(f"\n{soup.get_text()}") # Imprime solo el texto del archivo
            else:
                print("Modo no reconocido. Usa 'basico' o 'texto_plano'.")
            print("")

        except Exception:
            print("No se ha podido encontrar el archivo.\n")

    def actualizar_archivo(self,archivo):
        self.archivo_actual = archivo
        
    def agregar_cache(self, url, contenido):
        cache.insertar(url, contenido)

    # Comando para obtener caché
    def obtener_cache(self, url):
        contenido = cache.buscar(url)
        if contenido:
            return contenido
        return "No encontrado en caché"

    # Comando para vaciar caché por URL o por fecha
    def vaciar_cache(self, url=None, fecha=None):
        if url:
            cache.eliminar_por_url(url)
        elif fecha:
            cache.eliminar_por_fecha(fecha)

class Module2: # MODULO 2 Y SUS METODOS
    def __init__(self):
        self.pestañas = ListaDoblamenteEnlazada()
        self.pestaña_actual = None
        self.hosts = r"src\paginas\hosts.txt"

    def nueva_pestaña(self, url): # METODO PARA ABRIR UNA NUEVA PESTAÑA
        if url == None:
            print("Este comando necesita de un argumento")
        else:
            check = False
            try:
                with open(self.hosts, 'r') as txt:
                    lineas = txt.readlines()
                for linea in lineas[1:]:
                    linea = linea.split()
                    archivo = linea[0]
                    for elemento in linea[1:]:
                        if url == elemento:
                            self.pestañas.agregar(url)
                            check = True
                            if self.pestaña_actual is None:  # Si es la primera pestaña, establecer como actual
                                self.pestaña_actual = self.pestañas.inicio
                            print(f"Abriste una nueva pestaña con: {url}")

                if check == False:
                    print("No se puedo encontrar dicha Url o Ip.")
            except Exception:
                print("Url o Ip inexistente.")
                
    def cerrar_pestaña(self,arg): # METODO PARA CERRAR LA PRIMERA PESTAÑA
        if self.pestaña_actual:
            print(f"Cerrando la pestaña con: {self.pestaña_actual.url}")
            siguiente_pestaña = self.pestaña_actual.siguiente
            self.pestañas.eliminar(self.pestaña_actual)
            self.pestaña_actual = siguiente_pestaña if siguiente_pestaña else self.pestañas.inicio

    def cambiar_pestaña(self, n): # METODO PARA CAMBIAR A LA PESTAÑA INDICADA
        n = int(n)
        if n == None:
            print("Este comando necesita de un argumento")
        else:
            nodo = self.pestañas.obtener_pestaña(n - 1)
            if nodo:
                self.pestaña_actual = nodo
                print(f"Ahora estás en la pestaña con: {self.pestaña_actual.url}")
            else:
                print("Pestaña no encontrada.")

    def mostrar_pestañas(self,arg): # METODO PARA MOSTRAR LAS PESTAÑAS ABIERTAS
        pestañas = self.pestañas.mostrar()
        if pestañas:
            print("\nPestañas abiertas:")
            print("\n".join(pestañas))
        else:
            print("No hay pestañas abiertas.")

class Nodo:
    def __init__(self, url):
        self.url = url
        self.siguiente = None
        self.anterior = None

class ListaDoblamenteEnlazada:
    def __init__(self):
        self.inicio = None
        self.fin = None
        self.tamanio = 0

    def agregar(self, url):
        nuevo_nodo = Nodo(url)
        if self.tamanio == 0:
            self.inicio = self.fin = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.fin
            self.fin.siguiente = nuevo_nodo
            self.fin = nuevo_nodo
        self.tamanio += 1

    def eliminar(self, nodo):
        if nodo.anterior:
            nodo.anterior.siguiente = nodo.siguiente
        if nodo.siguiente:
            nodo.siguiente.anterior = nodo.anterior

        if nodo == self.inicio:
            self.inicio = nodo.siguiente
        if nodo == self.fin:
            self.fin = nodo.anterior

        self.tamanio -= 1

    def obtener_pestaña(self, index):
        actual = self.inicio
        for _ in range(index):
            if actual is not None:
                actual = actual.siguiente
        return actual

    def mostrar(self):
        actual = self.inicio
        pestañas = []
        index = 1
        while actual:
            pestañas.append(f"{index}. {actual.url}")
            actual = actual.siguiente
            index += 1
        return pestañas
    
class Module3: # MODULO 3 Y SUS METODOS
    def __init__(self):
        self.descargas = []

    def descargar(self,archivo): # METODO PARA DESCARGAR EL ARCHIVO INDICADO
        if archivo == None:
            print("Este comando necesita de un argumento.\n")
        else:
            print(f"Iniciando descarga en segundo plano de: {archivo}")
            self.descargas.append((archivo,str(randint(1,31))+" MB","PENDIENTE",datetime.now())) # Genera una descarga con un tamaño random entre 1 y 50
            n = len(self.descargas)
            hilo = threading.Thread(target= self.segundo_plano,args=[n]) # Crea un hilo que ejecuta la funcion segundo_plano
            hilo.start() # Inicio del proceso en segundo plano

            self.guardar_descargas(n)

    def segundo_plano(self,n): # METODO QUE PROCESA LA DESCARGA EN SEGUNDO PLANO
        archivo, size, estado, tiemstamp = self.descargas[-1]
        tiempo = size.split()[0] 
        time.sleep(int(tiempo)) # El tiempo de descarga es equivalente al tamaño del archivo
        self.descargas[n-1] = (self.descargas[n-1][0], self.descargas[n-1][1], "COMPLETADO", self.descargas[n-1][3]) # Actualiza el estado del archivo una vez ya completada la descarga
        self.actualizar_descargas(n)
    
    def cancelar_descarga(self, n): # METODO PARA CANCELAR UNA DESCARGA
        try:
            n = int(n)
            if n == None:
                print("Este comando necesita de un argumento.\n")
            elif n == 0:
                print("No existe esa descarga.")
            else:
                archivo, size, estado, tiemstamp = self.descargas[n-1]
                if estado != "COMPLETADO": # Verifica que la descarga no se haya completado aun
                    self.descargas.pop(n-1)
                    self.guardar_descargas(None)
                    print(f"Descarga cancelada: {archivo}")
                else:
                    print("La descarga ya se ha completado. No se puede cancelar.")
                    
        except Exception:
            print("No existe esa descarga.")

    def mostrar_descargas(self,arg): # METODO PARA MOSTRAR EL REGISTRO DE DESCARGAS
        print("\nCola de descargas:")
        with open("src/descargas.csv", mode='r') as file: # Lee el archivo descargas.csv y lo imprime
            reader = csv.reader(file)
            i = 0
            for row in reader:
                if i == 0:
                    print(f"   {row}")
                else:
                    print(f"{i}.-{row}")
                i+=1
        print("")

    def actualizar_descargas(self,n):
        with open("src/descargas.csv", mode='r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            filtrado = []
            archivo, size, estado, tiemstamp = self.descargas[n-1]
            for linea in reader:
                if linea[0] == str(archivo) and linea[1] == str(size) and linea[3] == str(tiemstamp):
                    filtrado.append(self.descargas[n-1])
                else:
                    filtrado.append((linea[0],linea[1],linea[2],linea[3]))

        with open("src/descargas.csv", mode='w', newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(("Archivo","Tamaño","Estado","Fecha y Hora"))
            for i in filtrado:
                writer.writerow(i)
                    

    def guardar_descargas(self,n): # METODO QUE ACTUALIZA EL ARCHIVO descargas.csv
        if n != None:
            with open("src/descargas.csv",'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.descargas[n-1])
        else:
            with open("src/descargas.csv",'w',newline='') as file:
                writer = csv.writer(file)
                writer.writerow(("Archivo","Tamaño","Estado","Fecha y Hora"))
                for descarga in self.descargas:
                    writer.writerow(descarga)

    def filtrar_descargas(self):
        with open("descargas.csv", mode='r') as archivo:
            try:
                reader = csv.reader(archivo)
                next(reader)
                i = 0
                filtrado = []
                for linea in reader:
                    archivo, size, estado, timestamp = (linea[0],linea[1],linea[2],linea[3])
                    if estado == "COMPLETADO":
                        self.descargas.append((archivo,size,estado,timestamp))
                        filtrado.append(self.descargas[i])
                        i+=1

                with open("src/descargas.csv", mode='w', newline='') as archivo:
                    writer = csv.writer(archivo)
                    writer.writerow(("Archivo","Tamaño","Estado","Fecha y Hora"))
                    for i in filtrado:
                        writer.writerow(i)

            except Exception:
                return
            
    def buscar(self, clave):
        arbol3.buscar_clave(clave)

    def mostrar_historial_busquedas(self, arg):
        arbol3.inorder(arbol3.raiz)
    
    def eliminar_busqueda(self, opcion, arg):
        if opcion == '--key':
            arbol3.eliminar_clave(arg)
            self._eliminar_del_csv(arg, 0)
            print(f"Se han eliminado las búsquedas con la palabra clave: {arg}")
        elif opcion == '--fecha':
            arbol3.eliminar_fecha(arg)
            self._eliminar_del_csv(arg, 1)
            print(f"Se han eliminado las búsquedas de fecha posterior a: {arg}")
        else:
            print("Opción no válida")

    def cargar_busquedas(self):
        with open('busquedas.csv', mode='r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                arbol3.cargar([row[0], row[1]])

    def _eliminar_del_csv(self, valor, indice):
        filas_filtradas = []
        with open('busquedas.csv', mode='r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if indice == 0:
                    if valor not in row[indice]:
                        filas_filtradas.append(row)
                else:
                    if row[indice] < valor:
                        filas_filtradas.append(row)

        with open('busquedas.csv', mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(filas_filtradas)

class Module1: # MODULO 1 Y SUS METODOS
    def __init__(self):
        self.historial = [] # Lista que guarda el historial de busquedas
        self.historial_adelante = [] # Lista que guarda las busquedas posteriores
        self.hosts = r"src\paginas\hosts.txt"

    def ir(self, url): # METODO QUE PERMITE VISITAR UNA IP O URL
        archivo = None
        if url == None:
            print("Este comando necesita de un argumento.\n")
        else:
            check = False
            try:
                with open(self.hosts, 'r') as txt:
                    lineas = txt.readlines()
                for linea in lineas[1:]:
                    linea = linea.split()
                    archivo = linea[0]
                    for elemento in linea[1:]:
                        if url == elemento:
                            check = True
                            Modulo4.actualizar_archivo(archivo)

            except FileNotFoundError:
                print("Archivo de historial no encontrado.")

            if check == True:
                self.historial.append((url, datetime.now()))
                self.historial_adelante.clear()
                arbol3.insertar(url)
                print(f"Visitando: {url}")

                with open("src/historial.csv", 'a', newline='') as csvfile: 
                    writer = csv.writer(csvfile)
                    url, timestamp = self.historial[-1]
                    writer.writerow([url, timestamp])
            else:
                print("Url o Ip no reconocida.")
    
    def atras(self, arg): # METODO QUE PERMITE RETROCEDER EN EL HISTORIAL
        if self.historial:
            pagina_actual = self.historial.pop()
            self.historial_adelante.append(pagina_actual)
            if self.historial:
                print(f"Volviendo a: {self.historial[-1][0]}")
            else:
                print("No hay más páginas en el historial.")
        else:
            print("No hay más páginas en el historial.")
    
    def adelante(self, arg): # METODO QUE PERMITE AVANZAR EN EL HISTORIAL
        if self.historial_adelante:
            pagina_actual = self.historial_adelante.pop()
            self.historial.append(pagina_actual)
            print(f"Avanzando a: {pagina_actual[0]}")
        else:
            print("No hay más páginas para avanzar.")

    def mostrar_historial(self,arg): # METODO QUE IMPRIME EL ARCHIVO historial.csv
        print("\nHistorial de navegación:")
        with open("historial.csv", mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)
        print("")
        
    # Funciones para manejar el archivo CSV
    def cargar_favoritos(self):
        favoritos = []
        try:
            with open('favoritos.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:  # Evitar filas vacías
                        url, nombre, fecha = row
                        favoritos.append((url, nombre, fecha))
        except FileNotFoundError:
            print("El archivo favoritos.csv no existe.")
        return favoritos

    def guardar_favoritos(self,favoritos):
        with open('favoritos.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for url, nombre, fecha in favoritos:
                writer.writerow([url, nombre, fecha])
        print(f"Se han guardado {len(favoritos)} favoritos en el archivo favoritos.csv.")

    # Funciones para manejar los comandos
    def agregar_favorito(self,url, nombre):
        if not url or not nombre:
            print("Error: La URL o el nombre del sitio no pueden estar vacíos.")
            return
        arbol1.agregar_favorito_comando(url, nombre)
        lista= self.cargar_favoritos()
        lista.append((url, nombre, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        arbol1.guardar_favoritos(lista)
        print(f"Favorito agregado: {url}")

    def eliminar_favorito(self,url):
        print(f"Eliminando el favorito con URL: {url}")
        
        # Eliminar el favorito del árbol
        arbol1.raiz = arbol1.eliminar_favorito(arbol1.raiz, url)
        lista= self.cargar_favoritos()
        # Eliminar el favorito de la lista de favoritos
        favoritos = [f for f in lista if f[0] != url]

        # Guardar la lista de favoritos actualizada
        self.guardar_favoritos(favoritos)
        
        print(f"Favorito eliminado: {url}")
    
    def buscar_favorito(self,url=str):
        favorito = arbol1.buscar_favorito(arbol1.raiz,url)
        if favorito:
            print(f"Favorito encontrado: {favorito.url} - {favorito.nombre} - {favorito.fecha}")
        else:
            print("Favorito no encontrado.")

    def mostrar_favoritos(self,args):
        arbol1.mostrar_favoritos(arbol1.raiz)        

class Main:  # MODULO PRINCIPAL
    def __init__(self):
        self.modulos = {
            "Modulo1": ["ir", "atras", "adelante", "mostrar_historial", "mostrar_favoritos", "buscar_favorito", "eliminar_favorito", "agregar_favorito"],
            "Modulo2": ["nueva_pestaña", "cerrar_pestaña", "cambiar_pestaña", "mostrar_pestañas"],
            "Modulo3": ["descargar", "mostrar_descargas", "cancelar_descarga", "buscar", "mostrar_historial_busquedas", "eliminar_busqueda"],
            "Modulo4": ["mostrar_contenido", "listar_paginas","agregar_cache","obtener_cache","vaciar_cache"]
        }

    def Inicio(self):  # METODO QUE INTERPRETA LA PETICION DEL USUARIO
        try:
            print("> ", end='')
            comando = input().lower().split()
            
            if comando[0] == "salir":
                for letra in "Cerrando el navegador. ¡Hasta la próxima!":
                    print(letra, end='', flush=True)
                    time.sleep(0.025)
                time.sleep(2)
                print()
                for letra in "Fin de la simulacion":
                    print(letra, end='', flush=True)
                    time.sleep(0.025) 
                print()
                os._exit(0)
                return
            
            elif comando[0] == "/help":
                print("\nir <url o ip>\natras\nadelante\n"
                      "mostrar_historial\nnueva_pestaña <url o ip>\n"
                      "cerrar_pestaña\ncambiar_pestaña <n>\nmostrar_pestañas"
                      "\ndescargar <url>\nmostrar_descargas\n"
                      "cancelar_descarga <n>\nlistar_paginas\n"
                      "mostrar_contenido <archivo.html> <modo>\n")
            
            else:
                # Asegúrate de que haya al menos dos partes en el comando
                if len(comando) < 2:
                    comando.append(None)
                
                # Itera a través de los módulos y verifica si el comando coincide
                for clave, lista in self.modulos.items():
                    for valor in lista:
                        if comando[0] == valor:
                            if comando[0] == "eliminar_busqueda":
                                if comando[1] == "--fecha":
                                    comando[2] += " " + comando[3]
                                    eval(clave + "." + valor + "(" + 'comando[1]' + "," + 'comando[2]' + ")")
                            elif comando[0] == "agregar_favorito":
                                # Si el comando es "agregar_favorito", asegúrate de pasar los dos parámetros (URL y nombre)
                                if len(comando) >= 3:  # Verifica que se hayan pasado al menos 2 parámetros
                                    eval(clave + "." + valor + "(" + 'comando[1]' + "," + 'comando[2]' + ")")
                                else:
                                    print("Error: Se requiere una URL y un nombre para agregar un favorito.")
                            elif comando[0] != "mostrar_contenido":
                                eval(clave + "." + valor + "(" + 'comando[1]' + ")")
                            elif len(comando) == 3:
                                eval(clave + "." + valor + "(" + 'comando[1]' + "," + 'comando[2]' + ")")
                            else:
                                eval(clave + "." + valor + "(" + 'None' + "," + 'comando[1]' + ")")
        
        except Exception as e:
            print(f"Ocurrió un error: {e}")
        
        self.Inicio()


print("\nBienvenido al Simulador de Navegador Web en Consola.\n"
      "Escribe un comando para comenzar. Usa '/help' para ver la lista de comandos disponibles.\n")
principal = Main()
Modulo1 = Module1()
Modulo2 = Module2()
Modulo3 = Module3()
Modulo4 = Module4()
arbol3 = ArbolBB()
arbol1 = ArbolAVL()
cache = BTreeCache(orden=4)
Modulo3.filtrar_descargas()
Modulo3.cargar_busquedas()
arbol1.cargar_favoritos()
principal.Inicio()