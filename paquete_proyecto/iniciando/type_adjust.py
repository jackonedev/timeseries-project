def type_adjust(data):
    """type_adjust()
    
    Keyword arguments:
    data: pandas.DataFrame -- Selecciona cada una de las columnas, y las evalua para elegir el mejor datatype:

        1ro: str -> float
            función 1: prueba cambio directo float(x)
            funcion 2: intenta eliminando el "." y cambiando la "," por "." 
        2do: float -> int
            función 3: si para cada fila x // int(x) == 0 entonces int(x)
                        además debe evaluar que porcentaje de no cumple dicha condicion y si es menor al 1% cambiarlo igual
        3: str -> datetime
            función 4: para las columnas object restantes pd.to_datetime()

    Return: pandas.DataFrame -- Con las columnas modificadas
    """
    