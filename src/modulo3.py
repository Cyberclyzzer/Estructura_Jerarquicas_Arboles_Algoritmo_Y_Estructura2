import csv
from datetime import datetime

class Nodo:
    def __init__(self, url):
        self.url = url
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.izquierda = None
        self.derecha = None

    def guardar(self):
        with open('src/busquedas.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.url, self.fecha])

class ArbolBB:
    def __init__(self):
        self.raiz = None

    def insertar(self, url):
        if self.raiz is None:
            self.raiz = Nodo(url)
            self.raiz.guardar()
        else:
            self._insertar_rec(self.raiz, url)

    def _insertar_rec(self, nodo, url):
        if url < nodo.url:
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(url)
                nodo.izquierda.guardar()
            else:
                self._insertar_rec(nodo.izquierda, url)
        else:
            if nodo.derecha is None:
                nodo.derecha = Nodo(url)
                nodo.derecha.guardar()
            else:
                self._insertar_rec(nodo.derecha, url)

    def buscar_clave(self, clave):
        resultados = []
        self.buscar_palabra_clave(self.raiz, clave, resultados)
        for nodo in resultados:
            print(f"{nodo.url} - {nodo.fecha}")
    
    def buscar_palabra_clave(self, nodo, clave, resultados):
        if nodo is not None:
            self.buscar_palabra_clave(nodo.izquierda, clave, resultados)
            if clave in nodo.url:
                resultados.append(nodo)
            self.buscar_palabra_clave(nodo.derecha, clave, resultados)

    def eliminar_clave(self, palabra_clave):
        self.raiz = self._eliminar_nodos_con_palabra_clave(self.raiz, palabra_clave)

    def _eliminar_nodos_con_palabra_clave(self, nodo, palabra_clave):
        if nodo is None:
            return None

        nodo.izquierda = self._eliminar_nodos_con_palabra_clave(nodo.izquierda, palabra_clave)
        nodo.derecha = self._eliminar_nodos_con_palabra_clave(nodo.derecha, palabra_clave)

        if palabra_clave in nodo.url:
            return self._fusionar(nodo.izquierda, nodo.derecha)

        return nodo

    def eliminar_fecha(self, fecha_limite):
        self.raiz = self._eliminar_posteriores_rec(self.raiz, fecha_limite)

    def _eliminar_posteriores_rec(self, nodo, fecha_limite):
        if nodo is None:
            return None

        nodo.izquierda = self._eliminar_posteriores_rec(nodo.izquierda, fecha_limite)
        nodo.derecha = self._eliminar_posteriores_rec(nodo.derecha, fecha_limite)

        if nodo.fecha > fecha_limite:
            return self._fusionar(nodo.izquierda, nodo.derecha)

        return nodo

    def _fusionar(self, izq, der):
        if izq is None:
            return der
        if der is None:
            return izq

        derecho_mas_izquierda = der
        while derecho_mas_izquierda.izquierda is not None:
            derecho_mas_izquierda = derecho_mas_izquierda.izquierda

        derecho_mas_izquierda.izquierda = izq
        return der

    def inorder(self, nodo):
        if nodo is not None:
            self.inorder(nodo.izquierda)
            print(f"{nodo.url} - {nodo.fecha}")
            self.inorder(nodo.derecha)
        else:
            return
        
    def cargar(self, array):
        nuevo = Nodo(array[0])
        nuevo.fecha = array[1]
        
        if self.raiz is None:
            self.raiz = nuevo
        else:
            self._cargar_rec(self.raiz, nuevo)

    def _cargar_rec(self, nodo, nuevo):
        if nuevo.url < nodo.url:
            if nodo.izquierda is None:
                nodo.izquierda = nuevo
            else:
                self._cargar_rec(nodo.izquierda, nuevo)
        else:
            if nodo.derecha is None:
                nodo.derecha = nuevo
            else:
                self._cargar_rec(nodo.derecha, nuevo)