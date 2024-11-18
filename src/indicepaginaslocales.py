class Nodo:
    def __init__(self, nombre, contenido=None):
        self.nombre = nombre
        self.contenido = contenido
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def listar_paginas(self, prefijo=''):
        # Recorre el árbol en orden y muestra las páginas
        resultado = []
        if self.contenido is not None:
            resultado.append(f"{prefijo}{self.nombre}")
        else:
            for hijo in self.hijos:
                resultado.extend(hijo.listar_paginas(f"{prefijo}{self.nombre}/"))
        return resultado

    def buscar_pagina(self, url):
        if self.contenido is not None and self.nombre == url:
            return self.contenido
        for hijo in self.hijos:
            resultado = hijo.buscar_pagina(url)
            if resultado:
                return resultado
        return None

class NArbol:
    def __init__(self):
        self.raiz = Nodo("")

    def agregar_pagina(self, ruta, contenido):
        partes = ruta.split('/')
        nodo_actual = self.raiz
        
        for parte in partes:
            encontrado = False
            for hijo in nodo_actual.hijos:
                if hijo.nombre == parte:
                    nodo_actual = hijo
                    encontrado = True
                    break
            
            if not encontrado:
                nuevo_nodo = Nodo(parte)
                nodo_actual.agregar_hijo(nuevo_nodo)
                nodo_actual = nuevo_nodo
        
        nodo_actual.contenido = contenido

    def listar_paginas(self):
        return self.raiz.listar_paginas()

    def ir(self, url): 
        partes = url.split('/') 
        nodo_actual = self.raiz 
        for parte in partes: 
            encontrado = False 
            for hijo in nodo_actual.hijos: 
                if hijo.nombre == parte: 
                    nodo_actual = hijo 
                    encontrado = True 
                    break 
                if not encontrado: 
                    return None 
        return nodo_actual.contenido

def cargar_archivo(nombre_archivo):
    arbol = NArbol()
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea:
                ruta, contenido = linea.split(';')
                arbol.agregar_pagina(ruta, contenido.strip())
    return arbol

def main():
    arbol = cargar_archivo("C:/Users/pc/Desktop/host.txt")

    while True:
        comando = input("> ").strip()
        
        if comando == "listar_paginas":
            print("Páginas HTML disponibles:")
            paginas = arbol.listar_paginas()
            for pagina in paginas:
                print(f"- {pagina}")
        
        elif comando.startswith("ir "):
            url = comando[3:]
            contenido = arbol.ir(url)
            if contenido:
                print(f"Visitando: {url}")
                print("Contenido (Modo Básico):")
                print(contenido)
            else:
                print("Página no encontrada.")
        
        elif comando == "salir":
            print("Cerrando el navegador. ¡Hasta la próxima!")
            break
        
        else:
            print("Comando no reconocido.")

if __name__ == "__main__":
    main()