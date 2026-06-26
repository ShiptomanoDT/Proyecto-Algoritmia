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

def preprocess_strong_suffix(shift, bpos, patron, m):
    i = m
    j = m + 1
    bpos[i] = j

    while i > 0:
        while j <= m and patron[i - 1] != patron[j - 1]:
            if shift[j] == 0:
                shift[j] = j - i

            j = bpos[j]

        i -= 1
        j -= 1
        bpos[i] = j


def preprocess_case2(shift, bpos, m):
    j = bpos[0]

    for i in range(m + 1):

        if shift[i] == 0:
            shift[i] = j

        if i == j:
            j = bpos[j]


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
    
    shift = [0] * (m + 1)
    bpos = [0] * (m + 1)

    preprocess_strong_suffix(shift, bpos, patron, m)
    preprocess_case2(shift, bpos, m)

    ocurrencias = []
    s = 0

    while s <= n - m:
        j = m - 1
        while j >= 0 and patron[j] == texto[s + j]:
            j -= 1
        if j < 0:
            ocurrencias.append(s)
            s += shift[0]
        else:
            cm = tabla_cm.get(texto[s + j], -1)

            desp_cm = max(1, j - cm)
            desp_sg = shift[j + 1]

            s += max(desp_cm, desp_sg)
    return ocurrencias
