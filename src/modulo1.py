import csv
from datetime import datetime

class Nodo:
    def __init__(self, url, nombre):
        self.url = url
        self.nombre = nombre
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Fecha de adición
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    # Inserta un nuevo favorito en el árbol AVL
    def insertar(self, root, url, nombre):
        if root is None:
            return Nodo(url, nombre)

        if url < root.url:
            root.izquierda = self.insertar(root.izquierda, url, nombre)
        else:
            root.derecha = self.insertar(root.derecha, url, nombre)

        # Actualiza la altura del nodo
        root.altura = 1 + max(self.altura(root.izquierda), self.altura(root.derecha))

        # Obtiene el factor de balance
        balance = self.obtener_balance(root)

        # Rotaciones para balancear el árbol
        if balance > 1 and url < root.izquierda.url:
            return self.rotacion_derecha(root)

        if balance < -1 and url > root.derecha.url:
            return self.rotacion_izquierda(root)

        if balance > 1 and url > root.izquierda.url:
            root.izquierda = self.rotacion_izquierda(root.izquierda)
            return self.rotacion_derecha(root)

        if balance < -1 and url < root.derecha.url:
            root.derecha = self.rotacion_derecha(root.derecha)
            return self.rotacion_izquierda(root)

        return root

    def altura(self, nodo):
        if nodo is None:
            return 0
        return nodo.altura

    def obtener_balance(self, nodo):
        if nodo is None:
            return 0
        return self.altura(nodo.izquierda) - self.altura(nodo.derecha)

    def rotacion_derecha(self, y):
        x = y.izquierda
        t2 = x.derecha
        x.derecha = y
        y.izquierda = t2
        y.altura = max(self.altura(y.izquierda), self.altura(y.derecha)) + 1
        x.altura = max(self.altura(x.izquierda), self.altura(x.derecha)) + 1
        return x

    def rotacion_izquierda(self, x):
        y = x.derecha
        t2 = y.izquierda
        y.izquierda = x
        x.derecha = t2
        x.altura = max(self.altura(x.izquierda), self.altura(x.derecha)) + 1
        y.altura = max(self.altura(y.izquierda), self.altura(y.derecha)) + 1
        return y

    # Agregar URL al árbol AVL
    def agregar_favorito(self, url, nombre):
        self.raiz = self.insertar(self.raiz, url, nombre)

    # Buscar un favorito en preorden
    def buscar_favorito(self, root, url):
        if root is None or root.url == url:
            return root
        if url < root.url:
            return self.buscar_favorito(root.izquierda, url)
        return self.buscar_favorito(root.derecha, url)

    # Mostrar los favoritos en postorden
    def mostrar_favoritos(self, root):
        if root:
            self.mostrar_favoritos(root.izquierda)
            self.mostrar_favoritos(root.derecha)
            print(f"{root.url} - {root.nombre} - {root.fecha}")

    # Eliminar un favorito del árbol
    def eliminar_favorito(self, root, url):
        if root is None:
            return root

        if url < root.url:
            root.izquierda = self.eliminar_favorito(root.izquierda, url)
        elif url > root.url:
            root.derecha = self.eliminar_favorito(root.derecha, url)
        else:
            if root.izquierda is None:
                return root.derecha
            elif root.derecha is None:
                return root.izquierda

            temp = self.obtener_minimo(root.derecha)
            root.url = temp.url
            root.nombre = temp.nombre
            root.fecha = temp.fecha
            root.derecha = self.eliminar_favorito(root.derecha, temp.url)

        root.altura = 1 + max(self.altura(root.izquierda), self.altura(root.derecha))
        balance = self.obtener_balance(root)

        if balance > 1 and self.obtener_balance(root.izquierda) >= 0:
            return self.rotacion_derecha(root)

        if balance < -1 and self.obtener_balance(root.derecha) <= 0:
            return self.rotacion_izquierda(root)

        if balance > 1 and self.obtener_balance(root.izquierda) < 0:
            root.izquierda = self.rotacion_izquierda(root.izquierda)
            return self.rotacion_derecha(root)

        if balance < -1 and self.obtener_balance(root.derecha) > 0:
            root.derecha = self.rotacion_derecha(root.derecha)
            return self.rotacion_izquierda(root)

        return root

    def obtener_minimo(self, root):
        current = root
        while current.izquierda is not None:
            current = current.izquierda
        return current

# Funciones para manejar el archivo CSV
def cargar_favoritos():
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

def guardar_favoritos(favoritos):
    with open('favoritos.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for url, nombre, fecha in favoritos:
            writer.writerow([url, nombre, fecha])
    print(f"Se han guardado {len(favoritos)} favoritos en el archivo favoritos.csv.")

# Funciones para manejar los comandos
def agregar_favorito_comando(arbol, favoritos, url, nombre):
    if not url or not nombre:
        print("Error: La URL o el nombre del sitio no pueden estar vacíos.")
        return
    arbol.agregar_favorito(url, nombre)
    favoritos.append((url, nombre, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    guardar_favoritos(favoritos)
    print(f"Favorito agregado: {url}")

def eliminar_favorito_comando(arbol, favoritos, url):
    print(f"Eliminando el favorito con URL: {url}")
    arbol.raiz = arbol.eliminar_favorito(arbol.raiz, url)
    favoritos = [f for f in favoritos if f[0] != url]
    guardar_favoritos(favoritos)
    print(f"Favorito eliminado: {url}")

def buscar_favorito_comando(arbol, url):
    favorito = arbol.buscar_favorito(arbol.raiz, url)
    if favorito:
        print(f"Favorito encontrado: {favorito.url} - {favorito.nombre} - {favorito.fecha}")
    else:
        print("Favorito no encontrado.")

def mostrar_favoritos_comando(arbol):
    print("Favoritos:")
    arbol.mostrar_favoritos(arbol.raiz)

# Función principal para ejecutar los comandos
def main():
    arbol = ArbolAVL()
    favoritos = cargar_favoritos()

    # Agregar favoritos iniciales al árbol
    for url, nombre, fecha in favoritos:
        arbol.agregar_favorito(url, nombre)

    while True:
        comando = input("Ingrese un comando: ").strip().lower()
        print(f"Comando recibido: {comando}")
        
        if comando.startswith("agregar_favorito"):
            # Verificamos si el comando tiene la URL
            partes = comando.split(" ")
            if len(partes) < 2:
                print("Error: Se requiere una URL después del comando 'agregar_favorito'.")
                continue  # Volver al inicio del ciclo

            url = partes[1]
            nombre = input("Ingrese el nombre del sitio: ")
            agregar_favorito_comando(arbol, favoritos, url, nombre)
        
        elif comando.startswith("eliminar_favorito"):
            # Verificamos si el comando tiene la URL
            partes = comando.split(" ")
            if len(partes) < 2:
                print("Error: Se requiere una URL después del comando 'eliminar_favorito'.")
                continue  # Volver al inicio del ciclo

            url = partes[1]
            eliminar_favorito_comando(arbol, favoritos, url)
        
        elif comando.startswith("buscar_favorito"):
            # Verificamos si el comando tiene la URL
            partes = comando.split(" ")
            if len(partes) < 2:
                print("Error: Se requiere una URL después del comando 'buscar_favorito'.")
                continue  # Volver al inicio del ciclo

            url = partes[1]
            buscar_favorito_comando(arbol, url)
        
        elif comando == "mostrar_favoritos":
            mostrar_favoritos_comando(arbol)
        
        elif comando == "salir":
            print("Saliendo...")
            break  # Salir del ciclo y terminar el programa

        else:
            print("Comando no reconocido. Intenta de nuevo.")


if __name__ == "__main__":
    main()
