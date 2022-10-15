from itertools import count
import os
import pickle

x1 = count()  # for crear_rotulo_html()
next(x1)

x2 = count()  # for crear_rotulo_pickle()
next(x2)

x3 = count()  # for enumerate_figures()
next(x3)

x4 = count()  # for descargar_objeto()
next(x4)


def enumerar_figuras(func): # se usa en presentacion.ipynb?
    global x3
    try:
        if func() is None:
            print(f"Figura {next(x3)}")
    except:
        pass


def descargar_imagen(obj, dir_name="html", prefix="img", suffix=None):
    """Descarga una figure en formato HTML"""
    obj.write_html(
        crear_directorio(dir_name)
        + "\\"
        + crear_rotulo_html(prefix=prefix, suffix=suffix),
        full_html=True,
    )


def descargar_objeto(obj, dir_name="objects", prefix="obj", suffix=None):
    """Descarga un objeto en formato pickle (Serializado)
    
    #TODO
    mira el nombre de los ficheros del directorio
    mira el primer caracter del nombre de los ficheros del directorio
    mientras count() esté dentro de la lista, count()
    cuando count() no esté en la lista, agregarlo al nombre del fichero que se va a descargar   
    
    """
    global x4

    path = f"{os.getcwd()}\\{dir_name}"
    list_dir = os.listdir(path)
    print (list_dir)

    for nombre in list_dir:
        if nombre[0].isdigit():
            last_val = int(nombre[0])

    print (last_val)

    x = next(x4)
    while last_val >= x:
        x = next(x4)
    
    print (x)


    file_name = f"{crear_directorio(dir_name)}\\{crear_rotulo_pickle(prefix=prefix, suffix=suffix, x=x)}"

    print (file_name)
    # with open(file_name, "wb") as f:
    #     pickle.dump(obj, f)


def cargar_objeto(file_name, dir_name="objects"):
    """Levanta desde el directorio, un objeto pickle guardado"""
    file_name = f"{crear_directorio(dir_name)}\\{file_name}"
    with open(file_name, "rb") as f:
        obj = pickle.load(f)
    return obj


def crear_directorio(dir_name):
    if not dir_name.startswith("\\"):
        dir_name = "\\" + dir_name
    path = os.getcwd() + dir_name
    os.makedirs(path, exist_ok=True)
    return path


def string_replace_blank(string):
    return string.replace(" ", "_")


def crear_rotulo_html(prefix, suffix):
    global x1
    if suffix is not None:
        return f"{next(x1)}_{prefix}_{string_replace_blank(suffix)}.html"
    return f"{next(x1)}_{prefix}.html"


def crear_rotulo_pickle(prefix, suffix, x=1):
    if suffix is not None:
        return f"{x}_{prefix}_{string_replace_blank(suffix)}.pickle"
    return f"{x}_{prefix}.pickle"


if __name__ == "__main__":
    
    my_var = "hola_mundo"

    descargar_objeto(my_var)
    
    pass

