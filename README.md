All data published in Zenodo - <a href="https://doi.org/10.5281/zenodo.15357334"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.15357334.svg" alt="DOI"></a>
Bursich, Daniele. «Mesh Overlap Tool». Zenodo, 7 maggio 2025.

# Mesh Overlap Analysis Dashboard

A Streamlit-based interactive application for statistical analysis of 1D datasets, with a strong emphasis on quality control and tolerance verification in industrial and metrological contexts.

## 📘 Theoretical Background

This tool operates in the domain of quantitative analysis of unidimensional datasets, especially relevant for dimensional control tasks (e.g., ISO 14253-1) or other precision measurement scenarios. It implements core principles of descriptive and inferential statistics, including standard deviation, skewness (Pearson, 1895), kurtosis, and RMSE (Root Mean Square Error), the latter widely used in accuracy assessment (see Willmott, 1981).

## 🖥️ Interface and User Experience

The dashboard is built using [Streamlit](https://streamlit.io), which allows interactive visual analytics with minimal development overhead. The configuration

```python
st.set_page_config(page_title="Analisi Mesh Overlap", layout="wide")
```

ensures that the layout is optimized for maximum data density per pixel, in line with the recommendations of Tufte (1983) for efficient visual design.

## 📂 Data Loading and Preprocessing

Data is uploaded via `.txt` files and preprocessed using:

```python
data = pd.to_numeric(pd.Series(raw), errors='coerce').dropna()
```

This line converts raw text lines into numeric values, coercing invalid entries to NaN and dropping them. This “fail-safe” approach aligns with best practices in robust preprocessing (Han et al., *Data Mining*, 2011), ensuring clean input for statistical processing.

## 📊 Statistical Computation

The analysis computes a comprehensive set of statistical descriptors:

- **Standard deviation and mean absolute deviation**: Reflect variability, with the former sensitive to outliers and the latter more robust (Mosteller & Tukey, 1977).
- **Skewness and kurtosis**: Capture distribution asymmetry and tail behavior; most interpretable in contrast to a Gaussian distribution.
- **Interquartile Range (IQR) and Tukey outliers**: Based on the canonical definitions from Tukey (1977), detect anomalous values beyond Q1 − 1.5×IQR and Q3 + 1.5×IQR.
- **RMSE**: Interpreted here as signal energy, or average quadratic deviation from zero.

All these metrics are consistent with statistical norms used in precision monitoring under ISO standards.

## 📈 Visualization and Comparative Analysis

Visualizations are rendered via `matplotlib`, embedded into Streamlit using `st.pyplot()`. Three primary plots are provided:

- A **histogram**, showing the distribution of values (see Cleveland, 1985).
- An **ordered scatter plot**, highlighting the sorted value distribution.
- An optional **radar chart**, aggregating tolerance percentages across multiple files—especially useful for comparative visual analytics.

The radar chart offers a synoptic view for multi-file, multi-feature comparison, ideal for quality assurance scenarios.

## 📝 Report Generation (PDF & ZIP)

A PDF report is generated using the [FPDF](https://pyfpdf.readthedocs.io/en/latest/) library, combining computed statistics with generated visualizations:

```python
pdf.image(fig1_path, w=180)
```

This integrated approach aligns with best practices in automatic reporting for audit trails and documentation. All output assets, including the PDF, radar plots, and image files, are bundled into a downloadable `.zip` archive using Python's `zipfile` module—ensuring portability and easy sharing in industrial contexts.

## 🛠️ Software Engineering Considerations

The project reflects common patterns in data science engineering:

- **Modular architecture**: Separates UI, analytics, and visualization logic.
- **Error resilience**: Uses `errors='coerce'` to safely handle input anomalies.
- **High customizability**: UI controls (sliders, color pickers, marker options).
- **Scalability**: Supports batch analysis and comparison of multiple datasets.

## 📚 Key References

- Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley.  
- Mosteller, F., & Tukey, J. W. (1977). *Data Analysis and Regression*.  
- Willmott, C. J. (1981). On the validation of models. *Climatic Change*.  
- Tufte, E. R. (1983). *The Visual Display of Quantitative Information*.  
- Knuth, D. E. (1997). *The Art of Computer Programming*, Vol. 1–3.  
- Han, J., Kamber, M., & Pei, J. (2011). *Data Mining: Concepts and Techniques*.  
- Pearson, K. (1895). *Contributions to the Mathematical Theory of Evolution*.  
