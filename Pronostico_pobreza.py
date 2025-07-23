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
    full_data_raw = {
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
        'Valores 2022 (%)': [ # Data from the second image, cleaned to float where possible
            None, 16.0, 15.0, 1.1, 28.4, 9.6, 45.9,
            None, 44.5, 8.8,
            None, 13.5, 22.8, 27.2, 3.2, 3.8, 11.7,
            None, 3.8, 25.7
        ],
        'Pronóstico optimista 2024 (%)': [ # Data from the first image, cleaned to float where possible
            None, 12.2, 11.5, 0.7, 34.6, 6.7, 46.6,
            None, 46.8, 6.1,
            None, 13.7, 16.1, 27.2, 3.2, 3.8, 11.7,
            None, 2.8, 18.9
        ],
        'Pronóstico restrictivo 2024 (%)': [ # Data from the first image, cleaned to float where possible
            None, 15.1, 14.3, 0.8, 31.9, 8.6, 44.4,
            None, 47.0, 6.0,
            None, 13.7, 16.2, 27.2, 3.2, 3.8, 11.7,
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

        st.subheader("Visualización del Rango y Datos Anteriores (Pobreza) - Gráfico de Araña")

        # Prepare data for radar chart for poverty
        poverty_data_for_radar = {
            'Scenario': ['2022', '2024 (Optimista)', '2024 (Restrictivo)'],
            'Pobreza (%)': [poverty_2022, optimistic_poverty_2024, restrictive_poverty_2024]
        }
        df_poverty_radar = pd.DataFrame(poverty_data_for_radar)

        fig_poverty_radar = go.Figure()

        # Add traces for each scenario for poverty
        for index, row in df_poverty_radar.iterrows():
            color = 'blue'
            if 'Optimista' in row['Scenario']:
                color = 'green'
            elif 'Restrictivo' in row['Scenario']:
                color = 'red'

            fig_poverty_radar.add_trace(go.Scatterpolar(
                r=[row['Pobreza (%)']],
                theta=[row['Scenario']],
                mode='markers+lines',
                name=row['Scenario'],
                fill='toself',
                line_color=color,
                # Corrected hovertemplate: removed f-string around Plotly placeholders
                hovertemplate="<b>%{theta}</b><br>Pobreza: %{r:.1f}%<extra></extra>"
            ))

        fig_poverty_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(poverty_2022, restrictive_poverty_2024) * 1.1] # Dynamic range
                ),
                angularaxis=dict(
                    direction="clockwise",
                    period=len(df_poverty_radar['Scenario']),
                    tickvals=list(range(len(df_poverty_radar['Scenario']))),
                    ticktext=df_poverty_radar['Scenario'].tolist() # Set custom tick labels
                )
            ),
            showlegend=True,
            title='Población en Pobreza: 2022 vs. Pronósticos 2024 (Gráfico de Araña)'
        )
        st.plotly_chart(fig_poverty_radar, use_container_width=True)

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

        st.dataframe(df_full.style.hide(axis="index")) # Hides the index for cleaner display

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
                    range=[0, df_carencias.drop(columns=['Valores 2022 (%)']).max().max() * 1.1] # Dynamic range
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

            # Data for poverty comparison radar chart
            poverty_data_compare_radar = {
                'Scenario': ['2022', '2024 (Optimista)', '2024 (Restrictivo)', '2024 (Real)'],
                'Pobreza (%)': [poverty_2022, optimistic_poverty_2024, restrictive_poverty_2024, real_poverty_2024]
            }
            df_poverty_compare_radar = pd.DataFrame(poverty_data_compare_radar)

            fig_poverty_compare_radar = go.Figure()

            colors_map = {
                '2022': 'blue',
                '2024 (Optimista)': 'green',
                '2024 (Restrictivo)': 'red',
                '2024 (Real)': 'darkblue'
            }

            for index, row in df_poverty_compare_radar.iterrows():
                fig_poverty_compare_radar.add_trace(go.Scatterpolar(
                    r=[row['Pobreza (%)']],
                    theta=[row['Scenario']],
                    mode='markers+lines',
                    name=row['Scenario'],
                    fill='toself',
                    line_color=colors_map.get(row['Scenario'], 'grey'),
                    # Corrected hovertemplate: removed f-string around Plotly placeholders
                    hovertemplate="<b>%{theta}</b><br>Pobreza: %{r:.1f}%<extra></extra>"
                ))

            fig_poverty_compare_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max(poverty_2022, restrictive_poverty_2024, real_poverty_2024) * 1.1]
                    ),
                    angularaxis=dict(
                        direction="clockwise",
                        period=len(df_poverty_compare_radar['Scenario']),
                        tickvals=list(range(len(df_poverty_compare_radar['Scenario']))),
                        ticktext=df_poverty_compare_radar['Scenario'].tolist()
                    )
                ),
                showlegend=True,
                title='Población en Pobreza: Comparativa Real vs. Pronósticos (Gráfico de Araña)'
            )
            st.plotly_chart(fig_poverty_compare_radar, use_container_width=True)


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

            max_val = max(df_carencias.max(numeric_only=True).max(), max(real_carencias.values())) if real_carencias else df_carencias.max(numeric_only=True).max()
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