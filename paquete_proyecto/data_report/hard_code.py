from paquete_proyecto.data_report.plots import BackendPlotter


def plot_and_storage(processors, feature, storage):
    for i in range(len(processors)):
        if i < 2:
            storage.add_graph(*BackendPlotter(processor= processors[i].set_content(feature=feature)).plot())
            continue
        elif i < 4:
            storage.add_graph(*BackendPlotter(processor= processors[i].set_content(feature=feature)).plot_area())
            continue
        elif i == 4:
            storage.add_graph(*BackendPlotter(processor= processors[i].set_content(feature=feature)).plot_kind(kind="bar", resample="M"))
            continue
        elif i == 5:
            storage.add_graph(*BackendPlotter(processor= processors[i].set_content(feature=feature)).plot_kind(kind="bar", resample="W"))
        elif i == 6:
            storage.add_graph(*BackendPlotter(processor= processors[i].set_content(feature=feature)).plot_kind(kind="hist", resample="M"))
        elif i == 7:
            storage.add_graph(*BackendPlotter(processor= processors[i].set_content(feature=feature)).plot_kind(kind="hist", resample="W"))