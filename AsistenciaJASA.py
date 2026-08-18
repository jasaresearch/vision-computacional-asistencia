import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime
import os

# Configuración de MediaPipe para detección facial
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Ruta de las fotos conocidas
path = 'fotos'
imagenes = []
classNombres = []
face_embeddings = []

print("Cargando imágenes de referencia...")
myList = os.listdir(path)

def extract_face_features(image, face_mesh):
    """Extrae características faciales usando MediaPipe Face Mesh"""
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(img_rgb)
    
    if results.multi_face_landmarks:
        # Obtener landmarks del primer rostro detectado
        landmarks = results.multi_face_landmarks[0]
        # Convertir landmarks a array numpy (coordenadas normalizadas)
        features = []
        for landmark in landmarks.landmark:
            features.extend([landmark.x, landmark.y, landmark.z])
        return np.array(features)
    return None

def calculate_similarity(features1, features2):
    """Calcula similitud entre dos sets de características faciales"""
    if features1 is None or features2 is None:
        return 0
    # Distancia euclidiana normalizada
    distance = np.linalg.norm(features1 - features2)
    # Convertir a similitud (0-1, donde 1 es idéntico)
    similarity = 1 / (1 + distance)
    return similarity

# Cargar imágenes y extraer características
with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    min_detection_confidence=0.5) as face_mesh:
    
    for cl in myList:
        img_path = f'{path}/{cl}'
        curImg = cv2.imread(img_path)
        if curImg is not None:
            features = extract_face_features(curImg, face_mesh)
            if features is not None:
                imagenes.append(curImg)
                classNombres.append(os.path.splitext(cl)[0])
                face_embeddings.append(features)
                print(f"[OK] Cargada: {os.path.splitext(cl)[0]}")
            else:
                print(f"[X] No se detectó rostro en: {cl}")
        else:
            print(f"[ERROR] Error al cargar: {cl}")

print(f"\nTotal de rostros conocidos: {len(classNombres)}")
print(f"Nombres: {classNombres}\n")

def MarkAttendace(name):
    """Registra asistencia en el archivo CSV"""
    with open('Attendace.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
            print(f"[OK] Asistencia registrada: {name} a las {dtString}")

# Iniciar captura de webcam
print("Iniciando webcam...")
print("Presiona 'q' para salir\n")
cap = cv2.VideoCapture(0)

# Configurar MediaPipe para detección en tiempo real
with mp_face_detection.FaceDetection(
    min_detection_confidence=0.5) as face_detection, \
     mp_face_mesh.FaceMesh(
    max_num_faces=5,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh_video:
    
    frame_count = 0
    process_every_n_frames = 2  # Procesar cada 2 frames para mejor rendimiento
    last_recognized = {}  # Diccionario para rastrear últimas detecciones {person_id: (name, frames_count)}
    
    while True:
        success, img = cap.read()
        if not success:
            print("Error al capturar imagen de la webcam")
            break
        
        frame_count += 1
        
        # Procesar solo cada N frames para mejorar rendimiento
        if frame_count % process_every_n_frames != 0:
            cv2.imshow('Sistema de Asistencia - MediaPipe', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue
        
        # Convertir a RGB para MediaPipe
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Detectar rostros
        detection_results = face_detection.process(img_rgb)
        mesh_results = face_mesh_video.process(img_rgb)
        
        if detection_results.detections and mesh_results.multi_face_landmarks:
            for detection, face_landmarks in zip(detection_results.detections, 
                                                 mesh_results.multi_face_landmarks):
                # Obtener bounding box
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = img.shape
                x1 = int(bboxC.xmin * iw)
                y1 = int(bboxC.ymin * ih)
                w = int(bboxC.width * iw)
                h = int(bboxC.height * ih)
                x2 = x1 + w
                y2 = y1 + h
                
                # Asegurar que las coordenadas están dentro de los límites
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(iw, x2), min(ih, y2)
                
                # Extraer características del rostro detectado
                current_features = []
                for landmark in face_landmarks.landmark:
                    current_features.extend([landmark.x, landmark.y, landmark.z])
                current_features = np.array(current_features)
                
                # Comparar con rostros conocidos
                best_match_idx = -1
                best_similarity = 0
                threshold = 0.50  # Umbral de similitud (ajustado para mejor precisión)
                
                for idx, known_features in enumerate(face_embeddings):
                    similarity = calculate_similarity(current_features, known_features)
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_match_idx = idx
                
                # Determinar si hay coincidencia
                if best_similarity > threshold and best_match_idx != -1:
                    name = classNombres[best_match_idx].upper()
                    color = (0, 255, 0)  # Verde para reconocido
                    confidence = int(best_similarity * 100)
                    label = f"{name} ({confidence}%)"
                    
                    # Registrar asistencia
                    MarkAttendace(name)
                else:
                    name = "DESCONOCIDO"
                    color = (0, 0, 255)  # Rojo para desconocido
                    label = name
                
                # Dibujar rectángulo y nombre (mejorado para mejor visibilidad)
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 4)  # Rectángulo más grueso
                cv2.rectangle(img, (x1, y2 - 45), (x2, y2), color, cv2.FILLED)  # Barra más grande
                cv2.putText(img, label, (x1 + 6, y2 - 10), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)  # Texto más grande
        
        # Mostrar imagen
        cv2.imshow('Sistema de Asistencia - MediaPipe', img)
        
        # Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\nCerrando sistema...")
            break

cap.release()
cv2.destroyAllWindows()
print("Sistema cerrado correctamente")
