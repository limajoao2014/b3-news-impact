import streamlit as st
import requests
import pandas as pd

# Configura a página para ocupar a tela toda
st.set_page_config(page_title="B3 News Impact", page_icon="📈", layout="wide")

st.title("📈 B3 News Impact")
st.markdown("Monitoramento de notícias e análise de sentimento com IA (Ollama).")

st.divider()

# Endereço da sua API (que está rodando no outro terminal)
API_URL = "http://127.0.0.1:8000/api/news"

try:
    # Bate na porta da API pedindo os dados
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        news_data = response.json()
        
        if news_data:
            # Transforma o JSON em uma tabela (DataFrame) do Pandas
            df = pd.DataFrame(news_data)
            
            # Formata a data para ficar legível
            df['published_at'] = pd.to_datetime(df['published_at']).dt.strftime('%d/%m/%Y %H:%M')
            
            # Reorganiza a ordem das colunas para ficar mais lógico
            df = df[['published_at', 'company_name', 'title', 'sentiment', 'impact_score', 'source']]
            
            # Renomeia as colunas para português na hora de exibir
            df.columns = ['Data', 'Empresa', 'Notícia', 'Sentimento', 'Impacto (1-5)', 'Fonte']
            
            # Exibe a tabela mágica interativa do Streamlit
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma notícia encontrada no momento.")
    else:
        st.error(f"Erro ao buscar dados na API. Código: {response.status_code}")

except Exception as e:
    st.error(f"❌ Não foi possível conectar à API. Ela está rodando no outro terminal? Erro: {e}")
# ... (seu código das notícias continua lá em cima)

st.divider()

# --- NOVA SEÇÃO: GRÁFICO DE PREÇOS ---
st.subheader("📈 Histórico de Preços das Ações")

# DICA: Coloquei ?limit=1000 na URL para ignorar o limite de 50 que você fez na API
# Assim o gráfico consegue puxar um histórico bem maior de pontos!
PRICES_API_URL = "http://127.0.0.1:8000/api/prices/?limit=1000"

try:
    response_prices = requests.get(PRICES_API_URL)
    
    if response_prices.status_code == 200:
        prices_data = response_prices.json()
        
        if prices_data:
            # 1. Transforma o JSON em DataFrame Pandas
            df_prices = pd.DataFrame(prices_data)
            
            # 2. Converte a coluna 'date' para o formato de tempo real
            # df_prices['date'] = pd.to_datetime(df_prices['date'])
            df_prices['date'] = pd.to_datetime(df_prices['date'], format='ISO8601')
            
            # 3. Filtro interativo (Multiselect)
            # Pega todos os tickers únicos (ex: PETR4, VALE3) que vieram do banco
            tickers_disponiveis = df_prices['ticker'].unique()
            
            empresas_selecionadas = st.multiselect(
                "Filtre as ações que deseja visualizar:",
                options=tickers_disponiveis,
                default=tickers_disponiveis[:3] if len(tickers_disponiveis) > 0 else None # Seleciona as 3 primeiras por padrão
            )
            
            if empresas_selecionadas:
                # 4. Filtra a tabela só com os tickers que você escolheu na tela
                df_filtrado = df_prices[df_prices['ticker'].isin(empresas_selecionadas)]
                
                # 5. O truque de Mestre (Pivot Table):
                # Eixo X (Index) = Data
                # Colunas = Tickers (PETR4, VALE3, etc)
                # Valores = Preço
                df_grafico = df_filtrado.pivot_table(
                    index='date',
                    columns='ticker',
                    values='price'
                )
                # --- A LINHA MÁGICA QUE ARRUMA AS DATAS ---
                df_grafico.index = df_grafico.index.strftime('%d/%m/%Y')
                
                # 6. Plota o gráfico!
                st.line_chart(df_grafico)
            else:
                st.warning("⚠️ Selecione pelo menos uma empresa no filtro acima para ver o gráfico.")
        else:
            st.info("Nenhum histórico de preço encontrado. Vá no terminal e rode o script collect_prices.py algumas vezes!")
    else:
        st.error(f"Erro ao buscar preços na API. Código: {response_prices.status_code}")
        
except Exception as e:
    st.error(f"Erro ao carregar a seção de gráficos: {e}")