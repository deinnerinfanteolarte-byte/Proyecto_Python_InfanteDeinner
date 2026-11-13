from almacenamiento import cargar_datos
from usuarios import iniciar_sesion
from roles import menu_administrativo, menu_medico


def main():
    datos = cargar_datos()
    ejecutando = True

    while ejecutando:
        usuario_actual = None
        while usuario_actual is None:
            usuario_actual = iniciar_sesion(datos)

        if usuario_actual["rol"] == "administrativo":
            accion = menu_administrativo(datos, usuario_actual)
        elif usuario_actual["rol"] == "medico":
            accion = menu_medico(datos, usuario_actual)
        else:
            print("\n[Error] Rol de usuario no reconocido.")
            accion = "continuar"

        if accion == "salir":
            ejecutando = False


if __name__ == "__main__":
    main()