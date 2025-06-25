# Requirements Fix:
# This code assumes that matplotlib is installed.
# To ensure all packages are available, run:
# pip install streamlit pandas numpy matplotlib scipy fpdf

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew
from fpdf import FPDF
from io import BytesIO
import base64
from datetime import datetime
from zipfile import ZipFile

st.set_page_config(page_title="Analisi Mesh Overlap", layout="wide")

# Interfaccia utente
st.markdown("# Dashboard Analisi Sovrapposizione Mesh")
titolo = st.text_input("Titolo Analisi", "Analisi di Sovrapposizione")
data_analisi = st.date_input("Data analisi", value=datetime.today())

with st.expander("📘 Manuale dei parametri statistici"):
    st.markdown("""
**Totale Punti**: Numero totale di righe/valori letti dal file.
**NaN Rimossi**: Valori non numerici scartati (ad es. celle vuote).
**Punti Utili**: Valori effettivamente analizzati dopo la pulizia.
**Media**: Valore medio dei dati.
**Dev. Std**: Scostamento medio dei dati rispetto alla media.
**Deviazione Media**: Media degli scostamenti assoluti dalla media.
**Skewness**: Indica asimmetria della distribuzione.
**Kurtosi**: Misura l'appuntimento della distribuzione.
**RMSE**: Errore quadratico medio.
**Minimo/Massimo**: Valori estremi del dataset.
**Quartili (Q1, Q2, Q3)**: Suddivisione percentuale dei dati.
**IQR**: Intervallo interquartile (Q3 - Q1).
**Outlier Alti/Bassi**: Valori oltre i limiti di Tukey.
**% in Tolleranza**: Percentuale di punti entro ±tolleranza.
""")

# Sidebar
st.sidebar.markdown("## ⚙️ Personalizzazione Grafici")
marker_size = st.sidebar.slider("Dimensione marker scatter", 2, 20, 4)
hist_color = st.sidebar.color_picker("Colore istogramma", value="#87ceeb")
font_size = st.sidebar.slider("Dimensione testo grafici", 8, 20, 10)
marker_shape = st.sidebar.selectbox("Forma marker scatter", ["o", "s", "^", "*", "x"])

uploaded_files = st.sidebar.file_uploader("Carica uno o più file .txt", type="txt", accept_multiple_files=True)
immagine = st.sidebar.file_uploader("Carica immagine di intestazione", type=['png','jpg','jpeg'])
tolerance = st.sidebar.number_input("Tolleranza ±", value=0.003, min_value=0.0001, max_value=0.1, step=0.001, format="%0.4f")
radar_enabled = st.sidebar.checkbox("Abilita grafico radar se > 1 file")
compare_enabled = st.sidebar.checkbox("Confronta tutti i file in una tabella unica")

if uploaded_files:
    if immagine:
        st.image(immagine, width=180)

    radar_data = {}
    radar_buf = BytesIO()
    pdf = FPDF()
    pdf.set_font("Arial", 'B', size=16)
    pdf.add_page()
    pdf.cell(200, 10, txt="Analisi Sovrapposizione Mesh", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Titolo: {titolo}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Data: {data_analisi.strftime('%d/%m/%Y')}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt="Indice dei File Analizzati", ln=True)
    pdf.set_font("Arial", size=12)
    for f in uploaded_files:
        pdf.cell(200, 10, txt=f"- {f.name}", ln=True)
    pdf.add_page()

    if compare_enabled:
        all_data = []
        all_stats = []
        for file in uploaded_files:
            with st.expander(f"📄 File: {file.name}"):
                file.seek(0)
                raw = file.read().decode("utf-8").splitlines()
                data = pd.to_numeric(pd.Series(raw), errors='coerce').dropna()
                df = pd.DataFrame({"Valore": data})
                df["File"] = file.name
                all_data.append(df)
                stats = {
                    "File": file.name,
                    "Media": data.mean(),
                    "Dev Std": data.std(),
                    "% in Tolleranza ±": ((data.between(-tolerance, tolerance)).sum() / len(data)) * 100
                }
                all_stats.append(stats)
        df_compare = pd.DataFrame(all_stats)
        df_all_data = pd.concat(all_data)
        with st.expander("📋 Confronto Globale tra i File"):
            st.dataframe(df_compare)
            fig, ax = plt.subplots()
            df_compare.plot(kind='bar', x='File', y='% in Tolleranza ±', ax=ax, legend=False, color='skyblue')
            ax.set_ylabel('% in Tolleranza')
            ax.set_title('Confronto Tolleranza tra i File')
            st.pyplot(fig)
            fig2, ax2 = plt.subplots()
            for label, group in df_all_data.groupby("File"):
                ax2.hist(group["Valore"], bins=100, alpha=0.5, label=label)
            ax2.set_title("Istogramma Confronto Globale")
            ax2.set_xlabel("Valori")
            ax2.set_ylabel("Frequenza")
            ax2.legend()
            st.pyplot(fig2)
            fig3, ax3 = plt.subplots()
            for label, group in df_all_data.groupby("File"):
                sorted_vals = np.sort(group["Valore"])
                ax3.plot(sorted_vals, label=label)
            ax3.set_title("Scatter Plot Ordinato Confrontato")
            ax3.set_xlabel("Indice")
            ax3.set_ylabel("Valore")
            ax3.legend()
            st.pyplot(fig3)

    for file in uploaded_files:
        with st.expander(f"📄 File: {file.name}"):
            file.seek(0)
            raw = file.read().decode("utf-8").splitlines()
            data = pd.to_numeric(pd.Series(raw), errors='coerce')
            total_points = len(data)
            clean_data = data.dropna().reset_index(drop=True)
            selected_range = clean_data[clean_data.between(-tolerance, tolerance, inclusive='both')]
            nan_removed = total_points - len(clean_data)

            q1 = np.percentile(clean_data, 25)
            q3 = np.percentile(clean_data, 75)
            iqr = q3 - q1
            outlier_low = clean_data < (q1 - 1.5 * iqr)
            outlier_high = clean_data > (q3 + 1.5 * iqr)

            stats = {
                "Totale Punti": total_points,
                "NaN Rimossi": nan_removed,
                "Punti Utili": len(clean_data),
                "In tolleranza": clean_data.between(-tolerance, tolerance, inclusive='both').sum(),
                "Minimo": selected_range.min(),
                "Massimo": selected_range.max(),
                "Media": selected_range.mean(),
                "Dev. Std": selected_range.std(),
                # "Deviazione Media": np.mean(np.abs(clean_data - clean_data.mean())),
                # "Skewness": skew(clean_data),
                # "Kurtosi": clean_data.kurtosis(),
                # "RMSE": np.sqrt(np.mean(clean_data ** 2)),
                "Q1": q1,
                "Mediana": np.percentile(selected_range, 50),
                "Q3": q3,
                # "IQR": iqr,
                # "Outlier Bassi": outlier_low.sum(),
                # "Outlier Alti": outlier_high.sum(),
                "% in Tolleranza ±": ((clean_data.between(-tolerance, tolerance, inclusive='both')).sum() / len(clean_data)) * 100
            }
            
            radar_data[file.name] = stats["% in Tolleranza ±"]

            st.dataframe(pd.DataFrame([stats]))

            col1, col2 = st.columns(2)
            with col1:
                fig1, ax1 = plt.subplots()
                ax1.hist(clean_data, bins=100, color=hist_color, edgecolor='black')
                ax1.axvline(tolerance, color='green', linestyle='--')
                ax1.axvline(-tolerance, color='green', linestyle='--')
                ax1.set_title("Istogramma")
                st.pyplot(fig1)
            with col2:
                fig2, ax2 = plt.subplots()
                sorted_data = np.sort(clean_data)
                ax2.scatter(range(len(sorted_data)), sorted_data, s=marker_size, alpha=0.6, marker=marker_shape)
                ax2.axhline(tolerance, color='green', linestyle='--')
                ax2.axhline(-tolerance, color='green', linestyle='--')
                ax2.set_title("Grafico Scatter Ordinato")
                st.pyplot(fig2)

            pdf.set_font("Arial", 'B', size=12)
            pdf.cell(200, 10, txt=f"File: {file.name}", ln=True)
            pdf.set_font("Arial", size=10)
            for k, v in stats.items():
                pdf.cell(200, 10, txt=f"{k}: {v}", ln=True)

            fig1_path = f"{file.name}_hist.png"
            fig2_path = f"{file.name}_scatter.png"
            fig1.savefig(fig1_path)
            fig2.savefig(fig2_path)
            pdf.image(fig1_path, w=180)
            pdf.image(fig2_path, w=180)

    if radar_enabled and len(radar_data) > 1:
        st.subheader("📊 Radar plot - % in tolleranza")
        labels = list(radar_data.keys())
        values = list(radar_data.values())
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]
        fig_radar, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        ax.plot(angles, values, linewidth=1)
        ax.fill(angles, values, alpha=0.3)
        ax.set_thetagrids(np.degrees(angles[:-1]), labels)
        st.pyplot(fig_radar)
        fig_radar.savefig(radar_buf, format='png')
        radar_buf.seek(0)
        with open("radar_plot.png", "wb") as f:
            f.write(radar_buf.read())
        pdf.image("radar_plot.png", w=180)

    pdf_output = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    b64 = base64.b64encode(pdf_output.read()).decode()
    href = f"<a href='data:application/pdf;base64,{b64}' download='Analisi_{data_analisi.strftime('%Y%m%d')}.pdf'>📄 Scarica PDF</a>"
    st.markdown(href, unsafe_allow_html=True)

    zip_buf = BytesIO()
    with ZipFile(zip_buf, "w") as zipf:
        zipf.writestr("README.txt", f"""Contenuto del file ZIP:
- Analisi_{data_analisi.strftime('%Y%m%d')}.pdf: Report PDF dell'analisi
- radar_plot.png: Grafico radar (se generato)
- *_hist.png: Istogrammi per ciascun file caricato
- *_scatter.png: Grafici scatter per ciascun file caricato
""")
        zipf.writestr(f"Analisi_{data_analisi.strftime('%Y%m%d')}.pdf", pdf_output.getvalue())

    zip_buf.seek(0)
    st.download_button("📦 Scarica ZIP", data=zip_buf, file_name=f"Analisi_{data_analisi.strftime('%Y%m%d')}.zip", mime="application/zip")
