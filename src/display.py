# display.py
# Funciones de presentación en consola.

from src.item import LRItem

ANCHO = 58
SEP   = "─" * ANCHO
SEP2  = "═" * ANCHO


def encabezado(titulo: str) -> None:
    print()
    print(SEP2)
    print(f"  {titulo}")
    print(SEP2)


def seccion(titulo: str) -> None:
    print()
    print(SEP)
    print(f"  {titulo}")
    print(SEP)


def mostrar_gramatica(grammar) -> None:
    seccion("GRAMÁTICA INGRESADA")
    print(f"  Símbolo inicial : {grammar.start_symbol}")
    print(f"  No-terminales   : {', '.join(sorted(grammar.non_terminals))}")
    print(f"  Terminales      : {', '.join(sorted(grammar.terminals))}")
    print()
    print("  Producciones:")
    for i, prod in enumerate(grammar.productions, 1):
        print(f"    {i:2}. {prod}")


def mostrar_items_entrada(items: set[LRItem]) -> None:
    seccion("ÍTEMS DE ENTRADA")
    if not items:
        print("  (conjunto vacío)")
        return
    for item in items:
        nota = "  ← ya es ítem de reducción" if item.is_complete else ""
        print(f"  {item}{nota}")


def mostrar_traza(traza: list[str]) -> None:
    seccion("PROCESO PASO A PASO")
    for linea in traza:
        print(linea)


def mostrar_resultado(cerradura: list[LRItem]) -> None:
    seccion("RESULTADO FINAL — CERRADURA COMPLETA")
    normales    = [it for it in cerradura if not it.is_complete]
    reducciones = [it for it in cerradura if it.is_complete]

    print(f"  Total de ítems: {len(cerradura)}")
    print()

    if normales:
        print("  Ítems normales (punto NO al final):")
        for item in normales:
            print(f"    {item}")

    if reducciones:
        print()
        print("  Ítems de REDUCCIÓN (punto al final):")
        for item in reducciones:
            print(f"    {item}   [REDUCE]")

    print()
    print(SEP)


def mostrar_menu_principal() -> None:
    encabezado("CALCULADORA DE CERRADURA LR(0)")
    print()
    print("  ¿Qué gramática desea usar?")
    print()
    print("  [1]  Gramática 1  :  S → SS+ | SS* | a")
    print("  [2]  Gramática 2  :  S → (S) | ε")
    print("  [3]  Gramática 3  :  S → L,  L → aL | a")
    print("  [4]  Gramática de clase  :  E → E+T | T,  T → T*F | F,  F → (E) | id")
    print("  [5]  Ingresar gramática personalizada")
    print("  [0]  Salir")
    print()
    print(SEP)


def mostrar_menu_items(grammar) -> list:
    seccion("SELECCIÓN DE ÍTEMS DE ENTRADA")
    print("  Seleccione el ítem inicial (o varios separados por coma):")
    print()

    todos_items: list[LRItem] = []
    for prod in grammar.productions:
        for pos in range(len(prod.body) + 1):
            todos_items.append(LRItem(prod, pos))

    for i, item in enumerate(todos_items, 1):
        nota = "  [reducción]" if item.is_complete else ""
        print(f"  [{i:2}]  {item}{nota}")

    print()
    print(f"  Ingrese número(s) de ítem [1-{len(todos_items)}], separados por coma:")
    return todos_items
