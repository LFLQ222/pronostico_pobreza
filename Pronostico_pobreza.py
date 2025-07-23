import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def app():
    st.set_page_config(layout="wide") # Use wide layout for better chart display
    st.title("Simulador de Pobreza 2024 con Datos ENOE-INEGI")

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

    # Previous Year Data (2022)
    poverty_2022 = 16.0

    # Data for social deprivations (carencias sociales)
    # Extracting relevant rows for carencias from the full data
    # Full data for both 2022 and 2024 forecasts (parsed from the images)
    # Organized into four main categories
    full_data_raw = {
        'Categoría': [
            # POBREZA
            'POBREZA', 'POBREZA', 'POBREZA', 'POBREZA', 'POBREZA', 'POBREZA', 'POBREZA',
            # PRIVACIÓN SOCIAL
            'PRIVACIÓN SOCIAL', 'PRIVACIÓN SOCIAL', 'PRIVACIÓN SOCIAL',
            # INDICADORES DE CARENCIA SOCIAL
            'INDICADORES DE CARENCIA SOCIAL', 'INDICADORES DE CARENCIA SOCIAL', 'INDICADORES DE CARENCIA SOCIAL', 'INDICADORES DE CARENCIA SOCIAL', 'INDICADORES DE CARENCIA SOCIAL', 'INDICADORES DE CARENCIA SOCIAL', 'INDICADORES DE CARENCIA SOCIAL',
            # BIENESTAR ECONÓMICO
            'BIENESTAR ECONÓMICO', 'BIENESTAR ECONÓMICO', 'BIENESTAR ECONÓMICO'
        ],
        'Variable': [
            # POBREZA
            'Pobreza',
            'Población en pobreza',
            'Población en pobreza moderada',
            'Población en pobreza extrema',
            'Población vulnerable por carencias sociales',
            'Población vulnerable por ingresos',
            'Población no pobre y no vulnerable',
            # PRIVACIÓN SOCIAL
            'Privación social',
            'Población con al menos una carencia social',
            'Población con al menos tres carencias sociales',
            # INDICADORES DE CARENCIA SOCIAL
            'Indicadores de carencia social',
            'Rezago educativo',
            'Carencia por acceso a los servicios de salud',
            'Carencia por acceso a la seguridad social',
            'Carencia por calidad y espacios de la vivienda',
            'Carencia por acceso a los servicios básicos de la vivienda',
            'Carencia por acceso a la alimentación nutritiva y de calidad',
            # BIENESTAR ECONÓMICO
            'Bienestar económico',
            'Población con ingreso inferior a la linea de pobreza extrema por ingresos',
            'Población con ingreso inferior a la linea de pobreza por ingresos'
        ],
        'Valores 2022 (%)': [ # Data from the second image, cleaned to float where possible
            # POBREZA
            None, 16.0, 15.0, 1.1, 28.4, 9.6, 45.9,
            # PRIVACIÓN SOCIAL
            None, 44.5, 8.8,
            # INDICADORES DE CARENCIA SOCIAL
            None, 13.5, 22.8, 27.2, 3.2, 3.8, 11.7,
            # BIENESTAR ECONÓMICO
            None, 3.8, 25.7
        ],
        'Pronóstico optimista 2024 (%)': [ # Data from the first image, cleaned to float where possible
            # POBREZA
            None, 12.2, 11.5, 0.7, 34.6, 6.7, 46.6,
            # PRIVACIÓN SOCIAL
            None, 46.8, 6.1,
            # INDICADORES DE CARENCIA SOCIAL
            None, 13.7, 16.1, 27.2, 3.2, 3.8, 11.7,
            # BIENESTAR ECONÓMICO
            None, 2.8, 18.9
        ],
        'Pronóstico restrictivo 2024 (%)': [ # Data from the first image, cleaned to float where possible
            # POBREZA
            None, 15.1, 14.3, 0.8, 31.9, 8.6, 44.4,
            # PRIVACIÓN SOCIAL
            None, 47.0, 6.0,
            # INDICADORES DE CARENCIA SOCIAL
            None, 13.7, 16.2, 27.2, 3.2, 3.8, 11.7,
            # BIENESTAR ECONÓMICO
            None, 3.4, 23.7
        ]
    }

    df_full = pd.DataFrame(full_data_raw)

    # Define the carencias variables for easy access
    carencias_variables = [
        'Rezago educativo',
        'Carencia por acceso a los servicios de salud',
        'Carencia por acceso a la seguridad social',
        'Carencia por calidad y espacios de la vivienda',
        'Carencia por acceso a los servicios básicos de la vivienda',
        'Carencia por acceso a la alimentación nutritiva y de calidad'
    ]

    # Define variables by category for easy access
    pobreza_variables = [
        'Población en pobreza',
        'Población en pobreza moderada',
        'Población en pobreza extrema',
        'Población vulnerable por carencias sociales',
        'Población vulnerable por ingresos',
        'Población no pobre y no vulnerable'
    ]
    
    privacion_social_variables = [
        'Población con al menos una carencia social',
        'Población con al menos tres carencias sociales'
    ]
    
    bienestar_economico_variables = [
        'Población con ingreso inferior a la linea de pobreza extrema por ingresos',
        'Población con ingreso inferior a la linea de pobreza por ingresos'
    ]

    # --- TABS ---
    tab1, tab2 = st.tabs(["Análisis de Pronósticos", "Cargar Datos Reales 2024"])

    with tab1:
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

        st.subheader("Visualización del Rango y Datos Anteriores (Pobreza) - Gráfico de Barras")

        # Prepare data for bar chart for poverty
        poverty_data_for_bar = {
            'Escenario': ['2022', '2024 (Optimista)', '2024 (Restrictivo)'],
            'Pobreza (%)': [poverty_2022, optimistic_poverty_2024, restrictive_poverty_2024]
        }
        df_poverty_bar = pd.DataFrame(poverty_data_for_bar)
        


        # Create bar chart with explicit configuration
        fig_poverty_bar = px.bar(
            df_poverty_bar,
            x='Escenario',
            y='Pobreza (%)',
            color='Escenario',
            color_discrete_map={
                '2022': 'blue',
                '2024 (Optimista)': 'green',
                '2024 (Restrictivo)': 'red'
            },
            title='Población en Pobreza: 2022 vs. Pronósticos 2024 (Gráfico de Barras)',
            text='Pobreza (%)'
        )
        
        # Force x-axis to be categorical
        fig_poverty_bar.update_xaxes(type='category')

        # Update layout for better presentation
        fig_poverty_bar.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside'
        )
        
        fig_poverty_bar.update_layout(
            xaxis_title="Escenario",
            yaxis_title="Pobreza (%)",
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig_poverty_bar, use_container_width=True)

        st.markdown(
            """
            ---
            **Nota:** Este "intervalo de confianza" se deriva directamente de los dos pronósticos
            (optimista y restrictivo) y no es un intervalo de confianza estadístico formal que requeriría
            más datos o supuestos sobre la distribución. Representa el rango de resultados esperados
            según las proyecciones dadas.
            """
        )

        st.header("2. Detalles Completos de Indicadores por Categorías (2022 y Pronósticos 2024)")

        # Display data organized by categories
        for categoria in ['POBREZA', 'PRIVACIÓN SOCIAL', 'INDICADORES DE CARENCIA SOCIAL', 'BIENESTAR ECONÓMICO']:
            st.subheader(f"**{categoria}**")
            df_categoria = df_full[df_full['Categoría'] == categoria]
            st.dataframe(df_categoria[['Variable', 'Valores 2022 (%)', 'Pronóstico optimista 2024 (%)', 'Pronóstico restrictivo 2024 (%)']].style.hide(axis="index"))
            st.markdown("---")

        st.markdown(
            """
            Para cada variable, puedes observar los valores de 2022 y los rangos de pronóstico para 2024.
            La comparación entre estos te da una idea de la variación esperada.
            """
        )

        st.subheader("Visualización de Carencias Sociales")

        # Prepare data for radar chart for carencias
        df_carencias = df_full[df_full['Variable'].isin(carencias_variables)].set_index('Variable')

        fig_carencias_radar = go.Figure()

        # Add traces for each year/forecast
        fig_carencias_radar.add_trace(go.Scatterpolar(
              r=df_carencias['Valores 2022 (%)'].tolist(),
              theta=carencias_variables,
              fill='toself',
              name='2022',
              line_color='blue'
        ))
        fig_carencias_radar.add_trace(go.Scatterpolar(
              r=df_carencias['Pronóstico optimista 2024 (%)'].tolist(),
              theta=carencias_variables,
              fill='toself',
              name='2024 (Optimista)',
              line_color='green'
        ))
        fig_carencias_radar.add_trace(go.Scatterpolar(
              r=df_carencias['Pronóstico restrictivo 2024 (%)'].tolist(),
              theta=carencias_variables,
              fill='toself',
              name='2024 (Restrictivo)',
              line_color='red'
        ))

        fig_carencias_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, df_carencias[['Pronóstico optimista 2024 (%)', 'Pronóstico restrictivo 2024 (%)']].max().max() * 1.1] # Dynamic range
                )),
            showlegend=True,
            title='Comparativa de Carencias Sociales: 2022 vs. Pronósticos 2024'
        )
        st.plotly_chart(fig_carencias_radar, use_container_width=True)


    with tab2:
        st.header("Cargar Datos Reales 2024")
        st.write(
            """
            Si tienes los datos reales para 2024, puedes ingresarlos aquí para compararlos
            con los pronósticos y los valores de 2022.
            """
        )

        st.subheader("Datos Reales de Pobreza (2024)")
        real_poverty_2024 = st.number_input(
            "Porcentaje de Población en Pobreza Real 2024 (%)",
            min_value=0.0, max_value=100.0, value=optimistic_poverty_2024, step=0.1
        )

        st.subheader("Datos Reales de Carencias Sociales (2024)")
        real_carencias = {}
        for carencia in carencias_variables:
            # Get default value from optimistic forecast if available, otherwise 0.0
            default_value = df_full[df_full['Variable'] == carencia]['Pronóstico optimista 2024 (%)'].iloc[0] if not df_full[df_full['Variable'] == carencia]['Pronóstico optimista 2024 (%)'].empty else 0.0
            real_carencias[carencia] = st.number_input(
                f"Porcentaje de '{carencia}' Real 2024 (%)",
                min_value=0.0, max_value=100.0, value=default_value, step=0.1, key=f"real_{carencia}"
            )

        if st.button("Comparar Datos Reales"):
            st.markdown("---")
            st.subheader("Comparativa de 'Población en Pobreza' (Real vs. Pronósticos vs. 2022)")

            # Data for poverty comparison bar chart
            poverty_data_compare_bar = {
                'Escenario': ['2022', '2024 (Optimista)', '2024 (Restrictivo)', '2024 (Real)'],
                'Pobreza (%)': [poverty_2022, optimistic_poverty_2024, restrictive_poverty_2024, real_poverty_2024]
            }
            df_poverty_compare_bar = pd.DataFrame(poverty_data_compare_bar)

            # Create comparison bar chart
            fig_poverty_compare_bar = px.bar(
                df_poverty_compare_bar,
                x='Escenario',
                y='Pobreza (%)',
                color='Escenario',
                color_discrete_map={
                    '2022': 'blue',
                    '2024 (Optimista)': 'green',
                    '2024 (Restrictivo)': 'red',
                    '2024 (Real)': 'darkblue'
                },
                title='Población en Pobreza: Comparativa Real vs. Pronósticos (Gráfico de Barras)',
                text='Pobreza (%)'
            )

            # Update layout for better presentation
            fig_poverty_compare_bar.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside'
            )
            
            fig_poverty_compare_bar.update_layout(
                xaxis_title="Escenario",
                yaxis_title="Pobreza (%)",
                showlegend=True,
                height=500
            )
            
            st.plotly_chart(fig_poverty_compare_bar, use_container_width=True)


            st.subheader("Comparativa de Carencias Sociales (Real vs. Pronósticos vs. 2022)")

            fig_carencias_compare_radar = go.Figure()

            # Add traces for each scenario
            fig_carencias_compare_radar.add_trace(go.Scatterpolar(
                  r=df_carencias['Valores 2022 (%)'].tolist(),
                  theta=carencias_variables,
                  fill='toself',
                  name='2022',
                  line_color='blue'
            ))
            fig_carencias_compare_radar.add_trace(go.Scatterpolar(
                  r=df_carencias['Pronóstico optimista 2024 (%)'].tolist(),
                  theta=carencias_variables,
                  fill='toself',
                  name='2024 (Optimista)',
                  line_color='green'
            ))
            fig_carencias_compare_radar.add_trace(go.Scatterpolar(
                  r=df_carencias['Pronóstico restrictivo 2024 (%)'].tolist(),
                  theta=carencias_variables,
                  fill='toself',
                  name='2024 (Restrictivo)',
                  line_color='red'
            ))
            # Add real data trace
            fig_carencias_compare_radar.add_trace(go.Scatterpolar(
                  r=[real_carencias[c] for c in carencias_variables],
                  theta=carencias_variables,
                  fill='toself',
                  name='2024 (Real)',
                  line_color='darkblue',
                  line_width=3
            ))

            max_val = max(df_carencias[['Valores 2022 (%)', 'Pronóstico optimista 2024 (%)', 'Pronóstico restrictivo 2024 (%)']].max().max(), max(real_carencias.values())) if real_carencias else df_carencias[['Valores 2022 (%)', 'Pronóstico optimista 2024 (%)', 'Pronóstico restrictivo 2024 (%)']].max().max()
            fig_carencias_compare_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max_val * 1.1]
                    )),
                showlegend=True,
                title='Comparativa de Carencias Sociales: Real vs. Pronósticos vs. 2022'
            )
            st.plotly_chart(fig_carencias_compare_radar, use_container_width=True)


if __name__ == "__main__":
    app()