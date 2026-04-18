

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.grammar import Grammar, Production
from src.item import LRItem
from src.closure import cerradura


# ─── Helpers ─────────────────────────────────────────────────────────────────

def items_como_strings(items: list[LRItem]) -> set[str]:
    """Convierte una lista de ítems a un set de strings para comparar fácilmente."""
    return {repr(it) for it in items}


# ─── Tests ───────────────────────────────────────────────────────────────────

def test_gramatica_1_estado_inicial():

    g = Grammar("S'")
    g.add_production("S'", ["S"])
    g.add_production("S",  ["S", "S", "+"])
    g.add_production("S",  ["S", "S", "*"])
    g.add_production("S",  ["a"])

    item_inicial = LRItem(g.productions_for("S'")[0], 0)
    resultado = cerradura({item_inicial}, g)
    resultado_str = items_como_strings(resultado)

    esperado = {
        "S' → • S",
        "S → • S S +",
        "S → • S S *",
        "S → • a",
    }

    assert resultado_str == esperado, (
        f"\nEsperado:  {esperado}\nObtenido: {resultado_str}"
    )
    print("  ✓ test_gramatica_1_estado_inicial: PASÓ")


def test_gramatica_1_item_con_punto_en_medio():

    g = Grammar("S'")
    g.add_production("S'", ["S"])
    g.add_production("S",  ["S", "S", "+"])
    g.add_production("S",  ["S", "S", "*"])
    g.add_production("S",  ["a"])

    prod_ss_plus = g.productions_for("S")[0]   # S → S S +
    item = LRItem(prod_ss_plus, 1)              # S → S • S +

    resultado = cerradura({item}, g)
    resultado_str = items_como_strings(resultado)

    esperado = {
        "S → S • S +",
        "S → • S S +",
        "S → • S S *",
        "S → • a",
    }

    assert resultado_str == esperado, (
        f"\nEsperado:  {esperado}\nObtenido: {resultado_str}"
    )
    print("  ✓ test_gramatica_1_item_con_punto_en_medio: PASÓ")


def test_gramatica_1_item_completo():
    """
    Un ítem completo NO debe expandirse.
    CERRADURA({S → a •}) = {S → a •}   (solo el ítem de reducción, nada más)
    """
    g = Grammar("S'")
    g.add_production("S'", ["S"])
    g.add_production("S",  ["S", "S", "+"])
    g.add_production("S",  ["S", "S", "*"])
    g.add_production("S",  ["a"])

    prod_a = g.productions_for("S")[2]   # S → a
    item   = LRItem(prod_a, 1)           # S → a •  (ítem completo)

    resultado = cerradura({item}, g)
    resultado_str = items_como_strings(resultado)

    assert resultado_str == {"S → a •"}, (
        f"Un ítem completo no debe expandirse.\nObtenido: {resultado_str}"
    )
    print("  ✓ test_gramatica_1_item_completo: PASÓ")


def test_gramatica_2_epsilon():

    g = Grammar("S'")
    g.add_production("S'", ["S"])
    g.add_production("S",  ["(", "S", ")"])
    g.add_production("S",  [])            # S → ε

    item_inicial = LRItem(g.productions_for("S'")[0], 0)
    resultado = cerradura({item_inicial}, g)
    resultado_str = items_como_strings(resultado)

    esperado = {
        "S' → • S",
        "S → • ( S )",
        "S → •",          # ítem de reducción por epsilon
    }

    assert resultado_str == esperado, (
        f"\nEsperado:  {esperado}\nObtenido: {resultado_str}"
    )
    print("  ✓ test_gramatica_2_epsilon: PASÓ")


def test_gramatica_3_estado_inicial():

    g = Grammar("S'")
    g.add_production("S'", ["S"])
    g.add_production("S",  ["L"])
    g.add_production("L",  ["a", "L"])
    g.add_production("L",  ["a"])

    item_inicial = LRItem(g.productions_for("S'")[0], 0)
    resultado = cerradura({item_inicial}, g)
    resultado_str = items_como_strings(resultado)

    esperado = {
        "S' → • S",
        "S → • L",
        "L → • a L",
        "L → • a",
    }

    assert resultado_str == esperado, (
        f"\nEsperado:  {esperado}\nObtenido: {resultado_str}"
    )
    print("  ✓ test_gramatica_3_estado_inicial: PASÓ")


def test_no_hay_duplicados():

    g = Grammar("S'")
    g.add_production("S'", ["S"])
    g.add_production("S",  ["S", "S", "+"])
    g.add_production("S",  ["S", "S", "*"])
    g.add_production("S",  ["a"])

    item_inicial = LRItem(g.productions_for("S'")[0], 0)
    resultado = cerradura({item_inicial}, g)

    # Convertimos a lista de strings y verificamos que no haya repetidos
    resultado_str = [repr(it) for it in resultado]
    assert len(resultado_str) == len(set(resultado_str)), (
        f"La cerradura contiene ítems duplicados: {resultado_str}"
    )
    print("  ✓ test_no_hay_duplicados: PASÓ")


# ─── Ejecutor sin pytest ──────────────────────────────────────────────────────

if __name__ == "__main__":
    print()
    print("═" * 50)
    print("  EJECUTANDO PRUEBAS DE CERRADURA LR(0)")
    print("═" * 50)
    print()

    pruebas = [
        test_gramatica_1_estado_inicial,
        test_gramatica_1_item_con_punto_en_medio,
        test_gramatica_1_item_completo,
        test_gramatica_2_epsilon,
        test_gramatica_3_estado_inicial,
        test_no_hay_duplicados,
    ]

    pasadas = 0
    falladas = 0

    for prueba in pruebas:
        try:
            prueba()
            pasadas += 1
        except AssertionError as e:
            print(f"  ✗ {prueba.__name__}: FALLÓ")
            print(f"    {e}")
            falladas += 1

    print()
    print("─" * 50)
    print(f"  Resultado: {pasadas} pasadas, {falladas} falladas")
    print("─" * 50)
    print()
