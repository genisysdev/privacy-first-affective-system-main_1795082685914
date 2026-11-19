# Sistema de Análisis Afectivo Privado (Edge Computing)

### Offline Voice Assistant & Emotion Tracker on Raspberry Pi 3

> **Status:** Functional Prototype (R&D)
> **Device:** Raspberry Pi 3 B+ (1GB RAM)
> **Privacy:** 100% Offline / Air-gapped

Este proyecto implementa un asistente virtual empático diseñado bajo el paradigma **Privacy-First**. A diferencia de Alexa o Google Assistant, todo el procesamiento (reconocimiento de voz, inferencia de LLM y síntesis de voz) ocurre localmente en el dispositivo, garantizando que ni una sola palabra salga de la habitación.

El sistema interactúa con el usuario, registra metadatos emocionales en un log local (`csv`) y proporciona feedback visual mediante una interfaz animada en framebuffer directo.

## Características Clave
* **100% Local & Offline:** No requiere conexión a internet.
* **Hardware Limitado:** Optimizado para correr en ARM64 con solo 1GB de RAM.
* **Latencia Controlada:** Uso de modelos cuantizados (GGUF) y motores C++ compilados.
* **Feedback Multimodal:** Respuesta por voz neuronal y expresiones faciales en pantalla HDMI.

## Stack Tecnológico

Para lograr inteligencia artificial generativa en una Raspberry Pi 3, se seleccionó una arquitectura de componentes ultra-ligeros:

| Capa | Tecnología | Función |
| :--- | :--- | :--- |
| **Oído (ASR)** | **Vosk (Small-ES)** | Reconocimiento de voz offline ligero y rápido. |
| **Cerebro (SLM)** | **Qwen2.5-0.5B (GGUF q4)** | Modelo de lenguaje pequeño (0.5B params) ejecutado vía `llama.cpp`. |
| **Voz (TTS)** | **Piper (Neural)** | Síntesis de voz en español de baja latencia. |
| **Cara (Visual)** | **FBI (Linux Framebuffer)** | Renderizado de imágenes directo a GPU (sin entorno de escritorio X11). |
| **Almacenamiento** | **SSD Swap** | Memoria virtual crítica para compensar la falta de RAM física. |

## Requisitos de Hardware
Este sistema **NO** funciona con tarjetas MicroSD estándar debido a la alta tasa de I/O requerida por el modelo de IA.

1.  **Raspberry Pi 3 Model B/B+**.
2.  **Disco SSD Externo** (Indispensable para Swap y velocidad).
3.  Micrófono USB y Parlante (Jack 3.5mm).
4.  Pantalla HDMI.

## Instalación y Despliegue (Resumen Técnico)

### 1. Preparación del Sistema (OS & Swap)
El sistema corre sobre **Raspberry Pi OS Lite (64-bit)**. Es crítico ampliar la memoria Swap en el SSD para evitar el *Out of Memory (OOM)* al cargar el modelo Qwen.


#### Aumentar SWAP a 2GB (Crítico para RPi 3)

```bash
sudo nano /etc/dphys-swapfile
```

#### Cambiar CONF_SWAPSIZE=100 a CONF_SWAPSIZE=2048

```bash
sudo /etc/init.d/dphys-swapfile restart
```

### 2. Configuración de Entorno
#### Instalación de dependencias de sistema para compilación ARM.

```bash
sudo apt install -y python3-pip python3-venv libopenblas-dev libportaudio2 fbi
python3 -m venv venv
source venv/bin/activate
```

### 3. Compilación de llama.cpp (Optimizado)
#### Compilamos el motor de inferencia específicamente para la arquitectura de la Pi.

```bash
CMAKE_ARGS="-DGGML_BLAS=ON -DGGML_VENDOR=OpenBLAS" pip install llama-cpp-python
```

### 4. Estructura de Datos
#### El sistema genera automáticamente un archivo de registro estructurado para su posterior análisis.

Output: registro_emociones.csv
Formato: Timestamp; Usuario; Emoción_Detectada; Prompt_Context; Respuesta_IA

## Arquitectura Lógica

```bash
graph TD
    User((Usuario)) -->|Voz| Mic[Micrófono USB]
    Mic -->|Audio Stream| ASR[Vosk ASR]
    ASR -->|Texto| Orchestrator[Python Controller]
    Orchestrator -->|Prompt + Contexto| LLM[Qwen 0.5B GGUF]
    LLM -->|Texto Generado| Orchestrator
    Orchestrator -->|Texto| TTS[Piper TTS]
    Orchestrator -->|Estado Emocional| CSV[(registro.csv)]
    Orchestrator -->|Estado Visual| FBI[Pantalla HDMI]
    TTS -->|Audio| Speaker[Parlante]
    FBI -->|Cara Robot| User
```
