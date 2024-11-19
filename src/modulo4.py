import datetime

class NodoBTree:
    def __init__(self, orden):
        self.orden = orden  # Número máximo de claves que puede almacenar el nodo
        self.claves = []    # Lista de URLs (clave)
        self.valores = []   # Lista de contenidos HTML (valor)
        self.hijos = []     # Punteros a los hijos
        self.es_hoja = True # Indicador de si el nodo es hoja

class BTreeCache:
    def __init__(self, orden=4):
        self.orden = orden  # Orden del B-tree
        self.raiz = NodoBTree(orden)  # La raíz comienza como un nodo vacío

    # Insertar una URL y su contenido en el árbol
    def insertar(self, url, contenido):
        if len(self.raiz.claves) == 2 * self.orden - 1:
            # Si la raíz está llena, dividirla
            nueva_raiz = NodoBTree(self.orden)
            nueva_raiz.hijos.append(self.raiz)
            self._dividir_nodo(nueva_raiz, 0)
            self.raiz = nueva_raiz

        self._insertar_en_nodo(self.raiz, url, contenido)

    # Función recursiva para insertar en el nodo adecuado
    def _insertar_en_nodo(self, nodo, url, contenido):
        if nodo.es_hoja:
            # Si el nodo es hoja, insertamos la URL y contenido
            self._insertar_en_hoja(nodo, url, contenido)
        else:
            # Si el nodo no es hoja, encontramos el hijo adecuado
            i = len(nodo.claves) - 1
            while i >= 0 and url < nodo.claves[i]:
                i -= 1
            i += 1
            # Recursión en el hijo
            if len(nodo.hijos[i].claves) == 2 * self.orden - 1:
                self._dividir_nodo(nodo, i)
                if url > nodo.claves[i]:
                    i += 1
            self._insertar_en_nodo(nodo.hijos[i], url, contenido)

    # Insertar en un nodo hoja
    def _insertar_en_hoja(self, nodo, url, contenido):
        nodo.claves.append(url)
        nodo.valores.append(contenido)
        self._ordenar_claves(nodo)

    # Ordenar las claves y valores en un nodo
    def _ordenar_claves(self, nodo):
        # Ordenamos las claves (URLs) y sus contenidos asociados
        for i in range(len(nodo.claves) - 1):
            for j in range(i + 1, len(nodo.claves)):
                if nodo.claves[i] > nodo.claves[j]:
                    nodo.claves[i], nodo.claves[j] = nodo.claves[j], nodo.claves[i]
                    nodo.valores[i], nodo.valores[j] = nodo.valores[j], nodo.valores[i]

    # Dividir un nodo cuando está lleno
    def _dividir_nodo(self, nodo_padre, indice_hijo):
        hijo = nodo_padre.hijos[indice_hijo]
        medio = len(hijo.claves) // 2
        clave_prom = hijo.claves[medio]

        # Crear el nuevo nodo que será el hijo derecho
        nuevo_hijo = NodoBTree(self.orden)
        nuevo_hijo.claves = hijo.claves[medio + 1:]
        nuevo_hijo.valores = hijo.valores[medio + 1:]
        hijo.claves = hijo.claves[:medio]
        hijo.valores = hijo.valores[:medio]

        if not hijo.es_hoja:
            nuevo_hijo.hijos = hijo.hijos[medio + 1:]
            hijo.hijos = hijo.hijos[:medio + 1]
            nuevo_hijo.es_hoja = False

        # Insertar la clave promovida en el nodo padre
        nodo_padre.claves.insert(indice_hijo, clave_prom)
        nodo_padre.valores.insert(indice_hijo, hijo.valores[medio])
        nodo_padre.hijos.insert(indice_hijo + 1, nuevo_hijo)

    # Buscar una URL en el B-tree
    def buscar(self, url):
        return self._buscar_en_nodo(self.raiz, url)

    # Función recursiva para buscar la URL en un nodo
    def _buscar_en_nodo(self, nodo, url):
        i = 0
        while i < len(nodo.claves) and url > nodo.claves[i]:
            i += 1
        if i < len(nodo.claves) and url == nodo.claves[i]:
            return nodo.valores[i]
        if nodo.es_hoja:
            return None
        return self._buscar_en_nodo(nodo.hijos[i], url)

    # Eliminar por URL
    def eliminar_por_url(self, url):
        self.raiz = self._eliminar_por_url(self.raiz, url)

    # Función recursiva para eliminar por URL
    def _eliminar_por_url(self, nodo, url):
        if nodo.es_hoja:
            if url in nodo.claves:
                index = nodo.claves.index(url)
                nodo.claves.pop(index)
                nodo.valores.pop(index)
            return nodo
        else:
            i = 0
            while i < len(nodo.claves) and url > nodo.claves[i]:
                i += 1
            if i < len(nodo.claves) and url == nodo.claves[i]:
                nodo.claves.pop(i)
                nodo.valores.pop(i)
            return nodo

    # Eliminar por fecha
    def eliminar_por_fecha(self, fecha):
        self.raiz = self._eliminar_por_fecha(self.raiz, fecha)

    # Función recursiva para eliminar por fecha
    def _eliminar_por_fecha(self, nodo, fecha):
        if nodo.es_hoja:
            for i in range(len(nodo.claves)):
                if nodo.valores[i].fecha_acceso > fecha:
                    nodo.claves.pop(i)
                    nodo.valores.pop(i)
        else:
            for hijo in nodo.hijos:
                self._eliminar_por_fecha(hijo, fecha)
        return nodo

        # Comando para agregar caché
    def agregar_cache(self, url, contenido):
        self.insertar(url, contenido)

    # Comando para obtener caché
    def obtener_cache(self, url):
        contenido = self.buscar(url)
        if contenido:
            return contenido
        return "No encontrado en caché"

    # Comando para vaciar caché por URL o por fecha
    def vaciar_cache(self, url=None, fecha=None):
        if url:
            self.eliminar_por_url(url)
        elif fecha:
            self.eliminar_por_fecha(fecha)

def main():
    cache = BTreeCache(orden=4)  # Crear la instancia del caché

    while True:
        # Leer el comando del usuario
        comando = input("Ingrese un comando (agregar_cache, obtener_cache, vaciar_cache, salir): ")

        if comando.startswith("agregar_cache"):
            _, url, contenido = comando.split(" ", 2)
            cache.agregar_cache(url, contenido)
            print(f"Contenido agregado a la caché para {url}")

        elif comando.startswith("obtener_cache"):
            _, url = comando.split(" ", 1)
            contenido = cache.obtener_cache(url)
            print(f"Contenido de {url}: {contenido}")

        elif comando.startswith("vaciar_cache"):
            args = comando.split(" ")
            if "--url" in args:
                url = args[args.index("--url") + 1]
                cache.vaciar_cache(url=url)
                print(f"Entrada de caché eliminada para {url}")
            elif "--fecha" in args:
                fecha_str = args[args.index("--fecha") + 1]
                fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
                cache.vaciar_cache(fecha=fecha)
                print(f"Entradas de caché eliminadas posteriores a {fecha_str}")
            else:
                print("Parámetros incorrectos para vaciar_cache.")

        elif comando == "salir":
            print("Saliendo del programa...")
            break
        else:
            print("Comando no reconocido. Intente de nuevo.")

# Ejecutar la función para iniciar la terminal
if __name__ == "__main__":
    main()