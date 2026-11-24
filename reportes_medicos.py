import json


def cargar_datos_clinica():
    # Lee datos.json sin modificarlo
    usuarios = []
    diagnosticos = []

    with open("datos.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
        if "usuarios" in datos:
            usuarios = datos["usuarios"]
        if "diagnosticos" in datos:
            diagnosticos = datos["diagnosticos"]
        elif "consultas" in datos:
            diagnosticos = datos["consultas"]

    return usuarios, diagnosticos


def ordenar_medicos_descendente(lista_medicos):
    # Ordena de mayor a menor segun total_diagnosticos (metodo burbuja)
    n = len(lista_medicos)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista_medicos[j]["total_diagnosticos"] < lista_medicos[j + 1]["total_diagnosticos"]:
                temporal = lista_medicos[j]
                lista_medicos[j] = lista_medicos[j + 1]
                lista_medicos[j + 1] = temporal
    return lista_medicos


def reporte_carga_medicos():
    usuarios, diagnosticos = cargar_datos_clinica()
    lista_medicos = []

    for usuario in usuarios:
        rol_usuario = str(usuario.get("rol", "")).lower()
        if rol_usuario == "medico" or rol_usuario == "médico":
            id_med = usuario.get("id", usuario.get("identificacion", ""))
            nombre_med = usuario.get("nombre_completo", usuario.get("nombre", "Sin nombre"))

            total_diag = 0
            pacientes_unicos = []
            suma_sintomas = 0
            suma_medicamentos = 0

            for diag in diagnosticos:
                medico_diag = diag.get("id_medico", diag.get("medico_id", ""))
                if str(medico_diag) == str(id_med):
                    total_diag = total_diag + 1

                    # Contar pacientes distintos
                    id_pac = diag.get("id_paciente", diag.get("paciente_id", ""))
                    if id_pac != "" and id_pac not in pacientes_unicos:
                        pacientes_unicos.append(id_pac)

                    # Contar sintomas
                    sintomas = diag.get("sintomas", [])
                    if type(sintomas) == list:
                        suma_sintomas = suma_sintomas + len(sintomas)
                    elif type(sintomas) == str and sintomas.strip() != "":
                        suma_sintomas = suma_sintomas + len(sintomas.split(","))

                    # Contar medicamentos
                    medicamentos = diag.get("medicamentos", diag.get("prescripcion", []))
                    if type(medicamentos) == list:
                        suma_medicamentos = suma_medicamentos + len(medicamentos)
                    elif type(medicamentos) == str and medicamentos.strip() != "":
                        suma_medicamentos = suma_medicamentos + len(medicamentos.split(","))

            if total_diag > 0:
                prom_sintomas = round(suma_sintomas / total_diag, 2)
                prom_medicamentos = round(suma_medicamentos / total_diag, 2)
            else:
                prom_sintomas = 0.0
                prom_medicamentos = 0.0

            info_medico = {
                "id_medico": id_med,
                "nombre_completo": nombre_med,
                "total_diagnosticos": total_diag,
                "pacientes_distintos": len(pacientes_unicos),
                "promedio_sintomas_por_consulta": prom_sintomas,
                "promedio_medicamentos_por_consulta": prom_medicamentos
            }
            lista_medicos.append(info_medico)

    lista_medicos = ordenar_medicos_descendente(lista_medicos)

    if len(lista_medicos) > 0:
        mayor_diag = lista_medicos[0]
        menor_carga = lista_medicos[len(lista_medicos) - 1]
        mayor_pacientes = lista_medicos[0]

        for med in lista_medicos:
            if med["pacientes_distintos"] > mayor_pacientes["pacientes_distintos"]:
                mayor_pacientes = med

        resumen = {
            "medico_mayor_diagnosticos": {
                "id_medico": mayor_diag["id_medico"],
                "nombre_completo": mayor_diag["nombre_completo"],
                "total_diagnosticos": mayor_diag["total_diagnosticos"]
            },
            "medico_mayor_pacientes_distintos": {
                "id_medico": mayor_pacientes["id_medico"],
                "nombre_completo": mayor_pacientes["nombre_completo"],
                "pacientes_distintos": mayor_pacientes["pacientes_distintos"]
            },
            "medico_menor_carga": {
                "id_medico": menor_carga["id_medico"],
                "nombre_completo": menor_carga["nombre_completo"],
                "total_diagnosticos": menor_carga["total_diagnosticos"]
            }
        }
    else:
        resumen = {
            "medico_mayor_diagnosticos": None,
            "medico_mayor_pacientes_distintos": None,
            "medico_menor_carga": None
        }

    reporte_final = {
        "medicos": lista_medicos,
        "resumen": resumen
    }

    with open("reporte_carga_medicos.json", "w", encoding="utf-8") as archivo_salida:
        json.dump(reporte_final, archivo_salida, indent=4, ensure_ascii=False)

    print("\n[OK] Reporte generado en 'reporte_carga_medicos.json'.")


def reporte_carga_médicos():
    # Alias con tilde para cumplir exactamente con el nombre del requisito
    reporte_carga_medicos()
