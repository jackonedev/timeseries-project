from paquete_proyecto.data_report.plots import BackendPlotter


def plot_and_storage(processors, feature, storage, select_figures, download_html=False):
    for i in range(len(processors)):
        if i < 2:
            storage.add_graph(*BackendPlotter(processor= processors[i].set_content(feature=feature)).plot(), select_figures=select_figures, download_html=download_html)
            continue
        elif i < 4:
            storage.add_graph(*BackendPlotter(processor= processors[i].set_content(feature=feature)).plot_area(), select_figures=select_figures, download_html=download_html)
            continue
        elif i == 4:
            storage.add_graph(*BackendPlotter(processor= processors[i].set_content(feature=feature)).plot_kind(kind="bar", resample="M"), select_figures=select_figures, download_html=download_html)
            continue
        elif i == 5:
            storage.add_graph(*BackendPlotter(processor= processors[i].set_content(feature=feature)).plot_kind(kind="bar", resample="W"), select_figures=select_figures, download_html=download_html)
        elif i == 6:
            storage.add_graph(*BackendPlotter(processor= processors[i].set_content(feature=feature)).plot_kind(kind="hist", resample="M"), select_figures=select_figures, download_html=download_html)
        elif i == 7:
            storage.add_graph(*BackendPlotter(processor= processors[i].set_content(feature=feature)).plot_kind(kind="hist", resample="W"), select_figures=select_figures, download_html=download_html)