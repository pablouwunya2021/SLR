# main.py
# Punto de entrada. Muestra el menú, carga la gramática y calcula la cerradura.
#
# Para ejecutar:
#     python main.py

from src.grammar import Grammar
from src.item import LRItem
from src.closure import cerradura_con_traza
from src.display import (
    mostrar_menu_principal,
    mostrar_menu_items,
    mostrar_gramatica,
    mostrar_items_entrada,
    mostrar_traza,
    mostrar_resultado,
    seccion,
    SEP,
)


def gramatica_1() -> Grammar:
    # S → SS+ | SS* | a  (producción aumentada S' → S)
    g = Grammar("S'")
    g.add_production("S'", ["S"])
    g.add_production("S",  ["S", "S", "+"])
    g.add_production("S",  ["S", "S", "*"])
    g.add_production("S",  ["a"])
    return g


def gramatica_2() -> Grammar:
    # S → (S) | ε  (producción aumentada S' → S)
    g = Grammar("S'")
    g.add_production("S'", ["S"])
    g.add_production("S",  ["(", "S", ")"])
    g.add_production("S",  [])
    return g


def gramatica_3() -> Grammar:
    # S → L,  L → aL | a  (producción aumentada S' → S)
    g = Grammar("S'")
    g.add_production("S'", ["S"])
    g.add_production("S",  ["L"])
    g.add_production("L",  ["a", "L"])
    g.add_production("L",  ["a"])
    return g


def gramatica_clase() -> Grammar:
    # E → E+T | T,  T → T*F | F,  F → (E) | id
    # Ejemplo de cadena: id + (id * id)
    g = Grammar("E'")
    g.add_production("E'", ["E"])
    g.add_production("E",  ["E", "+", "T"])
    g.add_production("E",  ["T"])
    g.add_production("T",  ["T", "*", "F"])
    g.add_production("T",  ["F"])
    g.add_production("F",  ["(", "E", ")"])
    g.add_production("F",  ["id"])
    return g


def ingresar_gramatica_personalizada() -> Grammar:
    seccion("INGRESO DE GRAMÁTICA PERSONALIZADA")
    print("  Formato:  A -> X Y z   (separe símbolos con espacios)")
    print("           'epsilon' para producción vacía (A -> epsilon)")
    print("  Escriba 'fin' cuando termine.")
    print()

    producciones_raw: list[tuple[str, list[str]]] = []
    simbolo_inicial: str | None = None

    while True:
        linea = input("  Producción: ").strip()

        if linea.lower() == "fin":
            if not producciones_raw:
                print("  [!] Debe ingresar al menos una producción.")
                continue
            break

        if "->" not in linea:
            print("  [!] Formato incorrecto. Use: A -> X Y z")
            continue

        partes    = linea.split("->", maxsplit=1)
        head      = partes[0].strip()
        body_str  = partes[1].strip()
        body      = [] if body_str.lower() in ("epsilon", "eps", "e", "ε", "") else body_str.split()

        producciones_raw.append((head, body))

        if simbolo_inicial is None:
            simbolo_inicial = head

    g = Grammar(f"{simbolo_inicial}'")
    g.add_production(f"{simbolo_inicial}'", [simbolo_inicial])
    for head, body in producciones_raw:
        g.add_production(head, body)

    return g


def seleccionar_items(grammar: Grammar) -> set[LRItem]:
    todos_items = mostrar_menu_items(grammar)

    while True:
        entrada = input("  Su elección: ").strip()
        try:
            indices = [int(x.strip()) for x in entrada.split(",")]
            seleccionados = set()
            for idx in indices:
                if 1 <= idx <= len(todos_items):
                    seleccionados.add(todos_items[idx - 1])
                else:
                    raise ValueError(f"Índice {idx} fuera de rango.")
            return seleccionados
        except ValueError as e:
            print(f"  [!] Entrada inválida: {e}. Intente de nuevo.")


def calcular_y_mostrar(grammar: Grammar) -> None:
    mostrar_gramatica(grammar)
    items_entrada = seleccionar_items(grammar)
    mostrar_items_entrada(items_entrada)
    resultado, traza = cerradura_con_traza(items_entrada, grammar)
    mostrar_traza(traza)
    mostrar_resultado(resultado)


def main() -> None:
    while True:
        mostrar_menu_principal()
        opcion = input("  Su opción: ").strip()

        if opcion == "0":
            print()
            print("  Hasta luego.")
            print()
            break
        elif opcion == "1":
            calcular_y_mostrar(gramatica_1())
        elif opcion == "2":
            calcular_y_mostrar(gramatica_2())
        elif opcion == "3":
            calcular_y_mostrar(gramatica_3())
        elif opcion == "4":
            calcular_y_mostrar(gramatica_clase())
        elif opcion == "5":
            try:
                grammar = ingresar_gramatica_personalizada()
                calcular_y_mostrar(grammar)
            except KeyboardInterrupt:
                print("\n  [!] Ingreso cancelado.")
        else:
            print("  [!] Opción no válida. Elija entre 0 y 5.")

        print()
        input("  Presione ENTER para continuar...")


if __name__ == "__main__":
    main()
