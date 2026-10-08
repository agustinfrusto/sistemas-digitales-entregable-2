# Entregable #2 — Control de balizas (Sistemas Digitales)

Proyecto de Sistemas Digitales. Se diseña una máquina de estados de Moore con flip-flops D que enciende las balizas de un camino cuando un vehículo completa la secuencia de ingreso S1S2 = 00 → 10 → 11 → 01 → 00. El sensor S3 reinicia el circuito de forma asíncrona.

Este repositorio permite que el equipo consulte el diseño con el agente de IA que prefiera. El agente solo responde sobre la lógica del modelo y el armado del circuito en SimulIDE 0.4.14-SR4, y no modifica nada.

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `Sistemas Digitales - Entregable #2 LETRA.pdf` | Letra del entregable (referencia principal). |
| `Apuntes de clase, sugerencia de trabajo.pdf` | Apuntes de clase del profesor (≈ 48 MB). |
| `Sintesis, sis digitales.pdf` | Guía genérica de síntesis, con un ejemplo resuelto. |
| `informe/01-diseno-fsm.md` | Diseño de la FSM, codificación, mapas de Karnaugh y ecuaciones. |
| `informe/02-diagrama-tiempos.md` | Diagrama de tiempos. |
| `informe/03-guia-simulide.md` | Guía de armado y prueba en SimulIDE. |
| `informe/04-esquematico.md` | Esquemático en SimulIDE. |
| `informe/Entregable2-SistemasDigitales.pdf` | Informe completo en PDF. |
| `AGENTS.md` | Reglas que siguen los agentes de IA (fuente única). |

## 1. Clonar el repositorio

Elija una de las tres opciones (válidas en Windows y macOS). El PDF de apuntes pesa ≈ 48 MB, por lo que la descarga puede tardar.

**a) Git en la terminal**

```bash
git clone https://github.com/agustinfrusto/sistemas-digitales-entregable-2.git
```

Si no tiene git: en Windows instale [Git for Windows](https://git-scm.com/download/win); en macOS ejecute `xcode-select --install` (Xcode Command Line Tools).

**b) GitHub Desktop**

1. Instale [GitHub Desktop](https://desktop.github.com/).
2. Menú File → Clone repository → pestaña URL.
3. Pegue `https://github.com/agustinfrusto/sistemas-digitales-entregable-2` y confirme.

**c) Descargar ZIP**

1. Abra la [página del repositorio](https://github.com/agustinfrusto/sistemas-digitales-entregable-2).
2. Botón verde Code → Download ZIP.
3. Descomprima la carpeta.

## 2. Consultar el diseño con un agente de IA

### Opción A — Agentes que leen la carpeta del repositorio

| Herramienta | Cómo iniciarla | Archivo que lee automáticamente |
|---|---|---|
| [Claude Code](https://claude.com/product/claude-code) | CLI `claude` dentro de la carpeta, o pestaña Code de la app de escritorio de Claude | `CLAUDE.md` → `AGENTS.md` |
| [OpenAI Codex](https://developers.openai.com/codex) | CLI `codex` dentro de la carpeta, o app de Codex | `AGENTS.md` |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `gemini` dentro de la carpeta | `GEMINI.md` → `AGENTS.md` |
| [Google Antigravity](https://antigravity.google/) | Abrir la carpeta | `GEMINI.md` / `AGENTS.md` |
| [Cursor](https://cursor.com/) | Abrir la carpeta | `AGENTS.md` |
| [VS Code](https://code.visualstudio.com/) + [GitHub Copilot](https://github.com/features/copilot) | Abrir la carpeta; usar el chat en modo agente | `AGENTS.md` |

Pasos:

1. Instale la herramienta siguiendo su sitio oficial (enlaces de la tabla).
2. Abra una terminal (PowerShell en Windows, Terminal en macOS) en la carpeta clonada, o abra la carpeta desde la aplicación.
3. Inicie el agente y haga su pregunta.

> **Recomendación:** si el agente pide permiso para editar archivos o ejecutar comandos, rechácelo. Use los modos de solo lectura o de planificación cuando existan.

### Opción B — Aplicaciones de chat sin acceso al repositorio

Sirve para ChatGPT, Claude y Gemini (escritorio o web, Windows o macOS).

1. Inicie un chat nuevo (o un Project / Gem).
2. Suba estos archivos: `AGENTS.md`, `informe/Entregable2-SistemasDigitales.pdf` y `Sistemas Digitales - Entregable #2 LETRA.pdf`. Los apuntes de clase son opcionales y pueden superar el límite de carga.
3. Pegue este primer mensaje:

```text
Sigue AGENTS.md como tus instrucciones para toda esta conversación.
Los otros archivos adjuntos son la letra del entregable y el informe de diseño.
Responde solo sobre este entregable, en español, citando el archivo usado.
```

Para reutilizarlo: en ChatGPT Projects, Claude Projects o Gemini Gems, pegue el contenido de `AGENTS.md` en las instrucciones del proyecto.

## 3. Ejemplos de preguntas

- ¿Por qué la máquina necesita 5 estados?
- ¿Por qué hay transiciones de retroceso en q1, q2 y q3?
- ¿Qué significa una X en la tabla de estado/salida?
- ¿Por qué se eligió esta codificación de los estados?
- ¿Cómo se obtiene D1 a partir de su mapa de Karnaugh?
- ¿Cómo conecto el reset asíncrono (S3) en SimulIDE?
- ¿Por qué E se enciende un ciclo de reloj después de completar la secuencia?
- Mi LED no se enciende nunca: ¿qué debo revisar?

## 4. Qué hace y qué no hace el agente

Hace:

- Explica la lógica de la FSM, los pasos de síntesis y el diagrama de tiempos.
- Guía el armado y la depuración en SimulIDE.
- Revisa la coherencia con la letra, citando el archivo usado.

No hace:

- Crear, editar o borrar archivos, ni hacer commit o push.
- Responder sobre otras materias, programación general, el guion del video o la entrega en Moodle.

Las reglas completas están en [`AGENTS.md`](AGENTS.md).

## 5. Regenerar el PDF (opcional)

```bash
bash informe/generar_pdf.sh
```

Requiere Python 3, pandoc y Google Chrome. Por ahora solo se probó en macOS (la ruta de Chrome es específica de macOS).
