# SuperPrompt — Práctica de Estrategias Evolutivas: Isotropía vs Anisotropía

## Contexto del Proyecto

| Campo | Valor |
|---|---|
| **Materia** | Optimización Inteligente |
| **Profesor** | Mtro. Raúl Gibrán Porras Alaniz |
| **Universidad** | Universidad Autónoma de Ciudad Juárez (UACJ) |
| **Programa** | Maestría en Inteligencia Artificial y Analítica de Datos (MIAAD) |
| **Alumno** | Javier Augusto Rebull Saucedo |
| **Matrícula** | 263483 |
| **Fecha de entrega** | 01 de mayo de 2026 |
| **Repositorio** | `https://github.com/jrebull/MIAAD_SMART_EstrategiasEvolutivas` |
| **Directorio de trabajo** | `/Users/haowei/Documents/MIAAD/SMART/EstrategiasEvolutivas` |
| **Directorio de figuras LaTeX** | `/Users/haowei/Documents/MIAAD/SMART/EstrategiasEvolutivas/Figures` |
| **Ambiente Python** | `cd /Users/haowei/Documents/MIAAD/SMART/EstrategiasEvolutivas && source .venv/bin/activate` (crear si no existe) |
| **GitHub user para commits** | `jrebull` |
| **Idioma de commits** | Español |

---

## Definición del Problema (Contexto Matemático)

### Función Objetivo: Elipsoide Invertido (MAXIMIZACIÓN)

$$f(\mathbf{x}) = \exp\left(-\sum_{i=1}^{D} \frac{(x_i - 2.0)^2}{i}\right)$$

| Parámetro | Valor |
|---|---|
| Dimensionalidad $D$ | 10 |
| Espacio de búsqueda | $x_i \in [-5.0, 5.0]$ para toda $i$ |
| Óptimo global | $\mathbf{x}^* = (2.0, 2.0, \ldots, 2.0)$ |
| Valor máximo alcanzable | $f(\mathbf{x}^*) = 1.0$ |

**Naturaleza del problema:** El denominador $i$ en cada término de la sumatoria hace que la pendiente del paisaje cambie en cada dimensión — las primeras dimensiones tienen gradiente empinado y las últimas gradiente suave. Esto genera un paisaje **mal condicionado** que penaliza la mutación isotrópica y favorece la anisotrópica.

### Hiperparámetros sugeridos

| Parámetro | Valor |
|---|---|
| Padres $\mu$ | 20 |
| Descendientes $\lambda$ | 100 |
| Generaciones | 500 |
| Corridas independientes | 30 |
| Umbral de éxito | $f(\mathbf{x}) \geq 0.95$ |

### Fórmulas de auto-adaptación

**Isotrópica** (un solo $\sigma$ global):
$$\sigma' = \sigma \cdot \exp(\tau \cdot \mathcal{N}(0,1))$$
$$\mathbf{x}' = \mathbf{x} + \sigma' \cdot \mathcal{N}(\mathbf{0}, \mathbf{I})$$

Donde $\tau = \frac{1}{\sqrt{2D}}$ (regla de Schwefel).

**Anisotrópica** (un vector $\boldsymbol{\sigma} \in \mathbb{R}^D$):
$$\sigma_i' = \sigma_i \cdot \exp(\tau_0 \cdot \mathcal{N}(0,1) + \tau_i \cdot \mathcal{N}_i(0,1))$$
$$x_i' = x_i + \sigma_i' \cdot \mathcal{N}_i(0,1)$$

Donde $\tau_0 = \frac{1}{\sqrt{2D}}$ (factor global) y $\tau_i = \frac{1}{\sqrt{2\sqrt{D}}}$ (factor individual por coordenada).

### Esquemas de selección

- **(μ + λ):** Selección elitista — los $\mu$ mejores se escogen de la unión padres ∪ descendientes.
- **(μ , λ):** Selección por coma — los $\mu$ mejores se escogen SOLO de los $\lambda$ descendientes (los padres mueren). Requiere $\lambda > \mu$.

### Métricas de evaluación

1. **Gráfica de convergencia:** Fitness promedio (de las 30 corridas) vs generaciones, las 4 variantes superpuestas.
2. **Tasa de éxito:** Porcentaje de corridas con $f(\mathbf{x}) \geq 0.95$.
3. **Gap:** $\text{Gap} = 1 - f(\mathbf{x}_{\text{mejor}})$, reportar Gap promedio y desviación estándar por variante.

---

## 4 Variantes a implementar

| ID | Esquema | Mutación | Clave corta |
|----|---------|----------|-------------|
| V1 | $(\mu + \lambda)$ | Isotrópica | `plus_iso` |
| V2 | $(\mu , \lambda)$ | Isotrópica | `comma_iso` |
| V3 | $(\mu + \lambda)$ | Anisotrópica | `plus_aniso` |
| V4 | $(\mu , \lambda)$ | Anisotrópica | `comma_aniso` |

---

## User Stories

### EPIC 1: Infraestructura del Proyecto

#### US-1.1 — Inicialización del repositorio
**Como** desarrollador,
**quiero** que el proyecto tenga un entorno Python limpio con `requirements.txt`, `README.md` y estructura de carpetas,
**para** que cualquier persona pueda reproducir los experimentos.

**Criterios de aceptación:**
- [ ] Crear virtualenv en `.venv` si no existe: `python3 -m venv .venv`
- [ ] `requirements.txt` con: `numpy`, `matplotlib`, `pandas`, `scipy` (versiones pinneadas)
- [ ] `pip install -r requirements.txt`
- [ ] Estructura de carpetas:
  ```
  EstrategiasEvolutivas/
  ├── src/
  │   ├── __init__.py
  │   ├── evolution_strategy.py      # Motor principal de EE
  │   ├── fitness.py                 # Función objetivo
  │   ├── operators.py               # Mutación, selección, auto-adaptación
  │   └── experiment.py              # Orquestador de 30 corridas × 4 variantes
  ├── Figures/                       # PNGs generadas para el reporte (LaTeX las lee de aquí)
  ├── LaTeX/
  │   └── main.tex                   # Reporte LaTeX (compila en Overleaf)
  ├── web/                           # Sitio Nuxt 3 con resultados interactivos
  │   ├── nuxt.config.ts
  │   ├── app.vue
  │   ├── pages/
  │   ├── components/
  │   ├── public/data/               # JSONs con resultados (copiados de results/)
  │   ├── public/images/             # PNGs de figuras (copiados de Figures/)
  │   ├── package.json
  │   └── tsconfig.json
  ├── results/                       # JSONs / CSVs con resultados numéricos
  ├── requirements.txt
  ├── README.md
  ├── run_experiments.py             # Script principal: ejecuta todo
  └── generate_figures.py            # Script separado: genera figuras
  ```
- [ ] `README.md` en español con: título, descripción, instrucciones de instalación, ejecución, estructura y referencias
- [ ] Archivo `.gitignore` adecuado (`.venv/`, `__pycache__/`, `results/*.csv`, `*.pyc`, `node_modules/`, `.nuxt/`, `.output/`, `dist/`)
- [ ] Commit: `"feat: inicialización del proyecto con estructura y dependencias"`

---

#### US-1.2 — Semillas reproducibles
**Como** investigador,
**quiero** que cada una de las 30 corridas use una semilla determinista diferente,
**para** garantizar reproducibilidad total.

**Criterios de aceptación:**
- [ ] Usar semillas: `seeds = [42 + i for i in range(30)]` o similar esquema determinista
- [ ] Cada corrida establece `np.random.seed(seed)` al inicio
- [ ] Si se ejecuta 2 veces se obtienen resultados idénticos bit a bit
- [ ] Documentar en README la estrategia de semillas

---

### EPIC 2: Motor de Estrategias Evolutivas

#### US-2.1 — Función objetivo (Elipsoide Invertido)
**Como** algoritmo,
**quiero** evaluar la función $f(\mathbf{x}) = \exp\left(-\sum_{i=1}^{D} \frac{(x_i - 2.0)^2}{i}\right)$,
**para** guiar la búsqueda hacia el óptimo global.

**Criterios de aceptación:**
- [ ] Implementar en `src/fitness.py` como función pura `inverted_ellipsoid(x: np.ndarray) -> float`
- [ ] Verificar con test unitario: `inverted_ellipsoid(np.full(10, 2.0))` == `1.0`
- [ ] Verificar: `inverted_ellipsoid(np.zeros(10))` < 1.0 (debería ser ~0.0067)
- [ ] Soportar evaluación vectorizada (array de individuos) si se desea
- [ ] Nota: es MAXIMIZACIÓN, no minimización

---

#### US-2.2 — Representación del individuo
**Como** algoritmo,
**quiero** que cada individuo contenga su vector de decisión $\mathbf{x}$ y su(s) parámetro(s) de estrategia $\sigma$,
**para** que la auto-adaptación opere sobre el genotipo completo.

**Criterios de aceptación:**
- [ ] Clase o namedtuple `Individual` con campos:
  - `x`: np.ndarray de shape (D,) — vector de decisión
  - `sigma`: float (isotrópico) o np.ndarray de shape (D,) (anisotrópico)
  - `fitness`: float
- [ ] Inicialización: $x_i \sim \mathcal{U}(-5.0, 5.0)$; $\sigma_0 = 1.0$ (escalar) o $\sigma_{0,i} = 1.0$ (vector)
- [ ] Método para clonar y mutar (retorna nuevo individuo, no modifica in-place)

---

#### US-2.3 — Mutación isotrópica con auto-adaptación
**Como** algoritmo isotrópico,
**quiero** mutar con un solo $\sigma$ global auto-adaptado,
**para** explorar el espacio con paso uniforme en todas las dimensiones.

**Criterios de aceptación:**
- [ ] Implementar en `src/operators.py`
- [ ] Fórmula:
  ```
  tau = 1 / sqrt(2 * D)
  sigma' = sigma * exp(tau * N(0,1))
  x' = x + sigma' * N(0, I_D)
  ```
- [ ] Aplicar boundary handling: clampear $x_i \in [-5.0, 5.0]$ tras mutación
- [ ] Aplicar lower bound en sigma: $\sigma' = \max(\sigma', \epsilon)$ con $\epsilon = 1 \times 10^{-8}$ para evitar estancamiento
- [ ] Test: verificar que sigma cambia entre generaciones

---

#### US-2.4 — Mutación anisotrópica con auto-adaptación
**Como** algoritmo anisotrópico,
**quiero** mutar con un vector $\boldsymbol{\sigma} \in \mathbb{R}^D$ auto-adaptado por coordenada,
**para** que el paso de mutación se ajuste independientemente a la escala de cada dimensión del paisaje.

**Criterios de aceptación:**
- [ ] Implementar en `src/operators.py`
- [ ] Fórmula:
  ```
  tau_global = 1 / sqrt(2 * D)
  tau_local  = 1 / sqrt(2 * sqrt(D))
  global_noise = N(0,1)  # un solo escalar compartido
  for i in range(D):
      sigma_i' = sigma_i * exp(tau_global * global_noise + tau_local * N_i(0,1))
      x_i'     = x_i + sigma_i' * N_i(0,1)
  ```
- [ ] Boundary handling y lower bound en sigma como en US-2.3
- [ ] Test: verificar que sigma converge a valores distintos por dimensión (las primeras dimensiones deberían tener sigma menor que las últimas, dado el denominador $i$)

---

#### US-2.5 — Selección (μ + λ) Elitista
**Como** esquema Plus,
**quiero** seleccionar los $\mu$ mejores de la unión padres ∪ descendientes,
**para** garantizar que nunca se pierda la mejor solución encontrada.

**Criterios de aceptación:**
- [ ] Implementar en `src/operators.py` función `select_plus(parents, offspring, mu)`
- [ ] Unir ambas listas, ordenar por fitness descendente, tomar los primeros $\mu$
- [ ] Test: el mejor individuo NUNCA puede empeorar entre generaciones

---

#### US-2.6 — Selección (μ , λ) Comma
**Como** esquema Comma,
**quiero** seleccionar los $\mu$ mejores SOLO de los $\lambda$ descendientes,
**para** permitir escape de óptimos locales al no preservar padres.

**Criterios de aceptación:**
- [ ] Implementar en `src/operators.py` función `select_comma(offspring, mu)`
- [ ] Ordenar offspring por fitness descendente, tomar los primeros $\mu$
- [ ] Validar que $\lambda > \mu$ al inicio del experimento (assertion)
- [ ] Test: es posible que la mejor solución empeore entre generaciones (y eso es correcto)

---

#### US-2.7 — Loop evolutivo principal
**Como** motor de EE,
**quiero** ejecutar el ciclo completo: inicializar → evaluar → [generar λ descendientes → mutar → evaluar → seleccionar] × 500 generaciones,
**para** resolver la función objetivo.

**Criterios de aceptación:**
- [ ] Implementar en `src/evolution_strategy.py` clase `EvolutionStrategy` con parámetros:
  - `mu`, `lambda_`, `generations`, `dimension`, `bounds`, `selection_type` ("plus" | "comma"), `mutation_type` ("isotropic" | "anisotropic")
- [ ] Método `run(seed) -> dict` que retorna:
  ```python
  {
      "best_fitness_history": list[float],      # mejor fitness por generación
      "avg_fitness_history": list[float],        # fitness promedio por generación
      "best_solution": np.ndarray,               # mejor x encontrado
      "best_fitness": float,                     # f(x_mejor)
      "sigma_history": list,                     # evolución de sigma(s) — para diagnóstico
      "seed": int
  }
  ```
- [ ] Cada generación: generar $\lambda$ descendientes eligiendo padre aleatoriamente de los $\mu$, mutar, evaluar, seleccionar
- [ ] Guardar historial de fitness para gráficas de convergencia

---

### EPIC 3: Experimentación

#### US-3.1 — Orquestador de experimentos
**Como** experimentador,
**quiero** ejecutar automáticamente 30 corridas × 4 variantes = 120 ejecuciones,
**para** obtener resultados estadísticamente significativos.

**Criterios de aceptación:**
- [ ] Implementar en `src/experiment.py` o `run_experiments.py`
- [ ] Iterar sobre las 4 variantes × 30 semillas
- [ ] Guardar resultados en `results/` como CSV o JSON:
  - `results/convergence_data.csv`: columnas `variant`, `run`, `generation`, `best_fitness`, `avg_fitness`
  - `results/summary.csv`: columnas `variant`, `run`, `final_best_fitness`, `gap`, `success`
- [ ] Mostrar progreso en terminal (print o tqdm)
- [ ] Tiempo estimado: <5 minutos para las 120 ejecuciones (optimizar si es necesario)
- [ ] Commit: `"feat: ejecución completa de 120 experimentos (30 × 4 variantes)"`

---

#### US-3.2 — Cálculo de métricas
**Como** analista,
**quiero** calcular Gap, tasa de éxito y estadísticas descriptivas por variante,
**para** incluirlas en el reporte.

**Criterios de aceptación:**
- [ ] Gap individual: $\text{Gap}_j = 1 - f(\mathbf{x}_{\text{mejor},j})$ para cada corrida $j$
- [ ] Gap promedio y desviación estándar por variante
- [ ] Tasa de éxito: $\frac{\text{corridas con } f(\mathbf{x}) \geq 0.95}{30} \times 100\%$
- [ ] Tabla resumen con formato:

  | Variante | Gap Promedio | Gap Desv. Estándar | Tasa de Éxito (%) | Mejor Fitness Prom. | Mejor Fitness Máx. |
  |---|---|---|---|---|---|
  | (μ+λ) Iso | ... | ... | ... | ... | ... |
  | (μ,λ) Iso | ... | ... | ... | ... | ... |
  | (μ+λ) Aniso | ... | ... | ... | ... | ... |
  | (μ,λ) Aniso | ... | ... | ... | ... | ... |

- [ ] **REGLA DE ORO:** Todos los valores numéricos deben generarse programáticamente desde los datos reales. Prohibido hardcodear.
- [ ] Formato numérico mexicano en reporte LaTeX: punto decimal, comas para miles

---

### EPIC 4: Visualización

#### US-4.1 — Gráfica de convergencia comparativa
**Como** evaluador,
**quiero** una sola gráfica que muestre la curva de convergencia promedio (30 corridas) de las 4 variantes,
**para** comparar visualmente el comportamiento de cada esquema.

**Criterios de aceptación:**
- [ ] Implementar en `generate_figures.py`
- [ ] Eje X: Generación (0–500), Eje Y: Fitness promedio
- [ ] 4 curvas con colores distinguibles y leyenda clara
- [ ] Incluir banda de sombra (±1 desv. estándar) con alpha bajo
- [ ] Paleta sugerida UACJ: Azul `#003CA6`, Oro `#C8962E`, Gris `#555559`, Rojo `#B71C1C` (o similar de alto contraste)
- [ ] Etiquetas en español: "Generación", "Fitness Promedio"
- [ ] Resolución: 300 DPI, formato PNG
- [ ] Guardar en `Figures/convergence_comparison.png`
- [ ] Tamaño: `figsize=(10, 6)` mínimo
- [ ] Fondo blanco, grid suave, fuente legible (≥12pt)

---

#### US-4.2 — Gráfica de barras de Gap y Tasa de Éxito
**Como** evaluador,
**quiero** gráficas adicionales que muestren Gap promedio (con barras de error) y tasa de éxito por variante,
**para** complementar el análisis cuantitativo.

**Criterios de aceptación:**
- [ ] Gráfica de barras del Gap promedio con barras de error (desv. estándar) por variante
- [ ] Gráfica de barras de tasa de éxito (%) por variante
- [ ] Misma paleta de colores que la gráfica de convergencia
- [ ] Guardar como:
  - `Figures/gap_comparison.png`
  - `Figures/success_rate.png`
- [ ] 300 DPI, fondo blanco, etiquetas en español

---

#### US-4.3 — Gráfica de evolución de sigma(s)
**Como** analista,
**quiero** una gráfica que muestre cómo evolucionan los parámetros de mutación (σ) a lo largo de las generaciones para las variantes anisotrópica e isotrópica,
**para** evidenciar la ventaja de la auto-adaptación individual por coordenada.

**Criterios de aceptación:**
- [ ] Para isotrópica: una curva de σ global vs generación (promedio de 30 corridas, una corrida representativa, o la mediana)
- [ ] Para anisotrópica: $D=10$ curvas de σ por dimensión vs generación, preferiblemente mostrando que σ₁ (gradiente empinado) < σ₁₀ (gradiente suave)
- [ ] Guardar como `Figures/sigma_evolution.png`

---

### EPIC 5: Reporte LaTeX

#### US-5.1 — Estructura del documento LaTeX
**Como** alumno,
**quiero** un reporte LaTeX que siga el formato de cabecera UACJ/MIAAD proporcionado como ejemplo,
**para** entregar un documento profesional y consistente con entregas anteriores.

**Criterios de aceptación:**
- [ ] Crear `/Users/haowei/Documents/MIAAD/SMART/EstrategiasEvolutivas/LaTeX/main.tex`
- [ ] Mantener **íntegra** la cabecera del ejemplo LaTeX proporcionado, solo actualizando:
  - Materia: `Optimización Inteligente` $\bullet$ `Mtro. Raúl Gibrán Porras Alaniz`
  - Título: `Práctica de Estrategias Evolutivas: Isotropía vs Anisotropía`
  - Subtítulo: `Evaluación de mecanismos de auto-adaptación y esquemas de selección`
  - Fecha: `01 de mayo de 2026`
  - Matrícula: `263483`
- [ ] Mantener **íntegra** la foto de perfil de Javier Rebull en la conclusión (sección `wrapfigure` con `javiprofile.jpg`)
- [ ] Fuente: **Helvetica** (`\usepackage{helvet}`, `\renewcommand{\familydefault}{\sfdefault}`) — como en el ejemplo
- [ ] `\graphicspath{{../Figures/}}` para que compile desde el subdirectorio `LaTeX/`
- [ ] **NO generar PDF** — Javier lo compila en Overleaf
- [ ] Compilable sin errores en Overleaf (verificar que no haya dependencias faltantes)
- [ ] Usar `\texorpdfstring` en títulos de sección que contengan fórmulas

---

#### US-5.2 — Contenido del reporte
**Como** alumno,
**quiero** que el reporte cubra todas las secciones necesarias con rigor técnico,
**para** obtener la máxima calificación.

**Secciones requeridas:**

1. **Introducción**
   - Qué son las Estrategias Evolutivas (breve historia: Rechenberg 1960s, Schwefel)
   - Diferencia con Algoritmos Genéticos (representación real, auto-adaptación de σ)
   - Objetivo de la práctica: comparar isotrópico vs anisotrópico en paisaje mal condicionado

2. **Marco Teórico**
   - EE y su esquema general $(\mu/\rho \stackrel{+}{,} \lambda)$
   - Auto-adaptación de parámetros de mutación (regla de Schwefel τ)
   - Mutación isotrópica vs anisotrópica (explicar con ecuaciones LaTeX)
   - Selección Plus vs Comma (ventajas/desventajas teóricas)
   - Función Elipsoide Invertido: ¿por qué es mal condicionada?

3. **Metodología**
   - Descripción del algoritmo implementado (pseudocódigo en LaTeX con `algorithm2e` o `algorithmic`)
   - Tabla de hiperparámetros ($\mu=20$, $\lambda=100$, $D=10$, 500 generaciones, 30 corridas)
   - Manejo de restricciones de caja

4. **Resultados Experimentales**
   - Gráfica de convergencia (Figure con referencia)
   - Tabla de resultados: Gap promedio ± desv. estándar, tasa de éxito por variante
   - Gráfica de Gap y tasa de éxito (barras)
   - Gráfica de evolución de σ (evidencia de auto-adaptación)
   - Análisis: ¿qué variante fue mejor y por qué?

5. **Discusión**
   - ¿Por qué la anisotrópica supera a la isotrópica en este problema?
   - ¿Qué efecto tiene Plus vs Comma en la convergencia?
   - Conexión con la teoría: la regla de Schwefel en acción
   - Limitaciones del experimento

6. **Conclusiones**
   - Con la foto `wrapfigure` de Javier Rebull a la izquierda
   - Reflexión personal conectando con experiencia profesional en banca (Santander)
   - Analogía: la auto-adaptación anisotrópica es como ajustar la tolerancia al riesgo de forma diferenciada por producto financiero, no con una política uniforme
   - Lecciones aprendidas

7. **Referencias** (formato IEEE)

---

#### US-5.3 — Referencias en formato IEEE
**Como** alumno,
**quiero** citar fuentes académicas confiables verificadas en la web,
**para** fundamentar el marco teórico con rigor.

**Referencias obligatorias:**

```bibtex
% [1] Paper fundacional de Rechenberg
@book{rechenberg1973,
  author    = {Rechenberg, Ingo},
  title     = {Evolutionsstrategie: Optimierung technischer Systeme nach Prinzipien der biologischen Evolution},
  publisher = {Frommann-Holzboog},
  address   = {Stuttgart},
  year      = {1973}
}

% [2] Libro de Schwefel
@book{schwefel1995,
  author    = {Schwefel, Hans-Paul},
  title     = {Evolution and Optimum Seeking},
  publisher = {Wiley},
  address   = {New York},
  year      = {1995}
}

% [3] Beyer & Schwefel — Comprehensive introduction (Natural Computing)
@article{beyer2002,
  author  = {Beyer, Hans-Georg and Schwefel, Hans-Paul},
  title   = {Evolution Strategies -- A Comprehensive Introduction},
  journal = {Natural Computing},
  volume  = {1},
  pages   = {3--52},
  year    = {2002},
  doi     = {10.1023/A:1015059928466}
}

% [4] Beyer — Teoría de auto-adaptación
@article{beyer1995,
  author  = {Beyer, Hans-Georg},
  title   = {Toward a Theory of Evolution Strategies: Self-Adaptation},
  journal = {Evolutionary Computation},
  volume  = {3},
  number  = {3},
  pages   = {311--347},
  year    = {1995}
}

% [5] Beyer & Deb — Self-adaptive features
@article{beyer2001,
  author  = {Beyer, Hans-Georg and Deb, Kalyanmoy},
  title   = {On Self-Adaptive Features in Real-Parameter Evolutionary Algorithms},
  journal = {IEEE Transactions on Evolutionary Computation},
  volume  = {5},
  number  = {3},
  pages   = {250--270},
  year    = {2001}
}

% [6] Eiben & Smith — Libro de texto de EC
@book{eiben2015,
  author    = {Eiben, Agoston E. and Smith, James E.},
  title     = {Introduction to Evolutionary Computing},
  publisher = {Springer},
  edition   = {2nd},
  year      = {2015},
  doi       = {10.1007/978-3-662-44874-8}
}

% [7] Bäck, Hammel & Schwefel — Historia y estado del arte
@article{back1997,
  author  = {Bäck, Thomas and Hammel, Ulrich and Schwefel, Hans-Paul},
  title   = {Evolutionary Computation: Comments on the History and Current State},
  journal = {IEEE Transactions on Evolutionary Computation},
  volume  = {1},
  number  = {1},
  pages   = {3--17},
  year    = {1997}
}

% [8] Material de clase
@misc{porras2026ee,
  author       = {Porras Alaniz, Raúl Gibrán},
  title        = {Práctica de Estrategias Evolutivas: Isotropía vs Anisotropía},
  howpublished = {Actividad de clase, Maestría en IA y Analítica de Datos, UACJ},
  year         = {2026}
}

% [9] Material de clase — AG
@misc{porras2026ag,
  author       = {Porras Alaniz, Raúl Gibrán},
  title        = {Programando un Algoritmo Genético desde Cero para el VRP},
  howpublished = {Actividad de clase, Maestría en IA y Analítica de Datos, UACJ},
  year         = {2026}
}
```

- [ ] Usar `\begin{thebibliography}` (no BibTeX) para máxima compatibilidad con Overleaf
- [ ] Formato IEEE estricto: `[1] Apellido, Iniciales., "Título," *Revista*, vol. X, pp. Y–Z, Año.`
- [ ] Todas las referencias deben estar citadas en el texto con `\cite{}`

---

### EPIC 6: Entrega Final

#### US-6.1 — Validación cruzada de figuras y datos
**Como** Javier (yo mismo, revisando mi trabajo),
**quiero** que las figuras del reporte LaTeX y los datos de las tablas se generen programáticamente desde los mismos archivos de resultados,
**para** eliminar cualquier discrepancia entre código, figuras y texto.

**Criterios de aceptación:**
- [ ] Las figuras en `Figures/` se generan con `generate_figures.py` que lee `results/`
- [ ] La tabla de resultados en el LaTeX incluye un comentario `% VALORES GENERADOS DESDE results/summary.csv`
- [ ] Ejecutar script de validación que imprime los valores y se comparan visualmente con el LaTeX
- [ ] NO inventar valores. Si una variante no converge, reportar el Gap real.

---

#### US-6.2 — README del repositorio
**Como** profesor revisando el repo,
**quiero** un README completo en español,
**para** entender qué es el proyecto, cómo ejecutarlo y qué esperar.

**Criterios de aceptación:**
- [ ] Título: `Práctica de Estrategias Evolutivas: Isotropía vs Anisotropía`
- [ ] Secciones: Descripción, Requisitos, Instalación, Ejecución, Estructura del proyecto, Resultados, Referencias
- [ ] Badge o mención del repositorio MIAAD
- [ ] Incluir ejemplo de ejecución y output esperado

---

#### US-6.3 — Commits y push
**Como** alumno,
**quiero** que todos los archivos estén commiteados con mensajes descriptivos en español,
**para** tener un historial limpio en GitHub.

**Criterios de aceptación:**
- [ ] Commits atómicos con mensajes en español:
  - `"feat: implementación del motor de Estrategias Evolutivas"`
  - `"feat: ejecución de 120 experimentos (30 corridas × 4 variantes)"`
  - `"feat: generación de figuras de convergencia, gap y evolución de sigma"`
  - `"docs: reporte LaTeX con marco teórico, resultados y conclusiones"`
  - `"feat: sitio web Nuxt 3 con resultados interactivos"`
  - `"docs: README y requirements.txt"`
- [ ] Push a `main` en `https://github.com/jrebull/MIAAD_SMART_EstrategiasEvolutivas`
- [ ] Username: `jrebull`

---

### EPIC 7: Sitio Web de Resultados (Nuxt 3)

#### US-7.1 — Scaffold del proyecto Nuxt 3
**Como** alumno,
**quiero** un sitio web con Nuxt 3 dentro de `web/` que presente los resultados de los experimentos de forma interactiva,
**para** complementar el reporte LaTeX con una experiencia visual moderna y navegable.

**Criterios de aceptación:**
- [ ] Inicializar proyecto Nuxt 3 en `web/`:
  ```bash
  cd /Users/haowei/Documents/MIAAD/SMART/EstrategiasEvolutivas
  npx nuxi@latest init web
  cd web
  npm install
  ```
- [ ] `nuxt.config.ts` con configuración mínima:
  ```ts
  export default defineNuxtConfig({
    devtools: { enabled: true },
    app: {
      head: {
        title: 'EE: Isotropía vs Anisotropía — MIAAD UACJ',
        meta: [
          { name: 'description', content: 'Resultados de la práctica de Estrategias Evolutivas — Optimización Inteligente, MIAAD, UACJ' }
        ],
        link: [
          { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
        ]
      }
    },
    css: ['~/assets/css/main.css'],
    ssr: true,
    compatibilityDate: '2026-04-21'
  })
  ```
- [ ] Instalar dependencias: `@nuxtjs/tailwindcss` (o Tailwind manual), `chart.js`, `vue-chartjs`
- [ ] `package.json` con scripts: `dev`, `build`, `generate` (SSG para deploy estático)
- [ ] `.gitignore` de Nuxt: `node_modules/`, `.nuxt/`, `.output/`, `dist/`
- [ ] Verificar que `npm run dev` levanta sin errores en `http://localhost:3000`

---

#### US-7.2 — Exportación de datos para la web
**Como** sitio web,
**quiero** que `generate_figures.py` (o un script separado `export_web_data.py`) exporte los resultados como JSONs listos para consumo frontend,
**para** no depender de Python en el navegador.

**Criterios de aceptación:**
- [ ] Generar `web/public/data/convergence.json`:
  ```json
  {
    "generations": [0, 1, 2, ..., 499],
    "variants": {
      "plus_iso":   { "mean": [...], "std": [...] },
      "comma_iso":  { "mean": [...], "std": [...] },
      "plus_aniso": { "mean": [...], "std": [...] },
      "comma_aniso":{ "mean": [...], "std": [...] }
    }
  }
  ```
- [ ] Generar `web/public/data/summary.json`:
  ```json
  {
    "variants": [
      {
        "id": "plus_iso",
        "label": "(μ+λ) Isotrópica",
        "gap_mean": 0.0023,
        "gap_std": 0.0011,
        "success_rate": 96.67,
        "best_fitness_mean": 0.9977,
        "best_fitness_max": 0.9999
      },
      ...
    ]
  }
  ```
- [ ] Generar `web/public/data/sigma_evolution.json` con la evolución de σ por dimensión (una corrida representativa para isotrópica y anisotrópica)
- [ ] Copiar las PNGs de `Figures/` a `web/public/images/` como respaldo estático
- [ ] **REGLA:** Los JSONs se generan programáticamente desde `results/`, nunca a mano

---

#### US-7.3 — Páginas y componentes del sitio
**Como** visitante del sitio,
**quiero** navegar las secciones de resultados con gráficas interactivas y tablas bien formateadas,
**para** entender rápidamente el desempeño de cada variante.

**Criterios de aceptación:**

**Layout general (`app.vue` o `layouts/default.vue`):**
- [ ] Header con logo UACJ/MIAAD (o texto estilizado), título de la práctica, nombre del alumno y matrícula
- [ ] Navegación lateral o superior: Inicio, Problema, Resultados, Convergencia, Análisis de σ, Conclusiones
- [ ] Footer con: repo GitHub, fecha, créditos al Mtro. Porras
- [ ] Paleta UACJ: Azul `#003CA6`, Oro `#C8962E`, Gris `#555559`, fondo blanco
- [ ] Responsive (mobile-friendly con Tailwind)
- [ ] Dark mode toggle (opcional pero deseable)

**Páginas:**

1. **`pages/index.vue`** — Hero / Landing
   - [ ] Título grande: "Estrategias Evolutivas: Isotropía vs Anisotropía"
   - [ ] Subtítulo: "Evaluación de mecanismos de auto-adaptación y esquemas de selección en un paisaje mal condicionado"
   - [ ] Cards resumen de las 4 variantes con su Gap promedio y tasa de éxito (leer de `summary.json`)
   - [ ] Botón CTA: "Ver resultados completos"
   - [ ] Breve descripción del problema (función Elipsoide Invertido, D=10)
   - [ ] Renderizar ecuación con KaTeX o MathJax (instalar `katex` o usar CDN)

2. **`pages/problem.vue`** — Definición del Problema
   - [ ] Función objetivo con ecuación renderizada
   - [ ] Tabla de hiperparámetros (μ, λ, D, generaciones, corridas)
   - [ ] Explicación visual de isotrópico vs anisotrópico (puede ser imagen estática de `Figures/` o SVG inline)
   - [ ] Explicación de selección Plus vs Comma

3. **`pages/results.vue`** — Tabla de Resultados
   - [ ] Tabla HTML/Tailwind con datos de `summary.json`
   - [ ] Columnas: Variante, Gap Promedio ± Desv. Estándar, Tasa de Éxito (%), Mejor Fitness Promedio, Mejor Fitness Máximo
   - [ ] Highlighting de la mejor variante (verde) y la peor (rojo suave)
   - [ ] Gráfica de barras interactiva (Chart.js / vue-chartjs) del Gap por variante con barras de error
   - [ ] Gráfica de barras de tasa de éxito

4. **`pages/convergence.vue`** — Gráfica de Convergencia Interactiva
   - [ ] Gráfica de líneas (Chart.js) con las 4 curvas de convergencia promedio
   - [ ] Banda de ±1σ como fill con alpha bajo
   - [ ] Tooltips al pasar el mouse mostrando generación y fitness
   - [ ] Checkboxes para mostrar/ocultar variantes individualmente
   - [ ] Zoom / pan si Chart.js lo soporta (plugin `chartjs-plugin-zoom`)
   - [ ] Datos cargados desde `convergence.json` via `useFetch` o `useAsyncData`

5. **`pages/sigma.vue`** — Análisis de Evolución de σ
   - [ ] Gráfica de evolución de σ isotrópico (una curva)
   - [ ] Gráfica de evolución de σ anisotrópico (10 curvas, una por dimensión)
   - [ ] Leyenda indicando qué dimensión es cada curva
   - [ ] Narrativa breve: "Las dimensiones con gradiente empinado (i=1,2) convergen a σ menores que las de gradiente suave (i=9,10)"

6. **`pages/conclusions.vue`** — Conclusiones
   - [ ] Foto de Javier Rebull (misma `javiprofile.jpg`)
   - [ ] Texto de conclusiones similar al del LaTeX
   - [ ] Links a: repositorio GitHub, reporte PDF (si está disponible)
   - [ ] Referencias en formato IEEE (lista estática)

**Componentes reutilizables (`components/`):**
- [ ] `VariantCard.vue` — card con nombre de variante, gap, tasa de éxito, color
- [ ] `ConvergenceChart.vue` — wrapper de Chart.js para la gráfica de convergencia
- [ ] `BarChart.vue` — wrapper genérico de barras con barras de error
- [ ] `SigmaChart.vue` — gráfica de evolución de sigma
- [ ] `MathEquation.vue` — componente que renderiza LaTeX con KaTeX (o slot con CDN)
- [ ] `ResultsTable.vue` — tabla estilizada con datos de summary.json

---

#### US-7.4 — Build estático y preparación para deploy
**Como** alumno,
**quiero** generar un build estático del sitio (`nuxt generate`),
**para** poder desplegarlo en GitHub Pages, Vercel, Netlify o `miaad.dev`.

**Criterios de aceptación:**
- [ ] `npm run generate` produce carpeta `.output/public/` sin errores
- [ ] El sitio funciona abriendo `index.html` directamente (sin servidor) o con `npx serve .output/public`
- [ ] Todas las rutas pre-renderizadas: `/`, `/problem`, `/results`, `/convergence`, `/sigma`, `/conclusions`
- [ ] Los JSONs en `public/data/` se incluyen correctamente en el build
- [ ] Las imágenes en `public/images/` se incluyen en el build
- [ ] Agregar a `nuxt.config.ts` si se despliega en GitHub Pages:
  ```ts
  app: {
    baseURL: '/MIAAD_SMART_EstrategiasEvolutivas/'  // solo si es GitHub Pages
  }
  ```
- [ ] Commit: `"feat: sitio web Nuxt con resultados interactivos"`

---

## Reglas Globales (LÉELAS TODAS, CLAUDE CODE)

### Código
1. **Clean Code / SOLID:** Funciones cortas, nombres descriptivos, responsabilidad única.
2. **Tipado:** Type hints en todas las funciones públicas.
3. **Docstrings:** En español, formato Google-style.
4. **Sin hardcodeo:** Todos los hiperparámetros como argumentos con valores por defecto.
5. **Reproducibilidad:** Semillas deterministas, resultados guardados en disco.
6. **Eficiencia:** NumPy vectorizado donde sea posible. Nada de `for` pixel-a-pixel si se puede evitar.

### LaTeX
7. **No generar PDF.** Solo `.tex`. Javier compila en Overleaf.
8. **`\graphicspath{{../Figures/}}`** — las figuras viven en `Figures/` del proyecto; el LaTeX en `LaTeX/` las referencia con `../Figures/`.
9. **Cabecera idéntica** al ejemplo proporcionado (solo cambiar materia, profesor, título, fecha).
10. **Foto de Javier** (`javiprofile.jpg`) en la conclusión con `wrapfigure`.
11. **`\texorpdfstring`** en títulos con fórmulas.
12. **Formato numérico mexicano:** punto para decimales, coma para miles.

### Figuras
13. **Generadas programáticamente.** No dibujar a mano, no editar manualmente.
14. **300 DPI, fondo blanco, PNG.**
15. **Guardar figuras en `Figures/`** dentro del proyecto (`/Users/haowei/Documents/MIAAD/SMART/EstrategiasEvolutivas/Figures/`) — el LaTeX las referencia desde ahí.
16. **Paleta UACJ de alto contraste** para las 4 variantes.
17. **Etiquetas en español.**
18. **Legible impreso en blanco y negro** (usar estilos de línea diferentes además de color).

### Git
19. **Commits en español.** Username: `jrebull`.
20. **No commitear `.venv/`, `__pycache__/`, archivos binarios grandes, `node_modules/`, `.nuxt/`, `.output/`.**

### Web (Nuxt 3)
21. **Nuxt 3 con TypeScript.** `nuxt.config.ts`, componentes en `<script setup lang="ts">`.
22. **Tailwind CSS** para estilado. Paleta UACJ como custom colors en `tailwind.config`.
23. **Chart.js + vue-chartjs** para gráficas interactivas. No usar D3 (overkill para este caso).
24. **Datos desde JSONs estáticos** en `public/data/`, generados programáticamente. No hardcodear datos en componentes.
25. **SSG (`nuxt generate`)** para build estático desplegable en cualquier hosting.
26. **KaTeX** (CDN o npm) para renderizar ecuaciones matemáticas — no MathJax (más pesado).
27. **Responsive y accesible.** Mobile-first con Tailwind breakpoints. Alt text en imágenes.

---

## Orden de Ejecución Sugerido

```
1. US-1.1  → Crear estructura y entorno
2. US-1.2  → Configurar semillas
3. US-2.1  → Función objetivo + tests
4. US-2.2  → Representación del individuo
5. US-2.3  → Mutación isotrópica
6. US-2.4  → Mutación anisotrópica
7. US-2.5  → Selección Plus
8. US-2.6  → Selección Comma
9. US-2.7  → Loop evolutivo principal
10. US-3.1 → Ejecutar 120 experimentos
11. US-3.2 → Calcular métricas
12. US-4.1 → Gráfica de convergencia
13. US-4.2 → Gráficas de Gap y tasa de éxito
14. US-4.3 → Gráfica de evolución de σ
15. US-5.1 → Estructura LaTeX
16. US-5.2 → Contenido del reporte
17. US-5.3 → Referencias IEEE
18. US-6.1 → Validación cruzada
19. US-6.2 → README
20. US-7.1 → Scaffold Nuxt 3
21. US-7.2 → Exportar datos a JSON para la web
22. US-7.3 → Páginas y componentes del sitio
23. US-7.4 → Build estático y preparación para deploy
24. US-6.3 → Commits y push (AL FINAL, incluye todo)
```

---

## Checklist Final (Definition of Done)

- [ ] `run_experiments.py` ejecuta sin errores y produce `results/`
- [ ] `generate_figures.py` produce 4+ figuras en `Figures/`
- [ ] `main.tex` compila sin errores en Overleaf (verificar con `pdflatex` local si es posible)
- [ ] Tabla de resultados en LaTeX coincide con `results/summary.csv`
- [ ] Las 4 variantes están correctamente etiquetadas en gráficas y tablas
- [ ] JSONs en `web/public/data/` generados desde `results/` (no hardcodeados)
- [ ] `npm run dev` en `web/` levanta sin errores
- [ ] `npm run generate` en `web/` produce build estático funcional
- [ ] Todas las páginas del sitio Nuxt cargan y muestran datos correctos
- [ ] Gráficas interactivas (Chart.js) funcionan con tooltips y toggle de variantes
- [ ] README.md completo y profesional (incluye sección del sitio web)
- [ ] Repositorio pusheado a GitHub con historial limpio
- [ ] requirements.txt permite recrear el entorno Python desde cero
- [ ] `package.json` permite recrear el entorno Node desde cero

---

*SuperPrompt generado para Claude Code — Proyecto MIAAD Optimización Inteligente, abril 2026.*
