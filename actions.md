# Acciones del Agente

## Acciones de Movimiento

| Acción    | Dirección       | Delta (fila, col) | Descripción                                              |
|-----------|-----------------|--------------------|----------------------------------------------------------|
| `up`      | ↑ Arriba        | `(-1,  0)`         | Mueve al agente una casilla hacia arriba                 |
| `down`    | ↓ Abajo         | `( 1,  0)`         | Mueve al agente una casilla hacia abajo                  |
| `left`    | ← Izquierda     | `( 0, -1)`         | Mueve al agente una casilla hacia la izquierda           |
| `right`   | → Derecha       | `( 0,  1)`         | Mueve al agente una casilla hacia la derecha             |

## Acciones de Objetos

| Acción    | Descripción                                                                 |
|-----------|-----------------------------------------------------------------------------|
| `pickup`  | Recoge el objeto en la casilla actual (`K` o `B`). Solo si no lleva nada.   |
| `drop`    | Suelta el objeto que lleva en la casilla actual. Solo en casillas vacías.   |

## Tabla de Recompensas

| Evento                                     | Recompensa | Recompensa Total |
|--------------------------------------------|:----------:|:----------------:|
| Cualquier acción (penalización por paso)   |    **-1**  |       -1         |
| Moverse a casilla vacía                    |      0     |       -1         |
| Moverse contra muro (`#`)                  |    **-5**  |       -6         |
| Moverse contra puerta (`D`) sin llave      |    **-5**  |       -6         |
| Abrir puerta (`D`) con llave (`K`)         |   **+50**  |      +49         |
| Recoger llave (`K`)                        |   **+30**  |      +29         |
| Recoger bola (`B`)                         |   **+10**  |       +9         |
| Soltar objeto                              |   **+20**  |      +19         |
| Llegar a la meta (`E`)                     |  **+100**  |      +99         |

> **Nota:** La recompensa total = penalización base (-1) + recompensa del evento.

## Símbolos del Tablero

| Símbolo | Significado         | Transitable |
|:-------:|---------------------|:-----------:|
| `#`     | Muro                |     ❌      |
| `S`     | Inicio del agente   |     ✅      |
| `E`     | Meta / Salida       |     ✅      |
| `K`     | Llave               |     ✅      |
| `B`     | Bola                |     ✅      |
| `D`     | Puerta (cerrada)    |  🔑 con K   |
| ` `     | Casilla vacía       |     ✅      |
