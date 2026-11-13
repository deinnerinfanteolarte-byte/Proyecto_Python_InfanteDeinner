from registro import registrar_usuario, registrar_paciente
from consultas import diagnosticar_paciente, ver_historia_clinica


def menu_administrativo(datos, usuario_actual):
    activo = True
    while activo:
        print("\n========================================")
        print("   CLÍNICA ACME - MENÚ ADMINISTRATIVO   ")
        print(f" Operario: {usuario_actual['nombres']} {usuario_actual['apellidos']}")
        print("========================================")
        print("1. Registrar usuario (Médico / Administrativo)")
        print("2. Registrar paciente")
        print("3. Consultar historia clínica")
        print("4. Cerrar sesión")
        print("5. Salir del sistema")

        opcion = input("\nSeleccione una opción (1-5): ").strip()

        if opcion == "1":
            registrar_usuario(datos)
        elif opcion == "2":
            registrar_paciente(datos)
        elif opcion == "3":
            ver_historia_clinica(datos)
        elif opcion == "4":
            print("\nCerrando sesión...")
            activo = False
        elif opcion == "5":
            print("\nSaliendo del sistema. ¡Hasta pronto!")
            return "salir"
        else:
            print("\n[Error] Opción no válida. Ingrese un número del 1 al 5.")

    return "continuar"


def menu_medico(datos, usuario_actual):
    activo = True
    while activo:
        print("\n========================================")
        print("       CLÍNICA ACME - MENÚ MÉDICO       ")
        print(f" Dr(a).: {usuario_actual['nombres']} {usuario_actual['apellidos']}")
        print("========================================")
        print("1. Diagnosticar paciente y generar prescripción")
        print("2. Consultar historia clínica")
        print("3. Cerrar sesión")
        print("4. Salir del sistema")

        opcion = input("\nSeleccione una opción (1-4): ").strip()

        if opcion == "1":
            diagnosticar_paciente(datos, usuario_actual)
        elif opcion == "2":
            ver_historia_clinica(datos)
        elif opcion == "3":
            print("\nCerrando sesión...")
            activo = False
        elif opcion == "4":
            print("\nSaliendo del sistema. ¡Hasta pronto!")
            return "salir"
        else:
            print("\n[Error] Opción no válida. Ingrese un número del 1 al 4.")

    return "continuar"