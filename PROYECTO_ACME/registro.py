from almacenamiento import guardar_datos
from pacientes import buscar_paciente


def registrar_usuario(datos):
    print("\n--- REGISTRO DE USUARIO (OPERARIO) ---")
    identificacion = input("Número de identificación: ").strip()
    if identificacion == "":
        print("[Error] La identificación no puede estar vacía.")
        return

    for usuario in datos["usuarios"]:
        if usuario["identificacion"] == identificacion:
            print("[Error] Ya existe un usuario con esa identificación.")
            return

    nombres = input("Nombres: ").strip()
    apellidos = input("Apellidos: ").strip()
    telefono = input("Número de teléfono: ").strip()
    email = input("E-mail corporativo: ").strip().lower()

    if "@" not in email or "." not in email:
        print("[Error] El formato del correo no es válido.")
        return

    for usuario in datos["usuarios"]:
        if usuario["email"].lower() == email:
            print("[Error] Ese correo ya está registrado.")
            return

    direccion = input("Dirección: ").strip()

    rol = ""
    while rol != "medico" and rol != "administrativo":
        print("Seleccione el rol:")
        print("1. Médico")
        print("2. Administrativo")
        opcion_rol = input("Opción (1 o 2): ").strip()
        if opcion_rol == "1":
            rol = "medico"
        elif opcion_rol == "2":
            rol = "administrativo"
        else:
            print("[Error] Opción inválida. Intente de nuevo.")

    password = input("Asigne una contraseña: ").strip()
    if password == "":
        print("[Error] La contraseña no puede estar vacía.")
        return

    nuevo_usuario = {
        "identificacion": identificacion,
        "nombres": nombres,
        "apellidos": apellidos,
        "telefono": telefono,
        "email": email,
        "direccion": direccion,
        "rol": rol,
        "password": password
    }

    datos["usuarios"].append(nuevo_usuario)
    guardar_datos(datos)
    print(f"\n[Éxito] Usuario {nombres} {apellidos} registrado correctamente.")


def registrar_paciente(datos):
    print("\n--- REGISTRO DE PACIENTE ---")
    identificacion = input("Número de identificación: ").strip()
    if identificacion == "":
        print("[Error] La identificación no puede estar vacía.")
        return

    existente = buscar_paciente(datos, identificacion)
    if existente is not None:
        print("[Error] Ya existe un paciente registrado con esa identificación.")
        return

    nombres = input("Nombres: ").strip()
    apellidos = input("Apellidos: ").strip()
    telefono = input("Número de teléfono: ").strip()
    email = input("E-mail: ").strip()
    direccion = input("Dirección: ").strip()
    genero = input("Género (Masculino/Femenino/Otro): ").strip()
    estado_civil = input("Estado civil (Soltero/Casado/Unión Libre/Divorciado/Viudo): ").strip()

    nuevo_paciente = {
        "identificacion": identificacion,
        "nombres": nombres,
        "apellidos": apellidos,
        "telefono": telefono,
        "email": email,
        "direccion": direccion,
        "genero": genero,
        "estado_civil": estado_civil
    }

    datos["pacientes"].append(nuevo_paciente)
    guardar_datos(datos)
    print(f"\n[Éxito] Paciente {nombres} {apellidos} registrado correctamente.")