from io import BytesIO

import pandas as pd


def generar_excel_revenue(reservas, sincronizaciones, kpis):
    output = BytesIO()

    df_reservas = pd.DataFrame(reservas)
    df_sync = pd.DataFrame(sincronizaciones)
    df_kpis = pd.DataFrame([kpis])

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_kpis.to_excel(writer, index=False, sheet_name="KPIs")
        df_reservas.to_excel(writer, index=False, sheet_name="Reservas")
        df_sync.to_excel(writer, index=False, sheet_name="Sincronizaciones")

    output.seek(0)
    return output
