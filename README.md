<i>Este es un resumen de presentacion.ipynb</i>

# <u>PROYECTO</u>: SERVICIO AUTOMOTRIZ **"AUTO MOTORS"**

![logo](https://user-images.githubusercontent.com/113382260/193469015-485cc23c-faef-4897-8617-2a5ee17470d7.png)

## Time Series Project - Data Science - Machine Learning

### <i>Agustin F. Stigliano - Python Developer y Data Scientist</i>

#### Año 2022

### TEMAS

- 1) CONSIGNA
- 2) DESARROLLO
- 3) CONCLUSIÓN

<br /><br /><br />

# 1. Consigna
<br />



## 1.1 <u>Descripción del proyecto</u>
Contamos con datos internos de la empresa como "Ventas" y "Empleados".<br />
Requieren analizar el impacto de la pandemia para evaluar si vender la empresa, si quiebra o si salir a buscar inversores para expansión del negocio hacia otros países.

<br />

## 1.2 <u>Objetivo</u>
El cliente necesita contar con toda la información ya analizada para tomar una decisión final.

<br /><br />

# 2. Desarrollo

El desarrollo del siguiente proyecto está dividido de la siguiente forma:

- 2.1 Descripción de la empresa
- 2.2 Etapas en el desarrollo del código
    - 2.2.1 DATA FEED: Descripción del acondicionamiento del dataset original
    - 2.2.2 DATA PREPARE: Descripción del tratamiento del dataset de trabajo
    - 2.2.3 DATA RESEARCH: Indicadores básicos
    - 2.2.4 DATA REPORT: Visualización

<br />

## 2.1 <u>Descripción de la empresa</u>
Empresa Colombiana automotríz con franquicias ofrece:<br /><br />
<div>
    <h5><b>1) SERVICIOS (servicio)</b></h5>
    <h5><b>2) REENCAUCHE (servicio)</b></h5>
    <h5><b>3) FILTROS (productos)</b></h5>
    <h5><b>4) LLANTAS (productos)</b></h5>
    <h5><b>5) LUBRICANTES (productos)</b></h5>
</div>

...    
**y mucho más!!**

<br />

## 2.2 <u>Etapas en el desarrollo de código</u>
<br />

### 2.2.1 <b><u>DATA FEED</u></b>: Descripción del acondicionamiento del dataset original


**1ro)** <br />
Se aplica la función **"importar_databases()"** (dentro del **"paquete_proyecto"** hay un módulo llamado **"iniciando"**, ahí dentro está el fichero **"bases.py"**), que carga los datos del ".csv", y pasan por una serie de tratamientos, primero manual, y posterior otro automátizado para estandarizar los tipos de variable de cada columna.

**2do)** <br />
Luego de una inspección con el módulo **"herramientas"**, fichero **"data_info.py"** se comprueba el estado de los datos, y finalmente se realizan ajustes finales desde **"iniciando"**, **"bases.py"**, **"ajustar_tipos()"**.

<br/><br/>


### 2.2.2 <b><u>DATA PREPARE</u></b>: Descripción del tratamiento del dataset de trabajo

**1ro)**<br />
AGREGAR COLUMNA "Ventas_USD" QUE SEA  "Ventas" A LA COTIZACION DEL "USD" DE LA FECHA

Queremos expresar las **ventas** en **dólares**, para eso se diseña una función que consulte la cotización histórica del **peso colombiano** respecto del dolar a través de un **API** ligada al servicio de **Alpha Vantage**. Una véz obtenido el **histórico semanal** desde el año 2014 hasta 2022, se procede a seleccionar el rango que contempla el dataset de trabajo, que corresponde al período de **2016 al 2020**. Luego se añáde la columna **"Cotizacion_USD"** y se calcula la columnas **"Ventas_USD"**


**2do)**<br />
AGREGAR FILAS DE FECHAS FALTANTES Y GENERADOR DE MUESTRAS

Es evidente que aquellos días en los que no hubo transacciones comerciales son fechas faltantes en nuestro dataset, lo que ocurre es que por definición de series temporales un **"log"** o **"paso"** es un fragmento temporal que puede ser considerado un elemento discreto, único, y equidistante de su "log" precedente y posterior. Completar las fechas del dataset es fundamental si se quiere desarrollar algoritmos de **machine learning** que usen librerías para series temporales.

Además de lo recién mencionado, ocurre que algunos **indicadores acumulativos** serían poco representativos de los períodos de estancamiento comercial, ya que no reflejarían la cantidad de días consecutivos sin introducir nuevas transacciones al sistema. 

Y por último, es necesario que el dataset esté completo si se quiere desarrollar **forecasting** (pronósticos), debido a que el proceso de **cross validation** para optimizar los hiperparámetros de entrenamiento, requiere **folds** que cumplan con lo antes mencionado respecto a las series temporales.



----------

<br /><br /><br /><br />



          Estructura de ficheros:

            (I)  "paquete_proyecto.iniciando":

                  - "bases.py": 
                        Contiene la función "importar_databases()" y "ajustar_tipos()" que usamos para iniciar el proyecto.


                  - Este módulo no es genérico, se desarrolló para el proyecto en cuestión.



            (II)  "paquete_proyecto.herramientas": 

                  - "type_adjust.py": 
                        Contiene la función "type_adjust()" que estandariza el criterio de selección del tipo de variable para cada columna.

                  - "data_info.py": 
                        Contiene la función "data_info()" que facilita el análisis del dataset de trabajo.

                  - "extra.py": 
                        Son funciones que se utilizan sobre otros ficheros de los módulos, no sobre el proyecto en sí.

                  - Este módulo es genérico, puede ser utilizado en otros proyectos.


            (III)  "paquete_proyecto.preprocesamiento":

                    - "forex_api.py": 
                            Contiene "alpha_vantage_fx_api()" una función desarrollada de forma genérica para consultar el histórico diario, semanal o mensual de más de 180 divisas que cotizan en el mercado de FOREX.

                    - "cotizacion.py": 
                            Contiene dos funciones que funcionan juntas "criterio_valor_apertura(preparar_cotizacion())" que es un criterio para tratar los datos recibidos por la API, y contiene "agregar_cotizacion()" que añade la columna de cotización a un dataset de trabajo existente. 

                    - "muestreo.py": 
                            La función "complete_dates()" añade todas las fechas faltantes a un dataset con índice datetime. Y "timeseries_cv()" recibe parámetros que se introducen en "sklearn.model_selection.TimeSeriesSplit()" y devuelve una lista cuyos elementos son los datasets solicitados.
                    
                    - Este módulo es genérico, puede ser utilizado en otros proyectos.
