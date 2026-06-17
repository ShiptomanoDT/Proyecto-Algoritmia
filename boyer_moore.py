# ============================================================
#  Algoritmo Boyer-Moore
#  Regla del caracter malo + Regla del sufijo bueno
#  Autor: Waldo Gustavo Davalos Terceros - Santiago Nahuel Mora Paca
#  Materia: INF3641 'A'
# ============================================================

def precomputar_caracter_malo(patron, m):
    """Tabla de caracter malo: ultimo indice de cada caracter en el patron."""
    tabla_cm = {}
    for j in range(m):
        tabla_cm[patron[j]] = j
    return tabla_cm


def calcular_sufijos(patron, m):
    """Calcula el arreglo de sufijos para la regla del sufijo bueno."""
    sufijos = [0] * m
    sufijos[m - 1] = m
    g = m - 1
    f = 0
    for i in range(m - 2, -1, -1):
        if i > g and sufijos[i + m - 1 - f] < i - g:
            sufijos[i] = sufijos[i + m - 1 - f]
        else:
            if i < g:
                g = i
            f = i
            while g >= 0 and patron[g] == patron[g + m - 1 - f]:
                g -= 1
            sufijos[i] = f - g
    return sufijos


def precomputar_sufijo_bueno(patron, m):
    """Tabla de sufijo bueno a partir del arreglo de sufijos."""
    tabla_sg = [m] * (m + 1)
    sufijos = calcular_sufijos(patron, m)
    for i in range(m - 1, -1, -1):
        if sufijos[i] == i + 1:
            for j in range(m - 1 - i):
                if tabla_sg[j] == m:
                    tabla_sg[j] = m - 1 - i
    for i in range(m - 1):
        tabla_sg[m - 1 - sufijos[i]] = m - 1 - i
    return tabla_sg


def boyer_moore(texto, patron):
    """
    Busqueda Boyer-Moore.
    Retorna lista de indices donde se encontro el patron.
    """
    n = len(texto)
    m = len(patron)
    if m == 0 or m > n:
        return []

    tabla_cm = precomputar_caracter_malo(patron, m)
    tabla_sg = precomputar_sufijo_bueno(patron, m)

    ocurrencias = []
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and patron[j] == texto[s + j]:
            j -= 1
        if j < 0:
            ocurrencias.append(s)
            s += tabla_sg[0]
        else:
            cm = tabla_cm.get(texto[s + j], -1)
            desp_cm = max(1, j - cm)
            #desp_sg = tabla_sg[j + 1]
            #s += max(desp_cm, desp_sg)
            s += desp_cm
    return ocurrencias

with open("./textos/La Odisea by Homer.txt", encoding="utf-8") as f:
    texto = f.read()

patron = "sed"

bm = set(boyer_moore(texto, patron))

i = 0
python = []

while True:
    i = texto.find(patron, i)

    if i == -1:
        break

    python.append(i)

    i += 1

faltan = sorted(set(python) - bm)
extras = sorted(bm - set(python))

print("Coincidencias Boyer-Moore:", len(bm))
print("Coincidencias Python:", len(python))
print()

print("¿Son exactamente iguales?:", bm == set(python))
print()

print("Coincidencias faltantes:", len(faltan))
print(faltan[:10])  # muestra las primeras 10

print()

print("Coincidencias extra:", len(extras))
print(extras[:10])  # muestra las primeras 10
