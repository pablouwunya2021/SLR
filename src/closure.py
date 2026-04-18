"""
closure.py
----------
Implementa la función CERRADURA (closure) de un conjunto de ítems LR(0).

"""

from src.grammar import Grammar
from src.item import LRItem


def cerradura(items: set[LRItem], grammar: Grammar) -> list[LRItem]:
    """
    Calcula la CERRADURA de un conjunto de ítems LR(0).
    """

    resultado: dict[LRItem, None] = {item: None for item in items}

    # Cola de ítems pendientes de procesar.
    # Comenzamos con todos los ítems del conjunto inicial.
    pendientes: list[LRItem] = list(items)

    # ── Bucle principal ────────────────────────────────────────────────────────
    # Procesamos cada ítem de la cola. Si al procesarlo se agregan nuevos ítems,
    # estos se encolan también.
    while pendientes:
        # Tomamos el siguiente ítem a procesar
        item_actual = pendientes.pop(0)

        # Obtenemos el símbolo inmediatamente a la derecha del punto
        B = item_actual.symbol_after_dot
        # no hay nada que expandir → pasamos al siguiente ítem.
        if B is None or not grammar.is_non_terminal(B):
            continue

        
        for produccion in grammar.productions_for(B):
            # El nuevo ítem siempre empieza con el punto al inicio: B → • γ
            nuevo_item = LRItem(produccion, dot_pos=0)

        
            if nuevo_item not in resultado:
                resultado[nuevo_item] = None   # agregamos al conjunto resultado
                pendientes.append(nuevo_item)  # lo encolamos para procesarlo

    return list(resultado.keys())


# ─────────────────────────────────────────────────────────────────────────────


def cerradura_con_traza(
    items: set[LRItem],
    grammar: Grammar
) -> tuple[list[LRItem], list[str]]:

    resultado: dict[LRItem, None] = {item: None for item in items}
    pendientes: list[LRItem] = list(items)
    traza: list[str] = []

    # Registramos el conjunto de entrada en la traza
    traza.append("─" * 55)
    traza.append("CONJUNTO DE ENTRADA:")
    for item in items:
        traza.append(f"  {item}")
    traza.append("─" * 55)
    traza.append("APLICANDO REGLA DE CERRADURA:")

    while pendientes:
        item_actual = pendientes.pop(0)
        B = item_actual.symbol_after_dot

        if B is None or not grammar.is_non_terminal(B):
            # Registramos en la traza por qué no se expande este ítem
            if B is None:
                razon = "ítem completo (punto al final) → no se expande"
            else:
                razon = f"'{B}' es terminal → no se expande"
            traza.append(f"\n  [{item_actual}]  →  {razon}")
            continue

        # B es no-terminal: vamos a expandir
        traza.append(f"\n  [{item_actual}]  →  '{B}' es no-terminal, expandiendo...")

        producciones_de_B = grammar.productions_for(B)
        if not producciones_de_B:
            traza.append(f"    (sin producciones para '{B}')")
            continue

        for produccion in producciones_de_B:
            nuevo_item = LRItem(produccion, dot_pos=0)
            if nuevo_item not in resultado:
                resultado[nuevo_item] = None
                pendientes.append(nuevo_item)
                traza.append(f"    ✓ AGREGADO: {nuevo_item}")
            else:
                traza.append(f"    · ya existe: {nuevo_item}")

    traza.append("\n" + "─" * 55)
    traza.append("CERRADURA COMPLETA:")
    for i, item in enumerate(resultado.keys()):
        traza.append(f"  {i+1}. {item}")
    traza.append("─" * 55)

    return list(resultado.keys()), traza
