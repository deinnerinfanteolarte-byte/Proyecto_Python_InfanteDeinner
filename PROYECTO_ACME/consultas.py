from datetime import datetime
from almacenamiento import guardar_datos, guardar_prescripcion_json
from pacientes import buscar_paciente


def diagnosticar_paciente(datos, usuario_actual):
    print("\n--- DIAGNÓSTICO DE PACIENTE ---")
    id_paciente = input("Ingrese el número de identificación del paciente: ").strip()
    paciente = buscar_paciente(datos, id_paciente)

    if paciente is None:
        print("[Error] El paciente no se encuentra registrado. Debe registrarlo un administrativo primero.")
        return

    print(f"\nPaciente encontrado: {paciente['nombres']} {paciente['apellidos']}")

    print("\nRegistro de síntomas (escriba 'fin' cuando termine de agregar síntomas):")
    sintomas = []
    continuar_sintomas = True
    while continuar_sintomas:
        sintoma = input("- Síntoma: ").strip()
        if sintoma.lower() == "fin":
            if len(sintomas) == 0:
                print("[Aviso] Debe registrar al menos un síntoma.")
            else:
                continuar_sintomas = False
        elif sintoma != "":
            sintomas.append(sintoma)

    diagnostico = ""
    while diagnostico == "":
        diagnostico = input("\nDescriba el diagnóstico (patología o enfermedad): ").strip()
        if diagnostico == "":
            print("[Error] El diagnóstico no puede estar vacío.")

    print("\n--- PRESCRIPCIÓN MÉDICA ---")
    medicamentos = []
    agregar_otro = "s"
    while agregar_otro.lower() == "s":
        nombre_med = input("Nombre del medicamento: ").strip()
        cantidad = input("Cantidad (ej. 1 caja, 20 tabletas): ").strip()
        dosis = input("Dosis diaria (ej. 1 tableta cada 8 horas): ").strip()
        tiempo = input("Tiempo de aplicación en días (ej. 7 días): ").strip()

        item_medicamento = {
            "medicamento": nombre_med,
            "cantidad": cantidad,
            "dosis": dosis,
            "tiempo_aplicacion": tiempo
        }
        medicamentos.append(item_medicamento)

        agregar_otro = input("¿Desea agregar otro medicamento? (s/n): ").strip()

    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fecha_archivo = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_medico = f"{usuario_actual['nombres']} {usuario_actual['apellidos']}"

    consulta = {
        "fecha": fecha_actual,
        "paciente_id": paciente["identificacion"],
        "paciente_nombre": f"{paciente['nombres']} {paciente['apellidos']}",
        "medico_id": usuario_actual["identificacion"],
        "medico_nombre": nombre_medico,
        "sintomas": sintomas,
        "diagnostico": diagnostico,
        "prescripcion": medicamentos
    }

    datos["consultas"].append(consulta)
    guardar_datos(datos)

    nombre_json_prescripcion = f"prescripcion_{paciente['identificacion']}_{fecha_archivo}.json"
    guardar_prescripcion_json(nombre_json_prescripcion, consulta)

    print("\n[Éxito] Diagnóstico guardado correctamente.")
    print(f"[Archivo generado] Prescripción exportada en: {nombre_json_prescripcion}")


def ver_historia_clinica(datos):
    print("\n--- HISTORIA CLÍNICA DEL PACIENTE ---")
    id_paciente = input("Ingrese el número de identificación del paciente: ").strip()
    paciente = buscar_paciente(datos, id_paciente)

    if paciente is None:
        print("[Error] No existe ningún paciente con ese número de identificación.")
        return

    print("\n============================================================")
    print("                  HISTORIA CLÍNICA - ACME                   ")
    print("============================================================")
    print(f"Identificación : {paciente['identificacion']}")
    print(f"Nombres        : {paciente['nombres']} {paciente['apellidos']}")
    print(f"Teléfono       : {paciente['telefono']}")
    print(f"E-mail         : {paciente['email']}")
    print(f"Dirección      : {paciente['direccion']}")
    print(f"Género         : {paciente['genero']}")
    print(f"Estado Civil   : {paciente['estado_civil']}")
    print("============================================================")

    encontradas = 0
    for consulta in datos["consultas"]:
        if consulta["paciente_id"] == id_paciente:
            encontradas = encontradas + 1
            print(f"\n--- CONSULTA #{encontradas} ---")
            print(f"Fecha       : {consulta['fecha']}")
            print(f"Médico      : {consulta['medico_nombre']}")
            print("Síntomas    :")
            for s in consulta["sintomas"]:
                print(f"   * {s}")
            print(f"Diagnóstico : {consulta['diagnostico']}")
            print("Medicamentos prescritos:")
            for med in consulta["prescripcion"]:
                print(
                    f"   - {med['medicamento']} | Cantidad: {med['cantidad']} | "
                    f"Dosis: {med['dosis']} | Tiempo: {med['tiempo_aplicacion']}"
                )
            print("------------------------------------------------------------")

    if encontradas == 0:
        print("\nEste paciente aún no tiene consultas ni diagnósticos registrados.")