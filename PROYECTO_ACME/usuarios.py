def iniciar_sesion(datos):
    print("\n========================================")
    print("       INICIO DE SESIÓN - CLÍNICA ACME  ")
    print("========================================")
    email = input("Usuario (e-mail corporativo): ").strip().lower()
    password = input("Contraseña: ").strip()

    for usuario in datos["usuarios"]:
        if usuario["email"].lower() == email and usuario["password"] == password:
            print(f"\nBienvenido(a), {usuario['nombres']} {usuario['apellidos']} ({usuario['rol']}).")
            return usuario

    print("\n[Error] Correo o contraseña incorrectos.")
    return None