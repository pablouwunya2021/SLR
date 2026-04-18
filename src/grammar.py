


class Production:

    def __init__(self, head: str, body: list[str]):
        self.head = head
        # Guardamos el cuerpo como tupla para que sea inmutable y hashable.
        # Esto nos permitirá usar producciones como claves en sets/dicts.
        self.body = tuple(body)

    def is_epsilon(self) -> bool:
        """Devuelve True si esta producción es la regla vacía (A → ε)."""
        return len(self.body) == 0

    # --- Métodos especiales ---------------------------------------------------

    def __repr__(self) -> str:
        """Representación legible: usada al imprimir en consola o en el debugger."""
        body_str = " ".join(self.body) if self.body else "ε"
        return f"{self.head} → {body_str}"

    def __eq__(self, other) -> bool:
        """Dos producciones son iguales si tienen la misma cabeza y el mismo cuerpo."""
        if not isinstance(other, Production):
            return False
        return self.head == other.head and self.body == other.body

    def __hash__(self) -> int:
        """
        Necesario para poder meter Production en un set o usarla como clave de dict.
        Se combina el hash de la cabeza y del cuerpo (que ya es una tupla, hashable).
        """
        return hash((self.head, self.body))


# ─────────────────────────────────────────────────────────────────────────────


class Grammar:
    
    def __init__(self, start_symbol: str):
        self.start_symbol: str = start_symbol

        # Lista ordenada de todas las producciones (mantiene el orden de ingreso).
        self.productions: list[Production] = []

        # Conjunto de no-terminales (cabezas de producciones).
        self.non_terminals: set[str] = set()

        # Conjunto de terminales (se calcula cuando se necesita).
        self._terminals: set[str] | None = None

    # --- Construcción ---------------------------------------------------------

    def add_production(self, head: str, body: list[str]) -> None:
       
        prod = Production(head, body)
        self.productions.append(prod)
        # Cada vez que agregamos una producción, registramos su cabeza como no-terminal.
        self.non_terminals.add(head)
        # Invalidamos el caché de terminales para que se recalcule.
        self._terminals = None

    # --- Consultas ------------------------------------------------------------

    def productions_for(self, symbol: str) -> list[Production]:
        
        return [p for p in self.productions if p.head == symbol]

    def is_non_terminal(self, symbol: str) -> bool:
        """Devuelve True si `symbol` es un no-terminal de la gramática."""
        return symbol in self.non_terminals

    def is_terminal(self, symbol: str) -> bool:
        """Devuelve True si `symbol` es un terminal."""
        return symbol in self.terminals

    @property
    def terminals(self) -> set[str]:
       
        if self._terminals is None:
            all_body_symbols = {
                symbol
                for prod in self.productions
                for symbol in prod.body
            }
            # Terminales = símbolos del cuerpo que no son cabeza de ninguna producción.
            self._terminals = all_body_symbols - self.non_terminals
        return self._terminals

    # --- Métodos especiales ---------------------------------------------------

    def __repr__(self) -> str:
        lines = [f"Gramática (inicio: {self.start_symbol})"]
        for prod in self.productions:
            lines.append(f"  {prod}")
        return "\n".join(lines)
