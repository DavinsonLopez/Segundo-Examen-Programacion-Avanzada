import io
import time
import random
import contextlib
import matplotlib.pyplot as plt
import tracemalloc
import algoritmos


TIEMPO_OUT = 3.0            # Limite de 3 segundos acumulados por variante
REPETICIONES = 5            # Veces que se promedia cada medicion
TAMANIOS = [10 ** 2, 10 ** 3, 10 ** 4, 10 ** 5]


def generar_peor_caso(n):
    """Peor caso: A con pares y B con impares (disjuntos) + shuffle."""
    A = [2 * i for i in range(n)]       # Multiplos de 2: pares
    B = [2 * i + 1 for i in range(n)]   # Multiplos de 2 mas 1: impares

    random.shuffle(A)
    random.shuffle(B)

    return A, B


def medir_tiempo(funcion, A, B, repeticiones=REPETICIONES):
    """Tiempo promedio de 'funcion(A, B)' usando time.perf_counter()."""
    total = 0.0

    for _ in range(repeticiones):
        inicio = time.perf_counter()
        funcion(A, B)
        total += time.perf_counter() - inicio

    return total / repeticiones


def experimento_peor_caso():
    """Tabla de tiempos con timeout: si acumula >3s, imprime TIMEOUT."""
    variantes = {
        'Variante A': algoritmos.interseccion_variante_a,
        'Variante B': algoritmos.interseccion_variante_b,
        'Variante C': algoritmos.interseccion_variante_c,
    }

    tiempo_acumulado = {nombre: 0.0 for nombre in variantes}

    # Datos que se usaran en la grafica log-log
    xs = {nombre: [] for nombre in variantes}
    ys = {nombre: [] for nombre in variantes}

    # Cabecera de la tabla
    encabezado = '{:>8}'.format('N')
    for nombre in variantes:
        encabezado += '{:>16}'.format(nombre)
    print(encabezado)
    print('-' * len(encabezado))

    # Mediciones por cada tamano de N
    for n in TAMANIOS:
        A, B = generar_peor_caso(n)

        fila = '{:>8}'.format(n)

        for nombre, funcion in variantes.items():
            # Si la variante ya supero el limite, no se vuelve a ejecutar
            if tiempo_acumulado[nombre] >= TIEMPO_OUT:
                fila += '{:>16}'.format('TIMEOUT')
                continue

            promedio = medir_tiempo(funcion, A, B)

            # Guardar el tiempo acumulado (total de las repeticiones)
            tiempo_acumulado[nombre] += promedio * REPETICIONES

            fila += '{:>16.6f}'.format(promedio)

            # Guardar el punto que se dibujara en la grafica log-log
            xs[nombre].append(n)
            ys[nombre].append(promedio)

        print(fila)

    return xs, ys


def graficar_loglog(xs, ys):
    """Grafica log-log con etiquetas, titulo, leyenda y grilla punteada."""
    plt.figure(figsize=(8, 6), num='Comparacion de complejidad algoritmica')

    plt.loglog(xs['Variante A'], ys['Variante A'], 'o-',
               label='Variante A (O(N^2))')
    plt.loglog(xs['Variante B'], ys['Variante B'], 's-',
               label='Variante B (O(N log N))')
    plt.loglog(xs['Variante C'], ys['Variante C'], '^-',
               label='Variante C (O(N))')

    plt.xlabel('Tamano de la entrada (N)')
    plt.ylabel('Tiempo promedio (segundos)')
    plt.title('Comparacion de complejidad computacional de las tres variantes (log-log)')
    plt.grid(True, linestyle=':', linewidth=0.7)
    plt.legend()


def buscar_n_estrella():
    """N* exacto: desde N=10 de 1 en 1 hasta que Variante B sea mas rapida."""
    print('Buscando N* (N incrementa de 1 en 1 desde 10)...')

    n = 10
    while True:
        A, B = generar_peor_caso(n)

        tiempo_a = medir_tiempo(algoritmos.interseccion_variante_a, A, B)
        tiempo_b = medir_tiempo(algoritmos.interseccion_variante_b, A, B)

        if tiempo_b < tiempo_a:
            print()
            print('N* encontrado: N = {}'.format(n))
            print('  Variante A (O(N^2)): {:.8f} segundos'.format(tiempo_a))
            print('  Variante B (O(N log N)): {:.8f} segundos'.format(tiempo_b))
            print('A partir de este tamano, la busqueda binaria supera a la fuerza bruta.')
            return n

        n += 1


def perfil_memoria():
    """Pico de RAM (MB) de las Variantes B y C con tracemalloc, N=100000."""
    n = 100000
    print()
    print('Espacio en RAM que usan los algoritmos (tracemalloc) - N = {}'.format(n))
    A, B = generar_peor_caso(n)

    # Variante B
    tracemalloc.start()
    algoritmos.interseccion_variante_b(A, B)
    _, pico_b = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    mb_b = pico_b / (1024.0 * 1024.0)

    # Variante C
    tracemalloc.start()
    algoritmos.interseccion_variante_c(A, B)
    _, pico_c = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    mb_c = pico_c / (1024.0 * 1024.0)

    print('  Variante B: {:.2f} MB como maximo'.format(mb_b))
    print('  Variante C: {:.2f} MB como maximo'.format(mb_c))

    print()
    print('JUSTIFICACION (mas memoria a cambio de mas velocidad):')
    print('La Variante C es mas rapida porque comprobar si un numero esta en')
    print('un conjunto es casi inmediato. Pero para lograrlo, el conjunto')
    print('guarda datos extra de organizacion, por lo que ocupa MAS espacio')
    print('en RAM que la lista ordenada que usa la Variante B. En resumen:')
    print('la Variante C gasta mas memoria para ganar velocidad.')


def graficar_reporte(texto):
    """Abre una ventana aparte con el reporte, ajustada al tamano del texto."""
    lineas = texto.split('\n')
    ancho_max = 0
    for linea in lineas:
        if len(linea) > ancho_max:
            ancho_max = len(linea)

   
    fuente = 9
    ancho_car = 0.6 * fuente / 72.0     # Ancho de cada caracter
    alto_linea = 1.3 * fuente / 72.0    # Alto de cada linea 

    ancho_pag = ancho_car * ancho_max + 1.0
    alto_pag = alto_linea * len(lineas) + 0.8

    figura = plt.figure(figsize=(ancho_pag, alto_pag), num='Reporte de resultados')
    ejes = figura.add_subplot(111)
    ejes.axis('off')
    ejes.text(0.02, 0.98, texto, fontsize=fuente, family='monospace',
              verticalalignment='top', transform=ejes.transAxes)


def run_experimentos():
    """Ejecuta las secciones e imprime sus resultados en consola."""
    print('=' * 62)
    print('EVALUACION 2 - ANALISIS DE ALGORITMOS, VELOCIDAD Y MEMORIA')
    print('=' * 62)

    print()
    print('[1] Peor caso (arreglos sin numeros en comun): tabla de tiempos')
    xs, ys = experimento_peor_caso()

    print()
    print('[2] Grafica logarítmica de los tiempos (en la otra ventana)')
    graficar_loglog(xs, ys)

    print()
    print('[3] Busqueda del punto exacto donde B supera a A')
    buscar_n_estrella()

    print()
    print('[4] Cuanto espacio en RAM usan los algoritmos')
    perfil_memoria()


def main():
    # Captura todo lo que se imprime en consola
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        run_experimentos()

    texto = buffer.getvalue()

    # Muestra la grafica log-log y el reporte en ventanas separadas
    graficar_reporte(texto)
    plt.show()


if __name__ == '__main__':
    main()