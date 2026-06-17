import sys
import time
from boyer_moore import boyer_moore

REPETICIONES = 10


def medir(texto, patron, reps=REPETICIONES):
    tiempos = []

    for _ in range(reps):
        inicio = time.perf_counter()
        ocurrencias = boyer_moore(texto, patron)
        fin = time.perf_counter()

        tiempos.append(fin - inicio)

    return ocurrencias, tiempos


def main():
    if len(sys.argv) != 3:
        print("Uso:")
        print("  python buscar_archivo.py <archivo> <patron>")
        sys.exit(1)

    archivo = sys.argv[1]
    patron = sys.argv[2]

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            texto = f.read()
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{archivo}'.")
        sys.exit(1)

    ocurrencias, tiempos = medir(texto, patron)

    promedio = sum(tiempos) / len(tiempos)
    minimo = min(tiempos)
    maximo = max(tiempos)

    velocidad = len(texto) / promedio if promedio > 0 else 0

    print("=" * 50)
    print("Demostración Boyer-Moore")
    print("=" * 50)
    print()
    print(f"Archivo analizado : {archivo}")
    print(f"Patrón buscado (P): {patron}")
    print()
    print(f"Tamaño del texto (n) : {len(texto):,} caracteres")
    print(f"Longitud patrón (m = |P|): {len(patron)} caracteres")
    print()
    print(f"Coincidencias encontradas : {len(ocurrencias)}")

    if ocurrencias:
        print("\nPrimeras coincidencias:")

        for pos in ocurrencias[:10]:
            linea = texto.count('\n', 0, pos) + 1

            print(f"Posición: {pos:<10}"
                  f"Línea: {linea}")

        if len(ocurrencias) > 10:
            print("...")

    print()
    print(f"Tiempo promedio ({REPETICIONES} ejecuciones): {promedio:.6f} s")
    print(f"Tiempo mínimo                 : {minimo:.6f} s")
    print(f"Tiempo máximo                 : {maximo:.6f} s")
    print()
    print(f"Velocidad aproximada          : {velocidad:,.0f} caracteres/s")

    print("=" * 50)


if __name__ == "__main__":
    main()
