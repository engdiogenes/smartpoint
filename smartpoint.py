import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Smartpoint", layout="wide")

# Sidebar com informações da aplicação
st.sidebar.title("📡 Smartpoint")
st.sidebar.markdown("""
**Smartpoint** é uma aplicação para rastreamento e análise de deslocamento de operadores em linhas de produção industriais.

**Tecnologia Utilizada:**
- Localização em tempo real (UWB)
- IOT com Esp32
- Visualização com Streamlit e Plotly
- Coleta e armazenamento dos dados

**Benefícios Inovadores:**
- Otimização de layout de estações de trabalho
- Análise de ergonomia e eficiência
- Suporte à engenharia de processos

**Desenvolvido por:**  
Eng Diógenes Oliveira
""")

# Tabs da aplicação
tab1, tab2 = st.tabs(["🎥 Animação de Rastreamento", "📊 Dashboard Analítico"])

# Simulação de trilha do operador
np.random.seed(42)
steps = 100
x = np.cumsum(np.random.normal(0, 0.3, steps)) + 5
y = np.cumsum(np.random.normal(0, 0.2, steps)) + 3
x = np.clip(x, 0, 10)
y = np.clip(y, 0, 6)
path = np.column_stack((x, y))
df = pd.DataFrame(path, columns=["x", "y"])
df["step"] = df.index
df["dist"] = np.sqrt(np.sum(np.diff(path, axis=0, prepend=path[0:1])**2, axis=1))
df["dist_acumulada"] = df["dist"].cumsum()
with tab1:
    st.header("🎥 Animação de Rastreamento do Operador")

    # Definição dos vértices do quadrilátero (antenas)
    antennas = np.array([
        [0, 0],
        [10, 0],
        [10, 6],
        [0, 6]
    ])

    # Gráfico 1: Trilha do operador
    frames1 = []
    for i in range(1, len(path)):
        frames1.append(go.Frame(
            data=[
                go.Scatter(x=path[:i, 0], y=path[:i, 1], mode='lines+markers', name='Trilha'),
                go.Scatter(x=antennas[:, 0], y=antennas[:, 1], mode='markers+text',
                           marker=dict(color='red', size=10),
                           text=[f"Antena {j+1}" for j in range(4)],
                           textposition="top center",
                           name='Antenas')
            ],
            name=str(i)
        ))

    fig1 = go.Figure(
        data=[
            go.Scatter(x=[], y=[], mode='lines+markers', name='Trilha'),
            go.Scatter(x=antennas[:, 0], y=antennas[:, 1], mode='markers+text',
                       marker=dict(color='red', size=10),
                       text=[f"Antena {j+1}" for j in range(4)],
                       textposition="top center",
                       name='Antenas')
        ],
        layout=go.Layout(
            title="Vista Superior da Estação de Trabalho - Trilha do Operador",
            xaxis=dict(range=[-1, 11], title="Metros (x)"),
            yaxis=dict(range=[-1, 7], title="Metros (y)"),
            updatemenus=[dict(type="buttons",
                              buttons=[dict(label="▶️ Iniciar",
                                            method="animate",
                                            args=[None, {"frame": {"duration": 100, "redraw": True},
                                                         "fromcurrent": True}])])]
        ),
        frames=frames1
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: Linhas até antenas + trilha acumulada
    frames2 = []
    for i in range(1, len(path)):
        lines = []
        lines.append(go.Scatter(x=path[:i+1, 0], y=path[:i+1, 1], mode='lines', line=dict(color='blue'), name='Trilha'))
        for ant in antennas:
            lines.append(go.Scatter(x=[path[i, 0], ant[0]], y=[path[i, 1], ant[1]],
                                    mode='lines', line=dict(dash='dot'), showlegend=False))
        lines.append(go.Scatter(x=[path[i, 0]], y=[path[i, 1]], mode='markers', marker=dict(size=8), name='Operador'))
        lines.append(go.Scatter(x=antennas[:, 0], y=antennas[:, 1], mode='markers+text',
                                marker=dict(color='red', size=10),
                                text=[f"Antena {j+1}" for j in range(4)],
                                textposition="top center",
                                name='Antenas'))
        frames2.append(go.Frame(data=lines, name=str(i)))

    fig2 = go.Figure(
        data=[
            go.Scatter(x=[], y=[], mode='lines', name='Trilha'),
            go.Scatter(x=[], y=[], mode='lines', showlegend=False),
            go.Scatter(x=[], y=[], mode='markers', name='Operador'),
            go.Scatter(x=antennas[:, 0], y=antennas[:, 1], mode='markers+text',
                       marker=dict(color='red', size=10),
                       text=[f"Antena {j+1}" for j in range(4)],
                       textposition="top center",
                       name='Antenas')
        ],
        layout=go.Layout(
            title="Linhas do Operador até as Antenas + Trilha",
            xaxis=dict(range=[-1, 11], title="Metros (x)"),
            yaxis=dict(range=[-1, 7], title="Metros (y)"),
            updatemenus=[dict(type="buttons",
                              buttons=[dict(label="▶️ Iniciar",
                                            method="animate",
                                            args=[None, {"frame": {"duration": 100, "redraw": True},
                                                         "fromcurrent": True}])])]
        ),
        frames=frames2
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3: Pontos + ondas radiais UWB
    import streamlit as st
    import streamlit.components.v1 as components

    # Carrega o conteúdo do HTML
    with open("ondas_radiais_carro_area_montagem.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    # Substitui o gráfico 3 por este HTML
    st.markdown("### Animação com Antenas e Área de Montagem - UWB ")
    components.html(html_content, height=550, scrolling=False)

    st.metric(label="📏 Distância Total Percorrida", value=f"{df['dist_acumulada'].iloc[-1]:.2f} metros")
    with tab2:
        st.header("📊 Dashboard Analítico")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📍 Mapa de Calor da Densidade de Presença")
            fig_heat = px.density_heatmap(df, x="x", y="y", nbinsx=20, nbinsy=12, color_continuous_scale="Viridis")
            st.plotly_chart(fig_heat, use_container_width=True)

        with col2:
            st.subheader("🧭 Trilha Completa do Operador")
            fig_path = px.line(df, x="x", y="y", markers=True)
            fig_path.update_layout(xaxis_title="x (m)", yaxis_title="y (m)", height=400)
            st.plotly_chart(fig_path, use_container_width=True)

        st.subheader("📈 Histograma de Distâncias Entre Pontos Consecutivos")
        fig_hist = px.histogram(df, x="dist", nbins=20, title="Distribuição dos Deslocamentos")
        fig_hist.update_layout(xaxis_title="Distância (m)", yaxis_title="Frequência")
        st.plotly_chart(fig_hist, use_container_width=True)

        st.subheader("📏 Distância Acumulada ao Longo do Tempo")
        fig_line = px.line(df, x="step", y="dist_acumulada", markers=True, title="Distância Total Percorrida")
        fig_line.update_layout(xaxis_title="Etapa", yaxis_title="Distância Acumulada (m)")
        st.plotly_chart(fig_line, use_container_width=True)

        st.subheader("📡 Radar de Métricas de Desempenho")
        metricas = {
            "Cobertura da Área": len(df.drop_duplicates(subset=["x", "y"])) / steps,
            "Eficiência de Trajeto": df["dist_acumulada"].iloc[-1] / (np.linalg.norm(path[-1] - path[0]) + 1e-6),
            "Repetição de Movimento": 1 - len(df.drop_duplicates(subset=["x", "y"])) / steps,
            "Deslocamento Médio": df["dist"].mean() / 2,
            "Exploração do Espaço": len(np.unique(np.round(df["x"]))) * len(np.unique(np.round(df["y"]))) / 60
        }
        radar_df = pd.DataFrame(dict(
            Métrica=list(metricas.keys()),
            Valor=list(metricas.values())
        ))
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_df["Valor"],
            theta=radar_df["Métrica"],
            fill='toself',
            name='Desempenho'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=False)
        st.plotly_chart(fig_radar, use_container_width=True)

        st.subheader("🧠 Diagnóstico e Sugestões de Melhoria")
        diagnostico = []

        if metricas["Cobertura da Área"] < 0.5:
            diagnostico.append(
                "- O operador está se concentrando em uma área pequena. Avaliar redistribuição de ferramentas.")
        if metricas["Eficiência de Trajeto"] < 2:
            diagnostico.append("- O trajeto do operador é pouco eficiente. Considerar reorganização do layout.")
        if metricas["Repetição de Movimento"] > 0.5:
            diagnostico.append("- Há muitos movimentos repetitivos. Avaliar ergonomia e fluxo de trabalho.")
        if metricas["Deslocamento Médio"] > 0.2:
            diagnostico.append("- Deslocamentos médios elevados. Verificar necessidade de movimentação frequente.")
        if metricas["Exploração do Espaço"] < 0.3:
            diagnostico.append("- Baixa exploração do espaço. Pode indicar layout subutilizado.")

        if not diagnostico:
            st.success("✅ Nenhuma anomalia detectada. O padrão de deslocamento parece eficiente.")
        else:
            for item in diagnostico:
                st.warning(item)


