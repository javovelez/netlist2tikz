# Bug: comas dentro de labels rompen el parser silenciosamente

**Reportado:** 2026-05-15 — descubierto generando figuras de cuadripolos para TP3 de TCII.
**Severidad:** Alta (falla silenciosa: PDF vacío sin error).
**Versión afectada:** la del repo actual (instalación editable en `<repo>/.venv`).

---

## Síntoma

El comando `n2t render` retorna código 0 e imprime `Escrito: foo.pdf`,
pero el PDF generado está **vacío** (~1 KB en lugar de los ~37 KB
habituales para un circuito simple). El usuario no se entera del
problema hasta abrir el PDF.

---

## Repro mínimo

```bash
cat > /tmp/repro.sch <<'EOF'
V1 1 0_1; down, l=5\,I_1
R1 1 2; right
W 0_1 2; right
EOF

n2t render /tmp/repro.sch -o /tmp/repro.pdf
ls -la /tmp/repro.pdf          # ~1 KB, vacío

n2t render /tmp/repro.sch --tikz --no-standalone | grep V1
# salida observada:
#   \draw (1) to [V, l_=$5\$, n=V1] (0_1)
# salida esperada:
#   \draw (1) to [V, l_=$5\,I_1$, n=V1] (0_1)
```

El `$5\$` con backslash huérfano genera TikZ inválido. `pdflatex`
**compila igual** porque el error queda dentro de un `\draw` y el
motor de TikZ lo descarta silenciosamente, devolviendo página en
blanco. `n2t` no chequea que el PDF contenga objetos dibujados.

---

## Causa raíz

El parser del netlist divide las **opciones** (lo que va después del
`;`) por comas, **sin respetar contextos LaTeX**. Cuando el valor de
una opción de label contiene:

- `\,` (espacio fino), `\;`, `\:`, `\!`
- `{,}` (coma decimal española)
- cualquier secuencia con coma interna

el parser corta en esa coma, el fragmento restante se pierde, y la
label queda truncada en mitad de una secuencia LaTeX (`$5\` sin
cerrar).

**Ubicación probable:** algún `split(',')` o regex equivalente en
`netlist2tikz/parser.py` o `lexer.py`, función que parsea el
segmento de opciones después del `;`.

---

## Comportamiento actual vs esperado

| Aspecto | Actual | Esperado |
|---|---|---|
| Parseo de `l=5\,I_1` | corta en la coma del `\,` → label `5\` | label completa `5\,I_1` |
| Reporte de error | ninguno (exit 0) | warning o error de parseo |
| PDF resultante | página vacía (~1 KB) | render correcto, o error explícito |

---

## Workaround vigente

Envolver toda label problemática en llaves:

```
V1 1 0_1; down, l={5\,I_1}
R1 4 0;   down, l={16{,}2\,V_a}
F1 3 0;   up,   l={r_m\,I_1}
```

El parser **sí** respeta `{...}` como atómico en los casos
probados. Esto debería documentarse mientras tanto en
`skill/SKILL.md`.

---

## Sugerencias de fix

### 1. Mínimo invasivo (recomendado): parser robusto

En la función que separa opciones, tratar `{...}` y `\X` como
contextos atómicos. Algoritmo de referencia:

```python
def split_options(s: str) -> list[str]:
    out, buf, depth = [], [], 0
    i = 0
    while i < len(s):
        c = s[i]
        # \X cuenta como un token único (no interpretar la X)
        if c == '\\' and i + 1 < len(s):
            buf.append(s[i:i+2]); i += 2; continue
        # {...} es contexto atómico
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        if c == ',' and depth == 0:
            out.append(''.join(buf).strip()); buf = []
        else:
            buf.append(c)
        i += 1
    if buf:
        out.append(''.join(buf).strip())
    return out
```

### 2. Defensa adicional: detectar render vacío

En el render path, después de generar el PDF, validar que el archivo
tenga un tamaño razonable o (mejor) inspeccionar la página con
`pdftotext` / `pdfinfo` para detectar páginas en blanco. Emitir
warning con la línea ofensora del netlist.

Heurística simple:

```python
import os
if os.path.getsize(out_pdf) < 2000:
    warnings.warn(
        f"PDF resultante muy pequeño ({size} B). "
        f"Posible label rota; revisar opciones con comas internas."
    )
```

### 3. Documentación

Agregar sección **"Caveats / Escapado de labels"** en
[`skill/SKILL.md`](skill/SKILL.md) mencionando que labels con `\,`,
`\;`, `\:`, `\!` o comas decimales `{,}` deben envolverse en
`{...}`. Actualmente no figura.

---

## Tests sugeridos

Agregar a `tests/`:

```python
def test_label_with_thinspace():
    sch = Schematic.from_string("V1 1 0; down, l=5\\,I_1\n")
    tikz = sch.to_tikz(standalone=False)
    assert "5\\,I_1" in tikz  # actualmente FALLA

def test_label_with_spanish_decimal():
    sch = Schematic.from_string("R1 1 0; down, l=16{,}2\\,V\n")
    tikz = sch.to_tikz(standalone=False)
    assert "16{,}2" in tikz   # actualmente FALLA

def test_silent_render_failure_detection(tmp_path):
    """Un netlist con label rota NO debe producir PDF de <2KB sin warning."""
    sch = Schematic.from_string("V1 1 0; down, l=5\\,I_1\n")
    out = tmp_path / "x.pdf"
    with pytest.warns(UserWarning, match="muy pequeño|label"):
        sch.to_pdf(str(out))
```

---

## Casos reales rotos en el TP de cuadripolos (TCII)

| Ejercicio | Label original | Workaround aplicado |
|---|---|---|
| Ej 4 — CCCS 6·I₂ | `l=6\,I_2` | `l={6\,I_2}` |
| Ej 6 — fuente 5·I₁ | `l=5\,I_1` | `l={5\,I_1}` |
| Ej 7 — fuente 16,2·Vₐ | `l=16{,}2\,V_a` | `l={16{,}2\,V_a}` |
| Ej 8 — fuente rₘ·I₁ | `l=r_m\,I_1` | `l={r_m\,I_1}` |
| Ej 21 — fuente 0,0395·V₁ | `l=0{,}0395\,V_1` | `l={0{,}0395\,V_1}` |

Antes del workaround, los 5 PDFs eran de ~1 KB (vacíos). Después,
~37–46 KB con render correcto.

---

## Próximos pasos sugeridos

1. **Patch del parser** (sección "Sugerencias de fix #1").
2. **Tests de regresión** con los casos reales del TP.
3. **Warning de render vacío** (sección #2).
4. **Update de `skill/SKILL.md`** con el caveat mientras tanto.

Una vez que el parser respete `{...}` y `\X`, todos los netlists del
TP3 funcionarán **sin** las llaves de workaround.
