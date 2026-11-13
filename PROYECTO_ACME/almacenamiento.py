import json
import os

ARCHIVO_DATOS = "datos.json"


def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        archivo = open(ARCHIVO_DATOS, "r", encoding="utf-8")
        datos = json.load(archivo)
        archivo.close()
        return datos
    else:
        datos_iniciales = {
            "usuarios": [
                {
                    "identificacion": "0000",
                    "nombres": "Admin",
                    "apellidos": "Administrador",
                    "telefono": "555 000111",
                    "email": "admin@acmeclinic.com",
                    "direccion": "Cl 185 # 26 - 85",
                    "rol": "administrativo",
                    "password": "admin123"
                }
            ],
            "pacientes": [],
            "consultas": []
        }
        guardar_datos(datos_iniciales)
        return datos_iniciales


def guardar_datos(datos):
    archivo = open(ARCHIVO_DATOS, "w", encoding="utf-8")
    json.dump(datos, archivo, indent=4, ensure_ascii=False)
    archivo.close()


def guardar_prescripcion_json(nombre_archivo, prescripcion_data):
    archivo = open(nombre_archivo, "w", encoding="utf-8")
    json.dump(prescripcion_data, archivo, indent=4, ensure_ascii=False)
    archivo.close()