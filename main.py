# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press the green button in the gutter to run the script.

from objetoseguro import ObjetoSeguro

if __name__ == '__main__':
    print("Karen Josefina Rivera Torres")
    print("Pproyecto")
    Ob1 = ObjetoSeguro("Alicia")
    Ob2 = ObjetoSeguro("Bob")
    Ob1.saludar(Ob2.nombre, "Hola, que tal?")
    Ob2.saludar(Ob1.nombre, "Hola, bien y tu?")
    Ob2.almacenar_msj("Hola, bien y tu?")
    Ob1.almacenar_msj("Hola, que tal?")
    Ob1.esperar_respuesta("hello")



# See PyCharm help at https://www.jetbrains.com/help/pycharm/