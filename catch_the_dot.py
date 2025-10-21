#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
%--------------------------------------------------------------------------%
%------- ------------------------------------------------------------------%
%------- Coceptos básicos de PDI (adaptado) -------------------------------%
%------- Por: <Daniel Rúa>    <cdaniel.rua1@udea.edu.co> -----------------------%
%------- Curso: Procesamiento de Imágenes y Visión Artificial -------------%
%------- Trabajo: Catch the Dot (Juego interactivo con cámara) ------------%
%------- Fecha: octubre 2025 -----------------------------------------------%
%--------------------------------------------------------------------------%

%--------------------------------------------------------------------------%
%--1. Inicializo el sistema -----------------------------------------------%
%--------------------------------------------------------------------------%
"""
import cv2
import numpy as np
import time
import random
import math

# ------------------- Configuraciones iniciales -----------------------------
CAM_INDEX = 0          # índice de la cámara (0 por defecto)
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
GAME_DURATION = 60     # duración del juego en segundos
TARGET_RADIUS = 30     # radio del objetivo en píxeles
HIT_DISTANCE = 40      # distancia para considerar "colisión" (px)

# --------------------------------------------------------------------------
#-- 2. Funciones utilitarias -----------------------------------------------
# --------------------------------------------------------------------------

def nothing(x):
    pass

def create_hsv_trackbars(window_name="Calibrar color"):
    cv2.namedWindow(window_name)
    cv2.createTrackbar("H_min", window_name, 0, 179, nothing)
    cv2.createTrackbar("H_max", window_name, 179, 179, nothing)
    cv2.createTrackbar("S_min", window_name, 50, 255, nothing)
    cv2.createTrackbar("S_max", window_name, 255, 255, nothing)
    cv2.createTrackbar("V_min", window_name, 50, 255, nothing)
    cv2.createTrackbar("V_max", window_name, 255, 255, nothing)

def read_hsv_trackbars(window_name="Calibrar color"):
    hmin = cv2.getTrackbarPos("H_min", window_name)
    hmax = cv2.getTrackbarPos("H_max", window_name)
    smin = cv2.getTrackbarPos("S_min", window_name)
    smax = cv2.getTrackbarPos("S_max", window_name)
    vmin = cv2.getTrackbarPos("V_min", window_name)
    vmax = cv2.getTrackbarPos("V_max", window_name)
    lower = np.array([hmin, smin, vmin])
    upper = np.array([hmax, smax, vmax])
    return lower, upper

def distance(p1, p2):
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

def spawn_target(w, h, margin=50):
    x = random.randint(margin, w - margin)
    y = random.randint(margin, h - margin)
    return (x, y)

# --------------------------------------------------------------------------
#-- 3. Lógica del juego (inicio del sistema, captura y loop principal) -----
# --------------------------------------------------------------------------

def main():
    # Inicializa cámara
    cap = cv2.VideoCapture(CAM_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    if not cap.isOpened():
        print("No se pudo abrir la cámara. Revisa el índice o permisos.")
        return

    # Crear ventana de calibración y trackbars para seleccionar color
    calib_win = "Calibrar color"
    create_hsv_trackbars(calib_win)
    print("Ajusta los trackbars para calibrar el color del objeto que usarás.")
    time.sleep(0.5)

    # Estado del juego
    score = 0
    target_pos = spawn_target(FRAME_WIDTH, FRAME_HEIGHT)
    start_time = None
    game_running = False

    # Bucle principal
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error leyendo cámara.")
            break

        frame = cv2.flip(frame, 1)  # espejo para interacción natural
        frame_blur = cv2.GaussianBlur(frame, (7,7), 0)
        hsv = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2HSV)

        # Leer parámetros HSV desde trackbars
        lower_hsv, upper_hsv = read_hsv_trackbars(calib_win)

        # Segmentación por histograma (máscara binaria)
        mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
        # Operaciones morfológicas para limpiar máscara
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Encontrar contornos para hallar el objeto
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        center = None

        if contours:
            # Tomar el contorno más grande (suponemos es el objeto)
            c = max(contours, key=cv2.contourArea)
            # Ignorar si el contorno es muy pequeño (ruido)
            if cv2.contourArea(c) > 500:
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                if M["m00"] > 0:
                    center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
                    # Dibujar en la cámara el seguimiento
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,255), 2)
                    cv2.circle(frame, center, 5, (0,0,255), -1)

        # Dibujar objetivo en la pantalla (acción)
        cv2.circle(frame, target_pos, TARGET_RADIUS, (255,0,0), -1)
        cv2.putText(frame, f"Puntaje: {score}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 2)

        # Manejo de inicio/detención del juego
        if not game_running:
            cv2.putText(frame, "Presiona 's' para iniciar (o 'q' para salir)", (10,460),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
        else:
            elapsed = time.time() - start_time
            remain = max(0, int(GAME_DURATION - elapsed))
            cv2.putText(frame, f"Tiempo: {remain}s", (450,30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,255), 2)
            if remain <= 0:
                game_running = False
                # Fin de la partida: mostrar mensaje
                cv2.putText(frame, "FIN! Presiona 'r' para reiniciar o 'q' para salir", (10,460),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

        # Comprobar colisión
        if center is not None and game_running:
            if distance(center, target_pos) <= HIT_DISTANCE:
                score += 1
                # Cuando haya colisión, generar nuevo objetivo y pequeña 'retroalimentación' visual
                target_pos = spawn_target(FRAME_WIDTH, FRAME_HEIGHT)
                # (Opcional) Puedes guardar el tiempo de impacto, mostrar animación, etc.

        # Mostrar máscara reducida en la esquina para depuración (opcional)
        mask_small = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        mask_small = cv2.resize(mask_small, (160,120))
        frame[0:120, FRAME_WIDTH-160:FRAME_WIDTH] = mask_small

        # Mostrar todo en ventana principal
        cv2.imshow("Catch the Dot - Juego", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s') and not game_running:
            # Iniciar el juego
            score = 0
            target_pos = spawn_target(FRAME_WIDTH, FRAME_HEIGHT)
            start_time = time.time()
            game_running = True
        elif key == ord('r'):
            # Reiniciar
            score = 0
            target_pos = spawn_target(FRAME_WIDTH, FRAME_HEIGHT)
            start_time = time.time()
            game_running = True

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
