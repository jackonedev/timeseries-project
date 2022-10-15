import pandas as pd
from matplotlib.pyplot import plot
import plotly.express as px
import chart_studio.plotly as py
import chart_studio.tools as tls
from time import sleep
from dotenv import load_dotenv
import os
from abc import ABC
from itertools import count

from paquete_proyecto.data_report.tools import descargar_imagen


class VisualizerData:
    """VisualizerData:
    - Storage some default values for graphs attributes
    - Storage a list of DataFrames
    - Storage a list with strings, must have same length than the previous list
    - Build an iterator for dataframe list
    - Build an iterator for feature list
    """

    width = 765# 765: for dashboard # 900: for exploring
    height = 400
    template = "plotly_dark"
    pd.options.plotting.backend = "plotly"

    def __init__(
        self,
        frame_list: list[pd.DataFrame],
        features: list[str],
        y_label=None,
        title_suffix=None,
    ):
        self.dataset_iterator = iter(frame_list)
        self.feature_iterator = iter(features)
        self.dataframe_list = frame_list
        self.features = features
        self.y_axis_label = y_label
        self.title_suffix = title_suffix


class VisualProcessor(ABC, VisualizerData):
    """Visual Processor
    - Tiene su metodo constructivo separado
    - cumple con la funcion obj.set_content()
    - admite obj.set_content().set_title()
    - su objetifo final es obj.set_content().plot(), .plot_area, .plot_kind(kind=)
    - Contiene un iterador interno y contiene función de selección manual de las features
    - los parámetros de set_content() son:
        - feature= None - default: se ejecuta el iterador interno - 'str': si la label existe, se setea esa feature
        - y_label=None- default: configuración predefinida del graph - 'str': crea el label para el y axis, y el titulo
        - ascending = False- establece el orden de las columnas de cada DataFrame
        - title_suffix = None - default: no añade aclaración al titulo - 'str' añade información adicional al titulo
        - download = False - default: modo de solo viusualización - True: tras cada visualización consulta si se desea descargar la imágen en formato html
    - los parámetros de set_title() son:
        - new_title - str: Reemplaza al título que genera el método set_content() por default
    - El método plot() no tiene parámetros
    - El método plot_areas() no tiene parámetros
    - El método plot_kind() recibe los siguientes parámetros:
        - kind = 'bar' - default: grafica un gráfico de barras - 'str': "bar", "barh", "hist", "box", "line"
        - resample=None - default: grafica tal cual está el TimeIndex - 'str': "W", "M", "2M", ... admite los parámetros del pd.resample()

    Modo de uso:

    list_feature = ['A', 'B', 'C']
    list_frames = [pd.DataFrame, pd.DataFrame, pd.DataFrame]

    instance = VisualProcessor(lista_frames, list_feature)
    for i in range(len(list_feature)):
        instance.set_content().plot()

    # or Calling a particular feature

    instance.set_content(feature="B").plot()

    """

    current_content = None
    title = "{} , {}"

    def _get_content(self):
        return next(self.dataset_iterator, None)

    def set_title(self, new_title):
        self.title_format = new_title
        return self

    def set_content(
        self,
        feature=None,
        y_label=None,
        ascending=False,
        title_suffix=None,
    ):
        """set_content
        Es un método que devuelve un objeto listo para aplicarsele el método "plot()".
        Si feature es None ejecuta el iterador
        Si feature corresponde a alguna feature, si existe, devuelve el dataframe correspondiente procesado
        """
        # Collect Dataframe from list by label search
        if feature is not None and self.features.count(feature) > 0:
            for i, label in enumerate(self.features):
                if label == feature:
                    self.current_content = self.dataframe_list[i]
                    self.current_feature = feature
                    break
        # Or Collect DataFrame from list by iterator
        else:
            if feature is not None:
                print("logg. No se encontró la feature solicitada")
            self.current_content = self._get_content()
            self.current_feature = next(self.feature_iterator, None)
        # Ordering columns
        self.current_content = self.current_content.reindex(
            dict(
                zip(
                    self.current_content.sum().sort_values(ascending=ascending).index,
                    self.current_content.columns,
                )
            ),
            axis=1,
        )
        
        # Set graphs attributes for plotter
        if y_label is not None:
            self.title_format = self.title.format(self.current_feature, y_label)
            self.y_axis_label = {"value": y_label}
        else:
            self.title_format = self.title.format(
                self.current_feature, self.y_axis_label
            )
            self.y_axis_label = {"value": self.y_axis_label}

        if title_suffix is not None:
            self.title_format += f" - ({title_suffix})"
        else:
            if self.title_suffix is not None:
                self.title_format += f" - ({self.title_suffix})"
        return self


class PlotterStorage(ABC):
    def __init__(self):
        self.figures = {}
        self.count = count()
        
    def add_graph(self, processor, type_graph, kind=None, resample=None, select_figures=False, download_html=False):
        def visual_data_wt():
            return dict(height=processor.height, width=processor.width, labels=processor.y_axis_label, template=processor.template)
        def visual_data_kind_wt(kind):
            return dict(kind=kind, height=processor.height, width=processor.width, labels=processor.y_axis_label, template=processor.template)

        num = next(self.count)
        if select_figures:
            if title := input("Ingrese título para guardar\nEnter para saltear"):
                
                if type_graph == "plot":
                    self.figure = processor.current_content.plot(
                        title = title,
                        **visual_data_wt()
                    )

                elif type_graph == "plot_areas":
                    self.figure = processor.current_content.plot.area(
                        title = title,
                        **visual_data_wt()
                    )

                elif type_graph == 'kind':
                    if resample:
                        with_resample = lambda obj, param: obj.current_content.resample(param).sum()
                        self.figure = with_resample(processor, resample).plot(
                            title=title,
                            **visual_data_kind_wt(kind)
                        )
                    else:
                        self.figure = processor.current_content.plot(
                            title=title,
                            **visual_data_kind_wt(kind)
                        )
                self.figures[processor.current_feature+'_'+str(num)] = self.figure
            
            if download_html:
                if name := input("Ingrese nombre para guardar\nEnter para salir"):
                    descargar_imagen(obj=self.figure, suffix=name)


class BackendPlotter:
    def __init__(self, processor):
        self.processor: VisualProcessor = processor

    def visual_data(self):
        return dict(title=self.processor.title_format, height=self.processor.height, width=self.processor.width, labels=self.processor.y_axis_label, template=self.processor.template)
    
    def visual_data_kind(self, kind):
        return dict(kind=kind, title=self.processor.title_format, height=self.processor.height, width=self.processor.width, labels=self.processor.y_axis_label, template=self.processor.template)
    
    def plot(self):
        self.figure = self.processor.current_content.plot(**self.visual_data())
        sleep(0.1)
        self.figure.show()
        return self.processor, 'plot'

    def plot_area(self):
        self.figure = self.processor.current_content.plot.area(**self.visual_data())
        sleep(0.1)
        self.figure.show()
        return self.processor, "plot_areas"

    def plot_kind(self, kind="bar", resample=None):
        with_resample = lambda obj, param: obj.current_content.resample(param).sum()
        if resample is not None:
            self.figure = with_resample(self.processor , resample).plot(**self.visual_data_kind(kind))
        else:
            self.figure = self.processor.current_content.plot(**self.visual_data_kind(kind))
        sleep(0.1)
        self.figure.show()
        return self.processor, 'kind', kind, resample


class GraphUploader:

    load_dotenv()
    USER = os.environ["USER_CS_J"]
    TOKEN = os.environ["TOKEN_CS_J"]
    tls.set_credentials_file(username=USER, api_key=TOKEN)
    pd.options.plotting.backend = "plotly"

    def __init__(self, storage):
        self.storage: PlotterStorage = storage
        self.figure = None

    def show_figures(self):
        print(f"Figures: {self.storage.figures.keys()}")

    def set_figure(self, figure=None, select=False):
        if figure is not None and list(self.storage.figures.keys()).count(figure) > 0:
            self.figure = True
            self.storage.figure = self.storage.figures[figure]
            return self

        elif select:
            print(f"Select Figure: {self.storage.figures.keys()}")
            while True:
                if name := input("Select figure = "):
                    if list(self.storage.figures.keys()).count(name) > 0:
                        self.figure = True
                        self.storage.figure = self.storage.figures[name]
                        return self
                    else:
                        print(
                            "label not found: check type writting or press enter to exit"
                        )
                        continue
                else:
                    print("Figure set up failed")
                break
        else:
            self.figure = None
            return self

    def show(self):
        if self.figure is None:
            return False
        self.storage.figure.show()

    def show_all(self):
        for figure in self.storage.figures.values():
            figure.show()

    def upload(self, filename, auto_open=True):
        if self.figure:
            py.plot(self.storage.figure, filename=filename, auto_open=auto_open)
        else:
            print ("It's necesary to apply method set_figure() first")

    def upload_all(self, auto_open=False):
        for key, figure in self.storage.figures.items():
            py.plot(figure, filename=input('select filename: '), auto_open=auto_open)
