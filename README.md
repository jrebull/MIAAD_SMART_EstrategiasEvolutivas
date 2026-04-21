# Práctica de Estrategias Evolutivas: Isotropía vs Anisotropía

**Maestría en Inteligencia Artificial y Analítica de Datos (MIAAD)** — Universidad Autónoma de Ciudad Juárez (UACJ)
**Materia:** Optimización Inteligente — Mtro. Raúl Gibrán Porras Alaniz
**Alumno:** Javier Augusto Rebull Saucedo (Matrícula 263483)
**Fecha de entrega:** 01 de mayo de 2026

---

## Descripción

Este proyecto implementa y compara cuatro variantes de Estrategias Evolutivas (EE) sobre la función **Elipsoide Invertido** (un paisaje mal condicionado), para evaluar el efecto de:

1. El esquema de selección: **(μ + λ)** elitista vs **(μ , λ)** con reemplazo total.
2. El mecanismo de auto-adaptación: **isotrópico** (un solo σ) vs **anisotrópico** (un σ por dimensión).

### Función objetivo (MAXIMIZACIÓN)

$$f(\mathbf{x}) = \exp\left(-\sum_{i=1}^{D} \frac{(x_i - 2.0)^2}{i}\right), \quad D=10, \quad x_i \in [-5, 5]$$

El denominador $i$ hace que cada dimensión tenga una escala distinta: las primeras son empinadas y las últimas suaves. Esto favorece la mutación anisotrópica.

### Variantes evaluadas

| ID | Esquema | Mutación | Clave |
|----|---------|----------|-------|
| V1 | (μ + λ) | Isotrópica | `plus_iso` |
| V2 | (μ , λ) | Isotrópica | `comma_iso` |
| V3 | (μ + λ) | Anisotrópica | `plus_aniso` |
| V4 | (μ , λ) | Anisotrópica | `comma_aniso` |

### Hiperparámetros

μ = 20, λ = 100, Generaciones = 500, D = 10, Corridas independientes = 30 por variante (total **120 experimentos**).

---

## Requisitos

- Python ≥ 3.11 (probado con 3.14)
- Node.js ≥ 18 (sólo para el sitio Nuxt 3 de `web/`)
- macOS / Linux (Windows funciona pero no se ha probado)

---

## Instalación

```bash
cd /Users/haowei/Documents/MIAAD/SMART/EstrategiasEvolutivas
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Ejecución

### 1. Ejecutar los 120 experimentos

```bash
source .venv/bin/activate
python run_experiments.py
```

Esto genera `results/convergence_data.csv` y `results/summary.csv`.

### 2. Generar figuras para el reporte

```bash
python generate_figures.py
```

Produce los PNG (300 DPI) en `Figures/`:

- `convergence_comparison.png` — convergencia promedio de las 4 variantes (banda ±1σ).
- `convergence_log.png` — convergencia del Gap en escala logarítmica.
- `gap_comparison.png` — Gap final promedio con barras de error (log).
- `success_rate.png` — tasa de éxito por variante.
- `generations_to_success.png` — boxplot de generaciones hasta cruzar f≥0.95.
- `sigma_evolution.png` — evolución de los parámetros de auto-adaptación σ.

### 3. Exportar datos para el sitio web

```bash
python export_web_data.py
```

Genera los JSONs en `web/public/data/` (convergence, summary, sigma_evolution) y copia los PNG de `Figures/` a `web/public/images/`.

### 4. Correr tests

```bash
pytest tests/ -v
```

### 5. Sitio web con resultados interactivos

```bash
cd web
npm install
npm run dev      # desarrollo en http://localhost:3000
npm run generate # build estático en .output/public/
```

---

## Estructura del proyecto

```
EstrategiasEvolutivas/
├── src/
│   ├── __init__.py
│   ├── evolution_strategy.py    # Motor principal
│   ├── fitness.py               # Función objetivo
│   ├── operators.py             # Mutación, selección, auto-adaptación
│   └── experiment.py            # Orquestador de corridas
├── tests/                       # Pruebas unitarias (pytest)
├── Figures/                     # PNGs generadas (300 DPI)
├── LaTeX/
│   └── main.tex                 # Reporte (compila en Overleaf)
├── web/                         # Sitio Nuxt 3 con resultados interactivos
├── results/                     # CSV / JSON con resultados crudos y agregados
│   ├── convergence_data.csv     # fitness por variante × corrida × generación
│   ├── summary.csv              # final_best_fitness, gap, success por corrida
│   ├── per_variant_summary.json # estadísticas agregadas por variante
│   └── sigma_evolution.json     # historial de σ promediado sobre las 30 corridas
├── run_experiments.py           # Script principal: 120 ejecuciones
├── generate_figures.py          # Genera las 6 figuras del reporte
├── export_web_data.py           # Exporta JSONs + PNGs al sitio Nuxt
├── requirements.txt
└── README.md
```

---

## Semillas y reproducibilidad

Las 30 corridas por variante usan semillas deterministas `seeds = [42 + i for i in range(30)]`. Dos ejecuciones consecutivas del mismo script producen resultados **idénticos bit a bit**.

---

## Resultados

Los valores numéricos (Gap promedio, desviación estándar, tasa de éxito) se generan **programáticamente** desde `results/summary.csv` y se inyectan en:

- El reporte LaTeX (`LaTeX/main.tex`, comentarios con las fuentes de datos).
- El sitio Nuxt 3 (`web/public/data/*.json`).

> Regla: prohibido hardcodear métricas en figuras, tablas o textos; todo se regenera desde los resultados crudos.

---

## Referencias principales

1. Rechenberg, I. *Evolutionsstrategie: Optimierung technischer Systeme nach Prinzipien der biologischen Evolution*, Frommann-Holzboog, 1973.
2. Schwefel, H.-P. *Evolution and Optimum Seeking*, Wiley, 1995.
3. Beyer, H.-G. & Schwefel, H.-P. *Evolution Strategies — A Comprehensive Introduction*, Natural Computing 1, 3–52, 2002.
4. Eiben, A.E. & Smith, J.E. *Introduction to Evolutionary Computing*, Springer, 2.ª ed., 2015.

Lista completa en la sección de referencias del reporte LaTeX.

---

## Repositorio

<https://github.com/jrebull/MIAAD_SMART_EstrategiasEvolutivas>
