# Sistema de Análisis Afectivo Privado (Edge Computing)

### Privacy-First Voice Emotion Recognition & Analytics Ecosystem

> **Architecture:** Edge AI (Raspberry Pi) + Local Analytics (Streamlit)
> **Focus:** Data Privacy, Offline Processing, Mental Health Monitoring.

Este repositorio contiene la implementación completa de un sistema de biofeedback auditivo que respeta la privacidad del usuario. El sistema se divide en dos módulos independientes que se comunican mediante registros planos (CSV), garantizando que **ningún dato sensible salga del entorno local**.

---

![Programmer portrait - AI-generated](<assets/Privacy-First Voice Emotion Recognition_banner.png>)
*Image generated with Google AI.*

![Programmer portrait - AI-generated](<assets/Privacy-First Voice Emotion Recognition.png>)
*Image generated with Google AI.*

![Programmer portrait - AI-generated](<assets/Privacy-First Voice Emotion Recognition_1.png>)
*Image generated with Google AI.*

## Módulos del Sistema

### 1. [Edge Node (Hardware)](./edge-node)

El dispositivo físico que interactúa con el usuario.

* **Tech:** Raspberry Pi 3, Vosk, Qwen 0.5B, Piper TTS.
* **Función:** Asistente de voz offline, detección de emociones y registro de sesiones.
* **[Ver Documentación Técnica ->](./edge-node/README.md)**

### 2. [Analytics Dashboard (Software)](./analytics-dashboard)

La suite de auditoría y visualización para profesionales.

* **Tech:** Python, Streamlit, Pandas, Plotly.
* **Función:** Análisis post-hoc de tendencias emocionales y patrones semánticos.
* **[Ver Documentación Técnica ->](./analytics-dashboard/README.md)**

---

## Flujo de Datos (Data Flow)

1. **Captura:** El `edge-node` procesa la voz y detecta la emoción en tiempo real.
2. **Almacenamiento:** Se genera un log local cifrado `registro_emociones.csv`.
3. **Ingesta:** El `analytics-dashboard` lee este archivo (sin subirlo a la nube) para generar visualizaciones.

---
