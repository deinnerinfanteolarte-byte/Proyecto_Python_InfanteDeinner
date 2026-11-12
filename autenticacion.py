"""ACME Clinic · Sistema de diagnósticos. Archivo principal de ejecución."""
import almacenamiento
import autenticacion
import diagnosticos
import historia_clinica
import pacientes
import usuarios


def menu_principal(datos, usuario):
    """Muestra el menú hasta que el usuario cierre sesión."""
    acciones = {
        "1": lambda: usuarios.registrar_usuario(datos),
        "2": lambda: pacientes.registrar_paciente(datos),
        "3": lambda: diagnosticos.diagnosticar(datos, usuario),
        "4": lambda: historia_clinica.mostrar_historia_clinica(datos),
    }
    while True:
        print(f"\n=== ACME CLINIC · {usuario['nombres']} ({usuario['rol']}) ===")
        print("1. Registrar usuario")
        print("2. Registrar paciente")
        print("3. Diagnosticar paciente")
        print("4. Historia clínica")
        print("5. Cerrar sesión")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "5":
            print("Sesión cerrada.")
            return
        accion = acciones.get(opcion)
        if accion:
            accion()
        else:
            print("  ⚠ Opción no válida.")


def main():
    datos = almacenamiento.cargar_datos()
    try:
        while True:
            usuario = autenticacion.login(datos)
            if usuario is None:
                print("Demasiados intentos fallidos. Cerrando el programa.")
                return
            menu_principal(datos, usuario)
            if input("¿Desea iniciar sesión con otro usuario? (s/n): ").strip().lower() not in ("s", "si", "sí"):
                print("Hasta luego.")
                return
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma finalizado.")


if __name__ == "__main__":
    main()

    #########################################################################


    """Login de usuarios."""
import utilidades

MAX_INTENTOS = 3


def buscar_usuario_por_email(datos, email):
    for usuario in datos["usuarios"]:
        if usuario["email"].lower() == email.lower():
            return usuario
    return None


def login(datos):
    """Solicita credenciales. Devuelve el usuario autenticado o None tras 3 intentos fallidos."""
    print("\n=== ACME CLINIC · Inicio de sesión ===")
    for intento in range(1, MAX_INTENTOS + 1):
        email = input("Usuario (e-mail): ").strip()
        password = utilidades.pedir_password("Contraseña: ")
        usuario = buscar_usuario_por_email(datos, email)
        if usuario and utilidades.verificar_password(password, usuario["password"]):
            print(f"\n✔ Bienvenido(a), {usuario['nombres']} {usuario['apellidos']}.")
            return usuario
        print(f"  ✖ Usuario o contraseña incorrectos ({intento}/{MAX_INTENTOS}).")
    return None

###############################################################################
"""Registro de usuarios del sistema (médicos y administrativos)."""
import almacenamiento
import autenticacion
import utilidades

ROLES = ["Médico", "Administrativo"]
MIN_PASSWORD = 6


def registrar_usuario(datos):
    print("\n--- Registro de usuario ---")
    identificacion = utilidades.pedir_identificacion()
    if any(u["identificacion"] == identificacion for u in datos["usuarios"]):
        print("  ✖ Ya existe un usuario con ese número de identificación.")
        return

    nombres = utilidades.pedir_texto("Nombres: ")
    apellidos = utilidades.pedir_texto("Apellidos: ")
    telefono = utilidades.pedir_telefono()
    email = utilidades.pedir_email("E-mail corporativo (será su usuario): ")
    if autenticacion.buscar_usuario_por_email(datos, email):
        print("  ✖ Ya existe un usuario con ese e-mail.")
        return
    direccion = utilidades.pedir_texto("Dirección: ")
    rol = utilidades.pedir_opcion("Rol del usuario:", ROLES)

    while True:
        password = utilidades.pedir_password(f"Contraseña (mín. {MIN_PASSWORD} caracteres): ")
        if len(password) < MIN_PASSWORD:
            print(f"  ⚠ La contraseña debe tener al menos {MIN_PASSWORD} caracteres.")
            continue
        if password != utilidades.pedir_password("Confirme la contraseña: "):
            print("  ⚠ Las contraseñas no coinciden.")
            continue
        break

    datos["usuarios"].append(
        {
            "identificacion": identificacion,
            "nombres": nombres,
            "apellidos": apellidos,
            "telefono": telefono,
            "email": email,
            "direccion": direccion,
            "rol": rol,
            "password": utilidades.hash_password(password),
        }
    )
    almacenamiento.guardar_datos(datos)
    print(f"  ✔ Usuario {nombres} {apellidos} registrado como {rol}.")

    ####################################################################
    """Proceso de diagnóstico: síntomas, diagnóstico y prescripción médica."""
import almacenamiento
import pacientes
import utilidades


def _pedir_sintomas():
    print("\nSíntomas (uno por línea; deje vacío para terminar):")
    sintomas = []
    while True:
        sintoma = input(f"  Síntoma {len(sintomas) + 1}: ").strip()
        if not sintoma:
            if sintomas:
                return sintomas
            print("  ⚠ Registre al menos un síntoma.")
            continue
        sintomas.append(sintoma)


def _pedir_medicamentos():
    print("\nPrescripción médica")
    medicamentos = []
    while utilidades.pedir_si_no("¿Agregar un medicamento?"):
        medicamentos.append(
            {
                "medicamento": utilidades.pedir_texto("  Medicamento: "),
                "cantidad": utilidades.pedir_entero("  Cantidad (unidades a entregar): "),
                "dosis": utilidades.pedir_texto(
                    "  Dosis diaria (ej. 1 tableta cada 8 horas): "
                ),
                "tiempo_aplicacion_dias": utilidades.pedir_entero(
                    "  Tiempo de aplicación (días): "
                ),
            }
        )
    return medicamentos


def diagnosticar(datos, medico):
    if medico["rol"] != "Médico":
        print("  ✖ Solo los usuarios con rol Médico pueden diagnosticar pacientes.")
        return

    print("\n--- Diagnosticar paciente ---")
    identificacion = utilidades.pedir_identificacion("Identificación del paciente: ")
    paciente = pacientes.buscar_paciente(datos, identificacion)
    if not paciente:
        print("  ✖ El paciente no está registrado. Regístrelo primero.")
        return
    print(f"Paciente: {paciente['nombres']} {paciente['apellidos']}")

    sintomas = _pedir_sintomas()
    diagnostico = utilidades.pedir_texto("\nDiagnóstico (patología o enfermedad): ")
    medicamentos = _pedir_medicamentos()

    fecha = utilidades.ahora()
    consulta = {
        "id": len(datos["consultas"]) + 1,
        "fecha": fecha,
        "paciente_id": paciente["identificacion"],
        "medico_id": medico["identificacion"],
        "sintomas": sintomas,
        "diagnostico": diagnostico,
        "medicamentos": medicamentos,
    }
    datos["consultas"].append(consulta)
    almacenamiento.guardar_datos(datos)

    prescripcion = {
        "fecha": fecha,
        "paciente": {
            "identificacion": paciente["identificacion"],
            "nombres": paciente["nombres"],
            "apellidos": paciente["apellidos"],
        },
        "medico": {
            "identificacion": medico["identificacion"],
            "nombres": medico["nombres"],
            "apellidos": medico["apellidos"],
        },
        "sintomas": sintomas,
        "diagnostico": diagnostico,
        "medicamentos": medicamentos,
    }
    ruta = almacenamiento.guardar_prescripcion(prescripcion)
    print("\n  ✔ Diagnóstico registrado.")
    print(f"  ✔ Prescripción médica generada: {ruta}")
    #################################################################
    """Consulta de la historia clínica de un paciente."""
import pacientes
import utilidades


def _nombre_medico(datos, medico_id):
    for usuario in datos["usuarios"]:
        if usuario["identificacion"] == medico_id:
            return f"{usuario['nombres']} {usuario['apellidos']}"
    return f"Médico {medico_id} (no encontrado)"


def mostrar_historia_clinica(datos):
    print("\n--- Historia clínica ---")
    identificacion = utilidades.pedir_identificacion("Identificación del paciente: ")
    paciente = pacientes.buscar_paciente(datos, identificacion)
    if not paciente:
        print("  ✖ El paciente no está registrado.")
        return

    print("\n" + "=" * 60)
    print("HISTORIA CLÍNICA")
    print("=" * 60)
    print(f"Identificación : {paciente['identificacion']}")
    print(f"Nombre         : {paciente['nombres']} {paciente['apellidos']}")
    print(f"Teléfono       : {paciente['telefono']}")
    print(f"E-mail         : {paciente['email']}")
    print(f"Dirección      : {paciente['direccion']}")
    print(f"Género         : {paciente['genero']}")
    print(f"Estado civil   : {paciente['estado_civil']}")

    consultas = sorted(
        (c for c in datos["consultas"] if c["paciente_id"] == identificacion),
        key=lambda c: c["fecha"],
    )
    if not consultas:
        print("\nEl paciente no tiene consultas registradas.")
        return

    for numero, consulta in enumerate(consultas, start=1):
        print("\n" + "-" * 60)
        print(f"Consulta {numero} · {consulta['fecha']}")
        print(f"Médico      : {_nombre_medico(datos, consulta['medico_id'])}")
        print("Síntomas    : " + "; ".join(consulta["sintomas"]))
        print(f"Diagnóstico : {consulta['diagnostico']}")
        if consulta["medicamentos"]:
            print("Medicamentos prescritos:")
            for m in consulta["medicamentos"]:
                print(
                    f"  - {m['medicamento']} | cantidad: {m['cantidad']} | "
                    f"dosis: {m['dosis']} | duración: {m['tiempo_aplicacion_dias']} día(s)"
                )
        else:
            print("Medicamentos prescritos: ninguno")
    print("=" * 60)
    ####################################################################
    """Persistencia de datos en archivos JSON."""
import json
import os

import utilidades

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_DATOS = os.path.join(BASE_DIR, "datos.json")
CARPETA_PRESCRIPCIONES = os.path.join(BASE_DIR, "prescripciones")

# Contraseña inicial del administrador (cámbiela o créela distinta en producción).
PASSWORD_ADMIN_INICIAL = "Admin123"


def _datos_iniciales():
    return {
        "usuarios": [
            {
                "identificacion": "0000",
                "nombres": "Admin",
                "apellidos": "Administrador",
                "telefono": "555 000111",
                "email": "admin@acmeclinic.com",
                "direccion": "Cl 185 # 26 – 85",
                "rol": "Administrativo",
                "password": utilidades.hash_password(PASSWORD_ADMIN_INICIAL),
            }
        ],
        "pacientes": [],
        "consultas": [],
    }


def guardar_datos(datos):
    with open(RUTA_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)


def cargar_datos():
    """Carga datos.json; si no existe, lo crea con el usuario administrador."""
    if not os.path.exists(RUTA_DATOS):
        datos = _datos_iniciales()
        guardar_datos(datos)
        return datos
    try:
        with open(RUTA_DATOS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except json.JSONDecodeError:
        print("⚠ datos.json está dañado. Corrija o elimine el archivo e intente de nuevo.")
        raise SystemExit(1)
    for clave in ("usuarios", "pacientes", "consultas"):
        datos.setdefault(clave, [])
    return datos


def guardar_prescripcion(prescripcion):
    """Guarda la prescripción médica como JSON y devuelve la ruta del archivo."""
    os.makedirs(CARPETA_PRESCRIPCIONES, exist_ok=True)
    marca = prescripcion["fecha"].replace("-", "").replace(":", "").replace(" ", "_")
    nombre = f"prescripcion_{prescripcion['paciente']['identificacion']}_{marca}.json"
    ruta = os.path.join(CARPETA_PRESCRIPCIONES, nombre)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(prescripcion, archivo, ensure_ascii=False, indent=4)
    return ruta
########################################################3
"""Funciones de apoyo: validación de entradas, contraseñas y fechas."""
import hashlib
import hmac
import os
import re
from datetime import datetime
from getpass import getpass

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")
TELEFONO_RE = re.compile(r"^[\d\s+\-()]{7,20}$")


# ---------- Contraseñas ----------
def hash_password(password, salt=None):
    """Devuelve 'salt$hash' usando PBKDF2-HMAC-SHA256."""
    salt = salt or os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt), 100_000
    ).hex()
    return f"{salt}${digest}"


def verificar_password(password, almacenado):
    try:
        salt, _ = almacenado.split("$")
    except ValueError:
        return False
    return hmac.compare_digest(hash_password(password, salt), almacenado)


def pedir_password(mensaje="Contraseña: "):
    try:
        return getpass(mensaje)
    except (EOFError, KeyboardInterrupt):
        raise
    except Exception:
        return input(mensaje)


# ---------- Fechas ----------
def ahora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------- Entradas validadas ----------
def pedir_texto(mensaje, obligatorio=True):
    while True:
        valor = input(mensaje).strip()
        if valor or not obligatorio:
            return valor
        print("  ⚠ Este campo es obligatorio.")


def pedir_identificacion(mensaje="Número de identificación: "):
    while True:
        valor = input(mensaje).strip()
        if valor.isalnum():
            return valor
        print("  ⚠ Ingrese solo letras y números, sin espacios.")


def pedir_telefono(mensaje="Teléfono: "):
    while True:
        valor = input(mensaje).strip()
        if TELEFONO_RE.match(valor):
            return valor
        print("  ⚠ Teléfono no válido (use dígitos, espacios, + o -).")


def pedir_email(mensaje="E-mail: "):
    while True:
        valor = input(mensaje).strip().lower()
        if EMAIL_RE.match(valor):
            return valor
        print("  ⚠ E-mail no válido.")


def pedir_entero(mensaje, minimo=1):
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit() and int(valor) >= minimo:
            return int(valor)
        print(f"  ⚠ Ingrese un número entero mayor o igual a {minimo}.")


def pedir_opcion(mensaje, opciones):
    """Muestra una lista numerada y devuelve la opción elegida."""
    print(mensaje)
    for i, opcion in enumerate(opciones, start=1):
        print(f"  {i}. {opcion}")
    while True:
        valor = input("Seleccione una opción: ").strip()
        if valor.isdigit() and 1 <= int(valor) <= len(opciones):
            return opciones[int(valor) - 1]
        print("  ⚠ Opción no válida.")


def pedir_si_no(mensaje):
    while True:
        valor = input(f"{mensaje} (s/n): ").strip().lower()
        if valor in ("s", "si", "sí"):
            return True
        if valor in ("n", "no"):
            return False
        print("  ⚠ Responda 's' o 'n'.")
        #######################################################
        {
    "usuarios": [
        {
            "identificacion": "0000",
            "nombres": "Admin",
            "apellidos": "Administrador",
            "telefono": "555 000111",
            "email": "admin@acmeclinic.com",
            "direccion": "Cl 185 # 26 – 85",
            "rol": "Administrativo",
            "password": "626621bc0e7891747cc79b3e9fdf3a15$5d98ee9286dc9709906d4c933c8f6f6c93dcff010050b29da29ea2eb44e6c748"
        }
    ],
    "pacientes": [],
    "consultas": []
}