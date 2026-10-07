# Guía de armado y prueba en SimulIDE

Guía para implementar el diseño de `01-diseno-fsm.md` en SimulIDE 0.4.14-SR4 y
verificar su funcionamiento.

## Ecuaciones a implementar

| Señal | Ecuación | Circuito |
|---|---|---|
| D2 | Q2 + Q1·Q0'·S2' | OR( Q2 , AND3( Q1, Q0', S2' ) ) |
| D1 | Q2'·S2 | AND( Q2', S2 ) |
| D0 | Q2'·S1 | AND( Q2', S1 ) |
| E | Q2 | Q2 conectada al LED |

## Componentes

| Cantidad | Componente | Uso |
|---|---|---|
| 3 | Flip-flop D con reset asíncrono | Q2, Q1, Q0 |
| 1 | Compuerta AND de 3 entradas | Término Q1·Q0'·S2' |
| 2 | Compuerta AND de 2 entradas | D1 y D0 |
| 1 | Compuerta OR de 2 entradas | D2 |
| 1 | Inversor | S2' |
| 1 | Fuente de reloj | CLK común |
| 3 | Interruptor o entrada lógica | S1, S2, S3 |
| 1 | LED + resistencia de 100 Ω a 1 kΩ | Salida E (balizas) |

## Conexiones

1. **Reloj:** el mismo CLK va a la entrada de reloj de los tres flip-flops.
2. **Reset:** S3 va al reset asíncrono de los tres flip-flops, que los lleva a
   000 (q0).
   - Verificar la polaridad del pin en SimulIDE. Si el reset es activo en
     bajo, conectar S3 a través de un inversor.
   - Los pines de set (preset) que no se usen se dejan en su nivel inactivo.
3. **Señales negadas:** Q2' y Q0' se toman de la salida Q' (Q negada) de cada
   flip-flop, sin inversores extra. S2' sí necesita un inversor.
4. **Lógica de estado siguiente:**
   - D2: AND3( Q1, Q0', S2' ) va a una entrada de la OR, y Q2 a la otra. La
     salida de la OR va a la entrada D del flip-flop Q2.
   - D1: AND( Q2', S2 ) va a la entrada D del flip-flop Q1.
   - D0: AND( Q2', S1 ) va a la entrada D del flip-flop Q0.
5. **Salida:** Q2 va al ánodo del LED, el cátodo a la resistencia y la
   resistencia a masa.

## Prueba de funcionamiento

Antes de cada prueba, activar y soltar S3 para partir de q0. Cada cambio de los
sensores se refleja en el siguiente flanco ascendente de CLK.

### Caso típico (coincide con el diagrama de tiempos)

| Paso | Acción | S1S2 | Estado esperado (Q2Q1Q0) | LED |
|---|---|---|---|---|
| 1 | Situación inicial | 00 | q0 (000) | Apagado |
| 2 | Activar S1 | 10 | q1 (001) | Apagado |
| 3 | Activar S2 | 11 | q2 (011) | Apagado |
| 4 | Soltar S1 | 01 | q3 (010) | Apagado |
| 5 | Soltar S2 | 00 | q4 (100) | Encendido |
| 6 | Activar S3 | 00 | q0 (000), de inmediato | Apagado |

### Retroceso durante el ingreso (Hip #2)

| Paso | Acción | S1S2 | Estado esperado | LED |
|---|---|---|---|---|
| 1 | Activar S1 | 10 | q1 | Apagado |
| 2 | Activar S2 | 11 | q2 | Apagado |
| 3 | Soltar S2 (retrocede) | 10 | q1 | Apagado |
| 4 | Soltar S1 (sale marcha atrás) | 00 | q0 | Apagado |

El LED no debe encenderse en ningún momento.

### Retroceso y nuevo avance

| Paso | Acción | S1S2 | Estado esperado | LED |
|---|---|---|---|---|
| 1 | S1, S2 y soltar S1 | 01 | q3 | Apagado |
| 2 | Activar S1 (retrocede) | 11 | q2 | Apagado |
| 3 | Soltar S1 | 01 | q3 | Apagado |
| 4 | Soltar S2 | 00 | q4 | Encendido |

### Balizas encendidas

Con el LED encendido (q4), mover S1 o S2 no debe apagarlo. Solo S3 lo apaga.
