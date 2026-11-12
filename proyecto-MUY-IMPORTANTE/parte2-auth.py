import json

def cargar_datos():
    try:
        with open("datos.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"usuarios": [], "pacientes": [], "diagnosticos": []}

def login():
    datos = cargar_datos()
    print("=== INICIO DE SESIÓN ACME ===")
    email = input("E-mail corporativo: ").strip()
    password = input("Contraseña: ").strip()

    for usuario in datos["usuarios"]:
        if usuario["email"] == email and usuario["password"] == password:
            print(f"\nBienvenido(a), {usuario['nombres']} {usuario['apellidos']}!")
            return usuario
            
    print("\nCredenciales incorrectas. Intente nuevamente.")
    return None