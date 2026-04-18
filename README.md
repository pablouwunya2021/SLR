# Calculadora de Cerradura LR(0)

Programa que calcula la cerradura (closure) de un conjunto de ítems LR(0) para una gramática libre de contexto.

## Requisitos

- Python 3.12+

## Estructura

```
slr-closure/
├── src/
│   ├── grammar.py   # Clases Production y Grammar
│   ├── item.py      # Clase LRItem (ítem con punto •)
│   ├── closure.py   # Función CERRADURA
│   └── display.py   # Presentación en consola
├── tests/
│   └── test_closure.py
└── main.py
```

## Uso

```bash
python main.py
```

Seleccione una gramática del menú y el ítem inicial. El programa muestra el proceso paso a paso y el resultado final.

## Gramáticas disponibles

| Opción | Gramática |
|--------|-----------|
| 1 | S → SS+ \| SS* \| a |
| 2 | S → (S) \| ε |
| 3 | S → L, L → aL \| a |
| 4 | E → E+T \| T, T → T*F \| F, F → (E) \| id *(vista en clase)* |
| 5 | Personalizada |

## Pruebas

```bash
python tests/test_closure.py
```
