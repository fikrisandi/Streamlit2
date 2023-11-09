import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import streamlit as st
import pandas as pd
import cufflinks as cf


def app():
    st.markdown(    
        """
        <h1 style='text-align: center;'>Exploratory Data Analysis (EDA)</h1>
        """,
        unsafe_allow_html=True
    )

    # Menggunakan HTML untuk mengatur teks lebih rapi
    st.markdown(
        """
        <h3 style='text-align: center;'>Informasi Dataset</h3>
        <p  style='text-align: justify;'>Dataset yang digunakan adalah `citi_day.csv` yang berasal dari `Kaggle`. Dataset ini bersifat open source, sehingga dapat diakses oleh siapa pun. Dataset ini berisi tentang `kualitas udara` pada negara `India` pada tahun `2015 - 2022`. 
        Tujuan dari proyek ini adalah memanfaatkan dataset `citi_day.csv` untuk membangun model prediksi kualitas udara yang dapat membantu dalam pemantauan dan identifikasi daerah-daerah yang memerlukan perhatian terkait polusi udara di India. Dalam upaya mencapai tujuan tersebut, dilaukan implementasi beberapa metode machine learning `Classification`, termasuk K-Nearest Neighbors (KNN), Support Vector Machine (SVM), Decision Tree, Random Forest, dan Boosting. Kemudian akan dicari metode yang mempunyai performa terbaik, untuk mengetahui model dengan performa terbaik akan dilakukan evaluasi kinerja model-model tersebut menggunakan sejumlah metrik evaluasi yang relevan.</p>
        """,
        unsafe_allow_html=True  # Mengizinkan penggunaan HTML
    )

    df = pd.read_csv('../city_day.csv')

    st.markdown('---')

    st.markdown(
        """
        <h3 style='text-align: center;'>Cek Outliers Data Numeric</h3>
        """,
        unsafe_allow_html=True  # Mengizinkan penggunaan HTML
    )

    fig = make_subplots(rows=2, cols=7)
    row_no = col_no = 1

    # Iterate through columns and create boxplots
    for col in df.columns:
        if df[col].dtype != "O":
            fig.add_trace(
                go.Box(y=df[col], name=col),
                row=row_no,
                col=col_no,
            )
            col_no += 1
            if col_no > 7:
                row_no += 1
                col_no = 1

    # Display the plot using Streamlit
    st.plotly_chart(fig)

    st.markdown('---')
    
    st.markdown(
        """
        <h3 style='text-align: center;'>Mengecek Distribusi Data</h3>
        <h4 style='text-align: center;'>1. Distribusi Data Numeric</h4>
        """,
        unsafe_allow_html=True  # Mengizinkan penggunaan HTML
    )
    list_num = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene', 'AQI']
    selected_column = st.selectbox("Pilih kolom feature numerik:", list_num)

    # Display histogram for the selected numeric column
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.hist(df[selected_column], bins=20, edgecolor='black', color='blue')
    ax.set_xlabel(selected_column, fontsize=8)
    ax.set_ylabel('Frequency', fontsize=8)
    plt.title(f'Histogram of {selected_column}')
    st.pyplot(fig)
    
    st.markdown('---')
    
    st.markdown(
        """
        <h4 style='text-align: center;'>2. Distribusi Data Variabel Target</h4>
        """,
        unsafe_allow_html=True  # Mengizinkan penggunaan HTML
    )
    df_aqi_bucket = df[['AQI_Bucket']]
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.countplot(x='AQI_Bucket', data=df_aqi_bucket, palette='viridis')
    ax.set_xlabel('AQI_Bucket', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    plt.title('Bar Chart of AQI_Bucket')
    st.pyplot(fig)

    # Load your dataframe (df) here

    # Data cleaning and processing
    df['Date'] = pd.to_datetime(df['Date'])

    # List of numeric columns for filling missing values
    numeric_columns = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene']

    # Fill missing values with median for each numeric column
    df[numeric_columns] = df[numeric_columns].apply(lambda x: x.fillna(x.median()))

    # Fill missing values for 'AQI' column with median
    df['AQI'] = df['AQI'].fillna(df['AQI'].median())

    # Fill missing values for 'AQI_Bucket' column with 'Moderate'
    df['AQI_Bucket'] = df['AQI_Bucket'].fillna('Moderate')

    # Calculate 'Vehicular Pollution' and 'Industrial Pollution'
    df['Vehicular Pollution'] = df['PM2.5'] + df['PM10'] + df['NO'] + df['NO2'] + df['NOx'] + df['NH3'] + df['CO']
    df['Industrial Pollution'] = df['SO2'] + df['O3'] + df['Benzene'] + df['Toluene'] + df['Xylene']

    # Filter data before and after 2020
    df_before_2020 = df[df['Date'] <= '2020-01-01']
    df_after_2020 = df[df['Date'] > '2020-01-01']

    # Create a Streamlit app
    st.title("Plotting Vehicular and Industrial Pollution")

    # Add dropdown to select data and variable
    selected_data_var = st.selectbox("Select Data and Variable", 
                                    [('Before 2020 - Vehicular Pollution', 'Vehicular Pollution'),
                                    ('Before 2020 - Industrial Pollution', 'Industrial Pollution'),
                                    ('After 2020 - Vehicular Pollution', 'Vehicular Pollution'),
                                    ('After 2020 - Industrial Pollution', 'Industrial Pollution')])

    # Plot the selected variable for the selected data
    if selected_data_var:
        data_label, var_label = selected_data_var
        df_selected = df_before_2020 if 'Before' in data_label else df_after_2020
        st.plotly_chart(df_selected[var_label].iplot(asFigure=True, title=var_label, xTitle='Cities', yTitle=var_label, linecolor='black'))

