# Interseccion de dos arreglos en tres variantes con distinta complejidad.
def busqueda_binaria(arr, objetivo):
    """Busqueda binaria tradicional. O(log N)."""
    inicio = 0
    fin = len(arr) - 1

    while inicio <= fin:
        medio = (inicio + fin) // 2

        if arr[medio] == objetivo:
            return True
        elif arr[medio] < objetivo:
            inicio = medio + 1
        else:
            fin = medio - 1

    return False


def interseccion_variante_a(A, B):
    """Fuerza bruta, dos ciclos anidados con break. O(N^2)."""
    resultado = []

    for x in A:
        for y in B:
            if x == y:
                resultado.append(x)
                break

    return resultado


def interseccion_variante_b(A, B):
    """Ordena B y aplica busqueda binaria por elemento. O(N log N)."""
    resultado = []
    B_ordenado = sorted(B)

    for x in A:
        if busqueda_binaria(B_ordenado, x):
            resultado.append(x)

    return resultado


def interseccion_variante_c(A, B):
    """Convierte B en un set y consulta pertenencia. O(N)."""
    resultado = []
    B_set = set(B)

    for x in A:
        if x in B_set:
            resultado.append(x)

    return resultado