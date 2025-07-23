import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def app():
    st.set_page_config(layout="wide", page_title="Simulador de Pobreza 2024 - Versión Mejorada")
    
    # Custom CSS for better styling with improved contrast
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card h3 {
        color: #374151;
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        font-weight: 600;
    }
    .metric-card h2 {
        color: #111827;
        margin: 0 0 0.25rem 0;
        font-size: 2rem;
        font-weight: 700;
    }
    .metric-card p {
        color: #6b7280;
        margin: 0;
        font-size: 0.875rem;
    }
    .insight-box {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff7f0e;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .insight-box h4 {
        color: #111827;
        margin: 0 0 0.5rem 0;
        font-weight: 600;
    }
    .insight-box ul {
        color: #374151;
        margin: 0;
        padding-left: 1.5rem;
    }
    .insight-box li {
        margin: 0.25rem 0;
    }
    .dark-mode-toggle {
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

   
    
    st.markdown('<h1 class="main-header">📊 Simulador de Pobreza 2024 - Análisis Avanzado</h1>', unsafe_allow_html=True)

    # Data from the images
    # Forecasts (2024)
    optimistic_poverty_2024 = 12.2
    restrictive_poverty_2024 = 15.1

    # Previous Year Data (2022)
    poverty_2022 = 16.0

    # Data for social deprivations (carencias sociales)
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
        'Valores 2022 (%)': [
            # POBREZA
            None, 16.0, 15.0, 1.1, 28.4, 9.6, 45.9,
            # PRIVACIÓN SOCIAL
            None, 44.5, 8.8,
            # INDICADORES DE CARENCIA SOCIAL
            None, 13.5, 22.8, 27.2, 3.2, 3.8, 11.7,
            # BIENESTAR ECONÓMICO
            None, 3.8, 25.7
        ],
        'Pronóstico optimista 2024 (%)': [
            # POBREZA
            None, 12.2, 11.5, 0.7, 34.6, 6.7, 46.6,
            # PRIVACIÓN SOCIAL
            None, 46.8, 6.1,
            # INDICADORES DE CARENCIA SOCIAL
            None, 13.7, 16.1, 27.2, 3.2, 3.8, 11.7,
            # BIENESTAR ECONÓMICO
            None, 2.8, 18.9
        ],
        'Pronóstico restrictivo 2024 (%)': [
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

    # Define variables by category for easy access
    carencias_variables = [
        'Rezago educativo',
        'Carencia por acceso a los servicios de salud',
        'Carencia por acceso a la seguridad social',
        'Carencia por calidad y espacios de la vivienda',
        'Carencia por acceso a los servicios básicos de la vivienda',
        'Carencia por acceso a la alimentación nutritiva y de calidad'
    ]

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
    tab1, tab2, tab3 = st.tabs([
        "📈 Dashboard Principal", 
        "🔍 Análisis Detallado", 
        "📊 Visualizaciones Avanzadas",
     
    ])

    with tab1:
        st.header("📊 Dashboard de Indicadores Clave")
        
        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Pobreza 2022</h3>
                <h2>{poverty_2022}%</h2>
                <p>Valor histórico</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            variation_optimistic = optimistic_poverty_2024 - poverty_2022
            trend_icon = "📉" if variation_optimistic < 0 else "📈"
            st.markdown(f"""
            <div class="metric-card">
                <h3>Pronóstico Optimista 2024</h3>
                <h2>{optimistic_poverty_2024}%</h2>
                <p>{trend_icon} {variation_optimistic:.1f} pp</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            variation_restrictive = restrictive_poverty_2024 - poverty_2022
            trend_icon = "📉" if variation_restrictive < 0 else "📈"
            st.markdown(f"""
            <div class="metric-card">
                <h3>Pronóstico Restrictivo 2024</h3>
                <h2>{restrictive_poverty_2024}%</h2>
                <p>{trend_icon} {variation_restrictive:.1f} pp</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            confidence_interval = restrictive_poverty_2024 - optimistic_poverty_2024
            st.markdown(f"""
            <div class="metric-card">
                <h3>Rango de Incertidumbre</h3>
                <h2>{confidence_interval:.1f} pp</h2>
                <p>Diferencia entre escenarios</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Main Chart
        st.subheader("📊 Evolución de la Pobreza: 2022 vs. Pronósticos 2024")
        
        # Prepare data for bar chart
        poverty_data_for_bar = {
            'Escenario': ['2022', '2024 (Optimista)', '2024 (Restrictivo)'],
            'Pobreza (%)': [poverty_2022, optimistic_poverty_2024, restrictive_poverty_2024]
        }
        df_poverty_bar = pd.DataFrame(poverty_data_for_bar)

        # Create simple bar chart (like the working original version)
        fig_poverty_bar = px.bar(
            df_poverty_bar,
            x='Escenario',
            y='Pobreza (%)',
            color='Escenario',
            color_discrete_map={
                '2022': '#6366f1',
                '2024 (Optimista)': '#10b981',
                '2024 (Restrictivo)': '#ef4444'
            },
            title='Evolución de la Pobreza en México',
            text='Pobreza (%)'
        )
        
        # Force x-axis to be categorical (simple fix that worked before)
        fig_poverty_bar.update_xaxes(type='category')
        
        # Update layout for better presentation
        fig_poverty_bar.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside'
        )
        
        # Simple layout without backgrounds
        fig_poverty_bar.update_layout(
            xaxis_title="Escenario",
            yaxis_title="Pobreza (%)",
            showlegend=True,
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_poverty_bar, use_container_width=True)

        
    with tab2:
        st.header("🔍 Análisis Detallado por Categorías")
        
        # Category selector
        selected_category = st.selectbox(
            "Selecciona una categoría para analizar:",
            ['POBREZA', 'PRIVACIÓN SOCIAL', 'INDICADORES DE CARENCIA SOCIAL', 'BIENESTAR ECONÓMICO']
        )
        
        # Filter data for selected category
        df_category = df_full[df_full['Categoría'] == selected_category].copy()
        
        # Remove None values for visualization
        df_category_clean = df_category.dropna(subset=['Valores 2022 (%)', 'Pronóstico optimista 2024 (%)', 'Pronóstico restrictivo 2024 (%)'])
        
        if not df_category_clean.empty:
            # Apply side-by-side visualization for all categories
            st.subheader("📊 Gráficos Separados por Indicador")
            st.write("Se muestran gráficos separados para cada indicador con escalas optimizadas para visualizar mejor las diferencias.")
            
            # Get all indicators for the selected category
            indicators = df_category_clean['Variable'].tolist()
            
            # Create columns based on number of indicators
            if len(indicators) == 1:
                # Single indicator - use full width
                col1, = st.columns(1)
                cols = [col1]
            elif len(indicators) == 2:
                # Two indicators - side by side
                col1, col2 = st.columns(2)
                cols = [col1, col2]
            elif len(indicators) == 3:
                # Three indicators - three columns
                col1, col2, col3 = st.columns(3)
                cols = [col1, col2, col3]
            elif len(indicators) == 4:
                # Four indicators - 2x2 grid
                col1, col2 = st.columns(2)
                col3, col4 = st.columns(2)
                cols = [col1, col2, col3, col4]
            elif len(indicators) == 5:
                # Five indicators - 3x2 grid
                col1, col2, col3 = st.columns(3)
                col4, col5 = st.columns(2)
                cols = [col1, col2, col3, col4, col5]
            elif len(indicators) == 6:
                # Six indicators - 3x2 grid
                col1, col2, col3 = st.columns(3)
                col4, col5, col6 = st.columns(3)
                cols = [col1, col2, col3, col4, col5, col6]
            else:
                # More than 6 indicators - use 3 columns
                cols = st.columns(3)
            
            # Create graphs for each indicator
            for i, indicator in enumerate(indicators):
                if i < len(cols):
                    with cols[i]:
                        indicator_data = df_category_clean[df_category_clean['Variable'] == indicator]
                        if not indicator_data.empty:
                            row = indicator_data.iloc[0]
                            
                            # Create grouped bar chart for indicator
                            fig = go.Figure()
                            
                            # Add bars for each scenario
                            fig.add_trace(go.Bar(
                                name='2022',
                                x=[indicator],
                                y=[row['Valores 2022 (%)']],
                                marker_color='#1f77b4'
                            ))
                            fig.add_trace(go.Bar(
                                name='2024 (Optimista)',
                                x=[indicator],
                                y=[row['Pronóstico optimista 2024 (%)']],
                                marker_color='#2ca02c'
                            ))
                            fig.add_trace(go.Bar(
                                name='2024 (Restrictivo)',
                                x=[indicator],
                                y=[row['Pronóstico restrictivo 2024 (%)']],
                                marker_color='#d62728'
                            ))
                            
                            # Calculate optimal y-axis range for better visualization
                            values = [row['Valores 2022 (%)'], row['Pronóstico optimista 2024 (%)'], row['Pronóstico restrictivo 2024 (%)']]
                            min_val = min(values)
                            max_val = max(values)
                            range_val = max_val - min_val
                            
                            # Set y-axis range with more padding (20%) to accommodate bars and text labels
                            y_min = max(0, min_val - range_val * 0.20)
                            y_max = max_val + range_val * 0.20
                            
                            fig.update_layout(
                                title=f'{indicator}',
                                xaxis_title="Indicador",
                                yaxis_title="Porcentaje (%)",
                                height=400,
                                showlegend=(i == 0),  # Only show legend for first graph
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                yaxis=dict(range=[y_min, y_max]),
                                title_x=0.5,
                                title_font_size=12,
                                barmode='group'
                            )
                            
                            # Add value labels on bars
                            fig.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Add analysis text
                            val_2022 = row['Valores 2022 (%)']
                            val_opt = row['Pronóstico optimista 2024 (%)']
                            val_res = row['Pronóstico restrictivo 2024 (%)']
                            
                            change_opt = val_opt - val_2022
                            change_res = val_res - val_2022
                            
                            st.markdown(f"""
                            <div class="insight-box">
                            <h4>📈 Análisis</h4>
                            <ul>
                                <li><strong>2022:</strong> {val_2022:.1f}%</li>
                                <li><strong>2024 (Optimista):</strong> {val_opt:.1f}% ({change_opt:+.1f} pp)</li>
                                <li><strong>2024 (Restrictivo):</strong> {val_res:.1f}% ({change_res:+.1f} pp)</li>
                            </ul>
                            </div>
                            """, unsafe_allow_html=True)
            
            # If there are more indicators than columns, create additional rows
            if len(indicators) > 6:
                remaining_indicators = indicators[6:]
                for i in range(0, len(remaining_indicators), 3):
                    batch = remaining_indicators[i:i+3]
                    if len(batch) == 3:
                        col1, col2, col3 = st.columns(3)
                        cols_batch = [col1, col2, col3]
                    elif len(batch) == 2:
                        col1, col2 = st.columns(2)
                        cols_batch = [col1, col2]
                    else:
                        col1, = st.columns(1)
                        cols_batch = [col1]
                    
                    for j, indicator in enumerate(batch):
                        if j < len(cols_batch):
                            with cols_batch[j]:
                                indicator_data = df_category_clean[df_category_clean['Variable'] == indicator]
                                if not indicator_data.empty:
                                    row = indicator_data.iloc[0]
                                    
                                    # Create grouped bar chart for indicator
                                    fig = go.Figure()
                                    
                                    # Add bars for each scenario
                                    fig.add_trace(go.Bar(
                                        name='2022',
                                        x=[indicator],
                                        y=[row['Valores 2022 (%)']],
                                        marker_color='#1f77b4'
                                    ))
                                    fig.add_trace(go.Bar(
                                        name='2024 (Optimista)',
                                        x=[indicator],
                                        y=[row['Pronóstico optimista 2024 (%)']],
                                        marker_color='#2ca02c'
                                    ))
                                    fig.add_trace(go.Bar(
                                        name='2024 (Restrictivo)',
                                        x=[indicator],
                                        y=[row['Pronóstico restrictivo 2024 (%)']],
                                        marker_color='#d62728'
                                    ))
                                    
                                    # Calculate optimal y-axis range for better visualization
                                    values = [row['Valores 2022 (%)'], row['Pronóstico optimista 2024 (%)'], row['Pronóstico restrictivo 2024 (%)']]
                                    min_val = min(values)
                                    max_val = max(values)
                                    range_val = max_val - min_val
                                    
                                    # Set y-axis range with more padding (20%) to accommodate bars and text labels
                                    y_min = max(0, min_val - range_val * 0.20)
                                    y_max = max_val + range_val * 0.20
                                    
                                    fig.update_layout(
                                        title=f'{indicator}',
                                        xaxis_title="Indicador",
                                        yaxis_title="Porcentaje (%)",
                                        height=400,
                                        showlegend=False,
                                        plot_bgcolor='rgba(0,0,0,0)',
                                        paper_bgcolor='rgba(0,0,0,0)',
                                        yaxis=dict(range=[y_min, y_max]),
                                        title_x=0.5,
                                        title_font_size=12,
                                        barmode='group'
                                    )
                                    
                                    # Add value labels on bars
                                    fig.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
                                    
                                    st.plotly_chart(fig, use_container_width=True)
                                    
                                    # Add analysis text
                                    val_2022 = row['Valores 2022 (%)']
                                    val_opt = row['Pronóstico optimista 2024 (%)']
                                    val_res = row['Pronóstico restrictivo 2024 (%)']
                                    
                                    change_opt = val_opt - val_2022
                                    change_res = val_res - val_2022
                                    
                                    st.markdown(f"""
                                    <div class="insight-box">
                                    <h4>📈 Análisis</h4>
                                    <ul>
                                        <li><strong>2022:</strong> {val_2022:.1f}%</li>
                                        <li><strong>2024 (Optimista):</strong> {val_opt:.1f}% ({change_opt:+.1f} pp)</li>
                                        <li><strong>2024 (Restrictivo):</strong> {val_res:.1f}% ({change_res:+.1f} pp)</li>
                                    </ul>
                                    </div>
                                    """, unsafe_allow_html=True)
                    
        # Show detailed table
        st.subheader("📋 Datos Detallados")
        st.dataframe(
            df_category[['Variable', 'Valores 2022 (%)', 'Pronóstico optimista 2024 (%)', 'Pronóstico restrictivo 2024 (%)']]
            .style.hide(axis="index")
            .format(precision=1)
        )

    with tab3:
        st.header("📊 Visualizaciones Avanzadas")
        
        # Radar Chart for Social Deprivations (Fixed)
        st.subheader("📊 Gráfico de Araña: Carencias Sociales")
        
        # Prepare data for radar chart
        df_carencias = df_full[df_full['Variable'].isin(carencias_variables)].set_index('Variable')
        
        # Create radar chart
        fig_radar = go.Figure() 
        
        # Add traces for each scenario
        fig_radar.add_trace(go.Scatterpolar(
            r=df_carencias['Valores 2022 (%)'].tolist(),
            theta=carencias_variables,
            fill='toself',
            name='2022',
            line_color='#6366f1',
            fillcolor='rgba(99, 102, 241, 0.3)'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=df_carencias['Pronóstico optimista 2024 (%)'].tolist(),
            theta=carencias_variables,
            fill='toself',
            name='2024 (Optimista)',
            line_color='#10b981',
            fillcolor='rgba(16, 185, 129, 0.3)'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=df_carencias['Pronóstico restrictivo 2024 (%)'].tolist(),
            theta=carencias_variables,
            fill='toself',
            name='2024 (Restrictivo)',
            line_color='#ef4444',
            fillcolor='rgba(239, 68, 68, 0.3)'
        ))
        
        # Simple layout without backgrounds
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, df_carencias[['Valores 2022 (%)', 'Pronóstico optimista 2024 (%)', 'Pronóstico restrictivo 2024 (%)']].max().max() * 1.1]
                )
            ),
            showlegend=True,
            title='Comparativa de Carencias Sociales: 2022 vs. Pronósticos 2024',
            height=600,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Heatmap
        st.subheader("🔥 Mapa de Calor: Variación por Indicador")
        
        # Calculate variations
        df_variations = df_full.copy()
        df_variations['Variación Optimista'] = df_variations['Pronóstico optimista 2024 (%)'] - df_variations['Valores 2022 (%)']
        df_variations['Variación Restrictiva'] = df_variations['Pronóstico restrictivo 2024 (%)'] - df_variations['Valores 2022 (%)']
        
        # Create heatmap data
        heatmap_data = df_variations.dropna(subset=['Variación Optimista', 'Variación Restrictiva'])[['Variable', 'Variación Optimista', 'Variación Restrictiva']].set_index('Variable')
        
        fig_heatmap = px.imshow(
            heatmap_data.T,
            title='Mapa de Calor: Variación 2024 vs 2022',
            color_continuous_scale='RdYlGn_r',
            aspect='auto'
        )
        
        fig_heatmap.update_layout(
            xaxis_title="Indicador",
            yaxis_title="Escenario",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)

    
if __name__ == "__main__":
    app() 