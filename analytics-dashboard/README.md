# Dashboard de Análisis Emocional con IA

### Privacy-First Analytics & Visualization Tool

> **Status:** Functional MVP
> **Stack:** Python • Streamlit • Pandas • Plotly
> **Context:** Post-hoc analysis for Offline Voice Assistant

Este proyecto es una suite de visualización interactiva diseñada para interpretar los registros biométricos y emocionales generados por el asistente de voz en el borde (Raspberry Pi). Permite a terapeutas o investigadores auditar las sesiones sin comprometer la privacidad del usuario, ya que el procesamiento de datos ocurre 100% en local (`localhost`).

## Objetivo del Sistema

Transformar datos crudos (logs CSV) en insights accionables sobre el estado anímico del usuario a lo largo del tiempo, identificando patrones de estrés o bienestar mediante análisis de series temporales y NLP.

## Características Principales

* **Zero-Cloud Processing:** El dashboard se ejecuta localmente en el navegador, garantizando que el historial sensible nunca salga de la PC del auditor.
* **Métricas Temporales:** Gráficos interactivos de evolución emocional (Día/Hora).
* **Análisis Semántico:** Nubes de palabras y frecuencia de términos para detectar "triggers" (motivos recurrentes de ansiedad/alegría).
* **Filtros Dinámicos:** Segmentación de datos por usuario, fecha o tipo de emoción detectada.

## Tech Stack

| Capa | Tecnología | Uso |
| :--- | :--- | :--- |
| **Frontend** | **Streamlit** | Interfaz web reactiva y rápida para Data Science. |
| **Procesamiento** | **Pandas** | Manipulación y limpieza de dataframes estructurados. |
| **Visualización** | **Plotly / Altair** | Gráficos interactivos y mapas de calor. |
| **Input** | **CSV Flatfile** | Ingesta de datos estructurados desde el dispositivo Edge. |

## Configuración del Entorno (Local)

Requisitos: Anaconda/Miniconda o Python 3.10+.

### 1. Instalación

Clona el repositorio y crea un entorno aislado para evitar conflictos de dependencias.

# 1. Crear entorno con Conda

```bash
conda create -n dashboard_ai_env python=3.10
conda activate dashboard_ai_env
```

# 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecución

Coloca el archivo registro_emociones.csv generado por la Raspberry Pi en la carpeta raíz (o usa el dataset sintético de prueba provisto en /data).

```bash
streamlit run dashboard.py
```

El sistema abrirá automáticamente el navegador en <http://localhost:8501>.

# Estructura de Datos Esperada

El sistema ingesta archivos .csv estandarizados por el módulo de Edge AI. El esquema requerido es

Columna Tipo Descripción
Timestamp Datetime Marca temporal exacta del evento.
Usuario String ID anonimizado del sujeto.
Emocion Categorical Ej: "Alegría", "Estrés", "Neutral".
Motivo String (NLP) Keywords extraídas del prompt del usuario.
Respuesta_AI Text Feedback otorgado por el asistente.
