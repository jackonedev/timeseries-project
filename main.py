import os
from dotenv import load_dotenv

# (I)
from paquete_proyecto.iniciando.bases import importar_databases, ajustar_tipos

# (II)
from paquete_proyecto.preprocesamiento.forex_api import alpha_vantage_fx_api
from paquete_proyecto.preprocesamiento.cotizacion import (
    criterio_valor_apertura,
    preparar_cotizacion,
    agregar_cotizacion,
)
from paquete_proyecto.preprocesamiento.muestreo import complete_dates


# PROGRAMA PRINCIPAL


def main():

    load_dotenv()

    # (I) Data Feed
    ventas, ventas_2 = importar_databases()
    ventas, ventas_2 = ajustar_tipos(ventas), ajustar_tipos(ventas_2)

    # (II) Data Prepare
    # Alpha Vantage API for Colombian Peso quotation, weekly from 2016 at 2020
    TOKEN = os.environ["TOKEN_AV"]
    cotizacion = alpha_vantage_fx_api("FX_WEEKLY", "COP", "USD", TOKEN)
    cotizacion = criterio_valor_apertura(
        preparar_cotizacion(ventas, cotizacion), "COP/USD"
    )

    # Adding quotation to column
    ventas, ventas_2 = agregar_cotizacion(ventas, cotizacion), agregar_cotizacion(
        ventas_2, cotizacion
    )

    # Express "Sell" in dolar currency
    ventas.loc[:, "Ventas_USD"], ventas_2.loc[:, "Ventas_USD"] = (
        ventas["Ventas"] * ventas["Cotizacion_USD"],
        ventas_2["Ventas"] * ventas_2["Cotizacion_USD"],
    )


if __name__ == "__main__":
    main()
