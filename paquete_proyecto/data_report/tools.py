from itertools import count
import os
import pickle

x1 = count()  # for crear_rotulo_html()
next(x1)

x2 = count()  # for crear_rotulo_pickle()
next(x2)

x3 = count()  # for enumerate_figures()
next(x3)


def enumerar_figuras(func):
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
    """Descarga un objeto en formato pickle (Serializado)"""
    file_name = f"{crear_directorio(dir_name)}\\{crear_rotulo_pickle(prefix=prefix, suffix=suffix)}"
    with open(file_name, "wb") as f:
        pickle.dump(obj, f)


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
        return f"{prefix}_{next(x1)}_{string_replace_blank(suffix)}.html"
    return f"{prefix}_{next(x1)}.html"


def crear_rotulo_pickle(prefix, suffix):
    global x2
    if suffix is not None:
        return f"{prefix}_{next(x1)}_{string_replace_blank(suffix)}.pickle"
    return f"{prefix}_{next(x1)}.pickle"


