import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Configuração da página ---
st.set_page_config(page_title="Calculadora Profissional de Juros Compostos", layout="centered")
st.title("💰 Calculadora Profissional de Juros Compostos")

# --- Histórico ---
if "historico" not in st.session_state:
    st.session_state.historico = []

# --- Entradas do usuário ---
col1, col2 = st.columns(2)
with col1:
    P = st.number_input("Valor Inicial (R$)", min_value=0.0, value=1000.0, step=100.0, format="%.2f")
    aporte_valor = st.number_input("Aporte Mensal (R$)", min_value=0.0, value=200.0, step=50.0, format="%.2f")
with col2:
    r_anual = st.number_input("Taxa de Juros (% ao ano)", min_value=0.0, value=10.0, step=0.1, format="%.2f") / 100
    n = st.number_input("Período (anos)", min_value=1, value=5, step=1)

# --- Botão Calcular ---
if st.button("Calcular", use_container_width=True):
    try:
        # Taxa efetiva mensal
        i_mensal = (1 + r_anual) ** (1/12) - 1

        total = P
        total_aporte = P
        total_juros = 0
        dados = []
        valores_anuais = []

        for mes in range(1, n*12 + 1):
            juros_mes = total * i_mensal
            total += juros_mes
            total += aporte_valor
            total_aporte += aporte_valor
            total_juros += juros_mes

            dados.append([mes, juros_mes, total_aporte, total_juros, total])

            if mes % 12 == 0:
                valores_anuais.append(total)

        # Salva no histórico
        st.session_state.historico.append(
            f"P={P:.2f}, Aporte={aporte_valor:.2f}, r={r_anual*100:.2f}%, n={n} anos => A={valores_anuais[-1]:,.2f}"
        )

        # Exibe resultado final
        st.subheader(f"Montante Final: R$ {valores_anuais[-1]:,.2f}")

        # Tabela detalhada
        df = pd.DataFrame(dados, columns=[
            "Mês", "Juros (R$)", "Total Investido (R$)", "Total Juros (R$)", "Total Acumulado (R$)"
        ])
        st.dataframe(df.style.format("{:,.2f}"), use_container_width=True)

        # Gráfico de crescimento anual
        fig, ax = plt.subplots(figsize=(7, 4))
        anos = list(range(1, n+1))
        ax.bar(anos, valores_anuais, color='#1f77b4', alpha=0.7)
        ax.plot(anos, valores_anuais, marker='o', color='#ff7f0e', linewidth=2, label='Montante')
        ax.set_title("Crescimento do Investimento", fontsize=14)
        ax.set_xlabel("Ano", fontsize=12)
        ax.set_ylabel("Montante (R$)", fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Erro ao calcular: {e}")

# --- Histórico de cálculos ---
if st.session_state.historico:
    st.markdown("### 📜 Histórico de Cálculos")
    for item in reversed(st.session_state.historico[-10:]):  # Últimos 10
        st.write(item)
