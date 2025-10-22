# 🎮 Catch the Dot
Juego interactivo con cámara desarrollado en Python y OpenCV.

---

## 🎥 Video de demostración

Haz clic en la imagen para ver el video:

[![Ver video en YouTube](https://img.youtube.com/vi/O1U1CJaBNZ8/0.jpg)](https://www.youtube.com/watch?v=O1U1CJaBNZ8)


## 🧠 Descripción general
**Catch the Dot** es un juego de visión por computador que detecta un objeto de color frente a la cámara.  
El jugador debe mover ese objeto (por ejemplo, una pelota o una tarjeta de color) para atrapar un punto azul que aparece en pantalla.  
Cada vez que lo alcanza, gana un punto y el objetivo cambia de lugar.

---

## ⚙️ Requisitos
- Python 3.8 o superior  
- Librerías:
  - `opencv-python`
  - `numpy`

---

## 🚀 Instalación
1. Clonar o descargar este repositorio.  
2. (Opcional) Crear entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   .\venv\Scripts\activate    # Windows
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Ejecución
Ejecuta el archivo principal:
```bash
python catch_the_dot.py
```

---

## 🎯 Cómo jugar
1. **Muestra un objeto de color** frente a la cámara (por ejemplo una tarjeta amarilla o roja).  
2. Ajusta los **sliders HSV** (Hue, Saturation, Value) en la ventana “Calibrar color” hasta que el programa detecte correctamente el color del objeto.  
3. Presiona la tecla **`s`** para comenzar el juego.  
4. Mueve el objeto frente a la cámara para **atrapar el punto azul** en la pantalla.  
5. Cada vez que el objeto toca el punto, **ganas un punto** y el objetivo aparece en otra posición.  
6. El juego dura **60 segundos**.  
7. Puedes:
   - Presionar **`r`** para reiniciar,  
   - Presionar **`q`** para salir.

---

## 📊 Indicadores en pantalla
- **Puntaje** (arriba a la izquierda).  
- **Tiempo restante** (arriba a la derecha).  
- **Máscara de detección** (arriba a la derecha pequeña ventana).  

---

## 🧩 Conceptos aplicados
- Captura y procesamiento de video en tiempo real.  
- Conversión de color (BGR → HSV).  
- Segmentación de color mediante umbrales.  
- Extracción de características (centroide).  
- Detección de colisión geométrica.  

---

## 📈 Resultados esperados
- Detección estable en condiciones de iluminación normal.  
- Interacción fluida (~25 fps).  
- Experiencia de juego intuitiva sin necesidad de teclado ni ratón.

---

## 👨‍💻 Autores
- **Carlos Daniel Rúa Gutiérrez**

Profesor: **David Fernández**  
Universidad de Antioquia – Facultad de Ingeniería  
Curso: **Procesamiento Digital de Imágenes y Visión Artificial (2025-2)**

---

## 📚 Referencias
- OpenCV Documentation — https://docs.opencv.org  
- LearnOpenCV: Color Detection and Object Tracking  
- Gonzalez & Woods — *Digital Image Processing*, 4th Ed.
