

from __future__ import annotations
from src.grammar import Production


class LRItem:
    

    def __init__(self, production: Production, dot_pos: int = 0):
        # Validamos que el punto esté dentro del rango permitido.
        if not (0 <= dot_pos <= len(production.body)):
            raise ValueError(
                f"dot_pos={dot_pos} fuera de rango para producción '{production}' "
                f"(body tiene {len(production.body)} símbolo(s))."
            )
        self.production = production
        self.dot_pos = dot_pos

    # --- Propiedades de conveniencia ------------------------------------------

    @property
    def head(self) -> str:
        """No-terminal de la cabeza de la producción subyacente."""
        return self.production.head

    @property
    def body(self) -> tuple[str, ...]:
        """Cuerpo de la producción subyacente."""
        return self.production.body

    @property
    def symbol_after_dot(self) -> str | None:
    
        if self.is_complete:
            return None
        return self.body[self.dot_pos]

    @property
    def is_complete(self) -> bool:
  
        return self.dot_pos == len(self.body)

    # --- Operaciones ----------------------------------------------------------

    def advance(self) -> "LRItem":
      
        if self.is_complete:
            raise RuntimeError(
                f"No se puede avanzar el punto de un ítem completo: {self}"
            )
        return LRItem(self.production, self.dot_pos + 1)

    # --- Métodos especiales ---------------------------------------------------

    def __repr__(self) -> str:
      
        body_list = list(self.body)

        # Para producciones épsilon: mostramos solo el punto
        if not body_list:
            return f"{self.head} → •"

        # Insertamos el símbolo '•' en la posición correcta
        body_with_dot = body_list.copy()
        body_with_dot.insert(self.dot_pos, "•")
        return f"{self.head} → {' '.join(body_with_dot)}"

    def __eq__(self, other) -> bool:
        """Dos ítems son iguales si tienen la misma producción Y la misma posición del punto."""
        if not isinstance(other, LRItem):
            return False
        return self.production == other.production and self.dot_pos == other.dot_pos

    def __hash__(self) -> int:
        """
        Necesario para meter ítems en un set (lo que usamos en CERRADURA).
        Combinamos el hash de la producción y la posición del punto.
        """
        return hash((self.production, self.dot_pos))
