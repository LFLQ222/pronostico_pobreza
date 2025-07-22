import streamlit as st
import pandas as pd

def app():
    st.set_page_config(layout="centered")
    st.title("Simulador de Pobreza 2024")

    st.write(
        """
        Esta aplicación presenta un simulador de pobreza para el año 2024, utilizando datos
        históricos de 2022 y pronósticos optimistas y restrictivos. Los datos base para
        este análisis se originan de la **Encuesta Nacional de Ocupación y Empleo (ENOE) del INEGI**.
        """
    )

    # Data from the images
    # Forecasts (2024)
    optimistic_poverty_2024 = 12.2
    restrictive_poverty_2024 = 15.1

    # Previous Year Data (2022) - from the second image
    poverty_2022 = 16.0

    st.header("1. Análisis de 'Población en Pobreza'")

    st.write(f"""
        Para el indicador 'Población en pobreza':
        * **Valor en 2022:** {poverty_2022}%
        * **Pronóstico Optimista 2024:** {optimistic_poverty_2024}%
        * **Pronóstico Restrictivo 2024:** {restrictive_poverty_2024}%
    """)

    st.subheader("Intervalo de Confianza Implícito para 2024")
    st.markdown(f"""
        Considerando los pronósticos, el intervalo de confianza implícito
        para la 'Población en pobreza' en 2024 es: **[{optimistic_poverty_2024}%, {restrictive_poverty_2024}%]**
    """)

    st.subheader("Variación Respecto a 2022")

    # Calculate variations
    variation_optimistic = optimistic_poverty_2024 - poverty_2022
    variation_restrictive = restrictive_poverty_2024 - poverty_2022

    st.write(f"""
        * **Variación (2024 Optimista vs. 2022):** {variation_optimistic:.1f} puntos porcentuales
        * **Variación (2024 Restrictivo vs. 2022):** {variation_restrictive:.1f} puntos porcentuales
    """)

    st.markdown(
        """
        La variación indica el cambio proyectado en el porcentaje de población en pobreza
        desde 2022 hasta los escenarios de pronóstico de 2024. Un valor negativo indica
        una disminución, mientras que un valor positivo indica un aumento.
        """
    )

    st.subheader("Visualización del Rango y Datos Anteriores")

    # Create a simple DataFrame for display
    data_poverty = {
        'Año/Pronóstico': ['2022', '2024 (Optimista)', '2024 (Restrictivo)'],
        'Población en Pobreza (%)': [poverty_2022, optimistic_poverty_2024, restrictive_poverty_2024]
    }
    df_poverty = pd.DataFrame(data_poverty)
    st.dataframe(df_poverty.style.hide(axis="index"))

    st.markdown(
        """
        ---
        **Nota:** Este "intervalo de confianza" se deriva directamente de los dos pronósticos
        (optimista y restrictivo) y no es un intervalo de confianza estadístico formal que requeriría
        más datos o supuestos sobre la distribución. Representa el rango de resultados esperados
        según las proyecciones dadas.
        """
    )

    st.header("2. Detalles Completos de Indicadores (2022 y Pronósticos 2024)")

    # Full data for both 2022 and 2024 forecasts
    full_data = {
        'Variable': [
            'Pobreza',
            'Población en pobreza',
            'Población en pobreza moderada',
            'Población en pobreza extrema',
            'Población vulnerable por carencias sociales',
            'Población vulnerable por ingresos',
            'Población no pobre y no vulnerable',
            'Privación social',
            'Población con al menos una carencia social',
            'Población con al menos tres carencias sociales',
            'Indicadores de carencia social',
            'Rezago educativo',
            'Carencia por acceso a los servicios de salud',
            'Carencia por acceso a la seguridad social',
            'Carencia por calidad y espacios de la vivienda',
            'Carencia por acceso a los servicios básicos de la vivienda',
            'Carencia por acceso a la alimentación nutritiva y de calidad',
            'Bienestar económico',
            'Población con ingreso inferior a la linea de pobreza extrema por ingresos',
            'Población con ingreso inferior a la linea de pobreza por ingresos'
        ],
        'Valores 2022 (%)': [ # Data from the second image
            '', '16.0', '15.0', '1.1', '28.4', '9.6', '45.9',
            '', '44.5', '8.8',
            '', '13.5', '22.8', '27.2', '3.2', '3.8', '11.7',
            '', '3.8', '25.7'
        ],
        'Pronóstico optimista 2024 (%)': [ # Data from the first image
            '', '12.2', '11.5', '0.7', '34.6', '6.7', '46.6',
            '', '46.8', '6.1',
            '', '13.7', '16.1', '27.2', '3.2', '3.8', '11.7',
            '', '2.8', '18.9'
        ],
        'Pronóstico restrictivo 2024 (%)': [ # Data from the first image
            '', '15.1', '14.3', '0.8', '31.9', '8.6', '44.4',
            '', '47.0', '6.0',
            '', '13.7', '16.2', '27.2', '3.2', '3.8', '11.7',
            '', '3.4', '23.7'
        ]
    }

    df_full = pd.DataFrame(full_data)
    st.dataframe(df_full.style.hide(axis="index")) # Hides the index for cleaner display

    st.markdown(
        """
        Para cada variable, puedes observar los valores de 2022 y los rangos de pronóstico para 2024.
        La comparación entre estos te da una idea de la variación esperada.
        """
    )


if __name__ == "__main__":
    app()