# Sistema de Control de Asistencia con Reconocimiento Facial

## 📋 Descripción

Proyecto educativo de **Visión Computacional** que implementa un sistema de control de asistencia mediante reconocimiento facial en tiempo real. Utiliza la cámara web del computador para detectar y reconocer rostros previamente registrados.

Este es un proyecto introductorio para comprender los fundamentos de visión por computadora antes de avanzar a redes neuronales convolucionales (CNN) y Deep Learning.

## 🎯 Objetivos de Aprendizaje

- Comprender cómo funcionan los sistemas de detección facial
- Trabajar con landmarks faciales usando MediaPipe
- Implementar comparación de características faciales
- Integrar visión por computadora con registro de datos (CSV)
- Practicar con OpenCV y procesamiento de imágenes en tiempo real

## 🛠️ Tecnologías Utilizadas

- **Python 3.x** - Lenguaje de programación
- **OpenCV** - Procesamiento de video y visión por computadora
- **MediaPipe** - Detección facial y extracción de landmarks
- **NumPy** - Cálculos matemáticos y comparación de vectores

## 📦 Requisitos del Sistema

- Python 3.8 o superior
- Webcam funcional
- Windows / Linux / macOS

## 🚀 Instalación

### Paso 1: Clonar o Descargar el Repositorio

```bash
git clone https://github.com/jasaresearch/vision-computacional-asistencia.git
cd vision-computacional-asistencia
```

O descarga el ZIP y descomprímelo.

### Paso 2: Crear Entorno Virtual (Recomendado)

**En Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

**En Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

**⚠️ Importante:** Este proyecto requiere `mediapipe==0.10.14`. Las versiones 1.x NO son compatibles con este código.

## 📸 Preparar tu Foto de Referencia

1. Ve a la carpeta `fotos/`
2. Agrega una foto tuya con las siguientes características:
   - **Nombre del archivo:** `TuNombre.jpg` (ejemplo: `Maria_Garcia.jpg`)
   - **Formato:** JPG o PNG
   - **Requisitos de la foto:**
     - Una sola persona en la imagen
     - Rostro visible frontalmente
     - Buena iluminación
     - Tamaño recomendado: 640x480 o superior

3. Ejemplo:
   ```
   fotos/
   ├── Maria_Garcia.jpg
   ├── Juan_Perez.jpg
   └── Ana_Lopez.jpg
   ```

## ▶️ Ejecutar el Sistema

```bash
python AsistenciaJASA.py
```

### ¿Cómo Funciona?

1. El programa carga todas las fotos de la carpeta `fotos/` y extrae los landmarks faciales
2. Se abre la webcam de tu computador
3. Cuando detecta un rostro, lo compara con los rostros conocidos
4. Si hay coincidencia (similitud > 50%), muestra tu nombre en **verde**
5. Si no te reconoce, muestra "DESCONOCIDO" en **rojo**
6. La asistencia se registra automáticamente en `Attendace.csv`

### Controles

- **Presiona `q`** para salir del programa

## 📊 Archivo de Registro

El archivo `Attendace.csv` guarda:
- **Nombre:** Identificación de la persona
- **Tiempo:** Hora de registro (formato HH:MM:SS)

Los registros se agregan automáticamente cuando eres reconocido por primera vez en cada sesión.

## 🔧 Solución de Problemas

### "No se detectó rostro en [foto]"
- Asegúrate de que la foto tenga buena iluminación
- Verifica que el rostro esté visible frontalmente
- Intenta con una foto diferente

### La webcam no se abre
- Verifica que tu webcam esté conectada y funcional
- Cierra otras aplicaciones que puedan estar usando la cámara
- En Windows, verifica los permisos de cámara en Configuración

### No me reconoce aunque agregué mi foto
- Asegúrate de que tu foto esté en la carpeta `fotos/`
- Verifica que la iluminación actual sea similar a la de la foto
- Prueba con diferentes ángulos frente a la cámara
- El umbral de similitud es del 50%, puedes ajustarlo en el código (línea ~160)

## 📚 Estructura del Proyecto

```
imagenesControlAsistencia/
│
├── fotos/                    # Carpeta con fotos de referencia
│   ├── ejemplo1.jpg
│   └── ejemplo2.jpg
│
├── AsistenciaJASA.py        # Código principal del sistema
├── Attendace.csv            # Registro de asistencias
├── requirements.txt         # Dependencias del proyecto
├── .gitignore              # Archivos ignorados por Git
└── README.md               # Este archivo
```

## 🎓 Para Estudiantes

### Ejercicios Propuestos

1. **Ajustar el umbral de similitud** - Modifica la línea del threshold y observa cómo afecta el reconocimiento
2. **Agregar más información al CSV** - Incluye fecha completa, no solo hora
3. **Contar el número de detecciones** - Lleva estadísticas de cuántas veces aparece cada persona
4. **Mejorar la interfaz visual** - Agrega más información en pantalla (FPS, número de rostros conocidos, etc.)

### Conceptos Clave a Investigar

- ¿Qué son los facial landmarks?
- ¿Cómo funciona la distancia euclidiana?
- ¿Qué es un embedding facial?
- Diferencia entre detección, reconocimiento y verificación facial

## 👨‍🏫 Contacto

Profesor: Jose Antonio Solano  
Curso: Visión Computacional  
Universidad: Universidad de Antioquia

## 📄 Licencia

Este proyecto es material educativo para el curso de Visión Computacional.

---

**Nota:** Este es un proyecto didáctico. Para sistemas de producción se recomiendan técnicas más robustas como redes neuronales profundas (FaceNet, ArcFace, etc.).
