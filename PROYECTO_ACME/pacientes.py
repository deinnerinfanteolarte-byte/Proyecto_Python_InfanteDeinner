def buscar_paciente(datos, identificacion):
    for paciente in datos["pacientes"]:
        if paciente["identificacion"] == identificacion:
            return paciente
    return None