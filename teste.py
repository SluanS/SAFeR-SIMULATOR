import streamlit as st
import random
import time
import json # Adicionado para melhor visualização do JSON
import datetime


DESTINATIONS_DATA = {
    "Luan": ["000.222.333.44", "452", "chavePixLuan"], 
    "Henrique": ["555.323.333.44", "452", "chavePixHenrique"],
    "Pietra": ["111.222.333.44", "492", "chavePixPietra"],
    "Michel": ["333.888.333.44", "492", "chavePixMichel"],
    "João": ["111.444.333.44", "892", "chavePixJoao"]
}
estados_brasil = {
    "Acre": {"latitude": -9.97499, "longitude": -67.8243},            # Rio Branco
    "Alagoas": {"latitude": -9.66599, "longitude": -35.735},          # Maceió
    "Amapá": {"latitude": 0.034934, "longitude": -51.0694},           # Macapá
    "Amazonas": {"latitude": -3.11866, "longitude": -60.0212},        # Manaus
    "Bahia": {"latitude": -12.9718, "longitude": -38.5011},           # Salvador
    "Ceará": {"latitude": -3.71722, "longitude": -38.5431},           # Fortaleza
    "Distrito Federal": {"latitude": -15.7797, "longitude": -47.9297},# Brasília
    "Espírito Santo": {"latitude": -20.3155, "longitude": -40.3128},  # Vitória
    "Goiás": {"latitude": -16.6864, "longitude": -49.2643},           # Goiânia
    "Maranhão": {"latitude": -2.52972, "longitude": -44.3028},        # São Luís
    "Mato Grosso": {"latitude": -15.601, "longitude": -56.0974},      # Cuiabá
    "Mato Grosso do Sul": {"latitude": -20.4428, "longitude": -54.6464}, # Campo Grande
    "Minas Gerais": {"latitude": -19.9167, "longitude": -43.9345},    # Belo Horizonte
    "Pará": {"latitude": -1.45583, "longitude": -48.5039},            # Belém
    "Paraíba": {"latitude": -7.11509, "longitude": -34.8641},         # João Pessoa
    "Paraná": {"latitude": -25.4284, "longitude": -49.2733},          # Curitiba
    "Pernambuco": {"latitude": -8.04666, "longitude": -34.8771},      # Recife
    "Piauí": {"latitude": -5.08917, "longitude": -42.8019},           # Teresina
    "Rio de Janeiro": {"latitude": -22.9068, "longitude": -43.1729},  # Rio de Janeiro
    "Rio Grande do Norte": {"latitude": -5.79357, "longitude": -35.1986}, # Natal
    "Rio Grande do Sul": {"latitude": -30.0318, "longitude": -51.2065},   # Porto Alegre
    "Rondônia": {"latitude": -8.76194, "longitude": -63.9039},        # Porto Velho
    "Roraima": {"latitude": 2.81972, "longitude": -60.6733},          # Boa Vista
    "Santa Catarina": {"latitude": -27.5954, "longitude": -48.548},   # Florianópolis
    "São Paulo": {"latitude": -23.5505, "longitude": -46.6333},       # São Paulo
    "Sergipe": {"latitude": -10.9472, "longitude": -37.0731},         # Aracaju
    "Tocantins": {"latitude": -10.1675, "longitude": -48.3277}        # Palmas
}


def delta_button_method():
    """
    Cria o popover de metadados para configuração do Payload da API.
    Salva os dados no st.session_state["pix_meta"].
    """
    with st.popover("🛠"):
        st.subheader("PayLoad API")
        # Foi necessário usar chaves fixas ou o valor do input em si para evitar o erro de 'key must be unique'
        data = st.date_input(label="Data da transação", format="DD/MM/YYYY", value="2025-10-04", max_value="today",key="meta_data_hora",min_value=datetime.date(2000, 1, 1)).strftime("%m/%d/%Y")
        hora = st.time_input(label="Horário da transação:",value=datetime.time(12,0), key="meta_hora").strftime("%H:%M:%S")
        local = st.selectbox(label="Local da transação: ", options=estados_brasil.keys(),placeholder="Selecione o estado de origem",)
        st.subheader("Dispositivo")
        device_id = st.text_input("Device ID", value="1234567890", placeholder="ID único do dispositivo", key="meta_device_id")
        modelo_dispositivo = st.text_input("Modelo do dispositivo", value="iPhone 14", placeholder="Ex: Samsung S22", key="meta_modelo_dispositivo")
        data_cadastro = st.text_input("Data de cadastro", value="2023-01-15", placeholder="AAAA-MM-DD", key="meta_data_cadastro")

        st.subheader("Remetente")
        n_conta_remetente = st.text_input("Conta Remetente", value="12345-6", placeholder="Número da conta", key="meta_conta_remetente")
        n_agencia_remetente = st.text_input("Agência Remetente", value="1234", placeholder="Número da agência", key="meta_agencia_remetente")
        nome_remetente = st.text_input("Nome Remetente", value="João da Silva", placeholder="Nome completo", key="meta_nome_remetente")
        cpf_remetente = st.text_input("CPF Remetente", value="123.456.789-00", placeholder="Ex: 123.456.789-00", key="meta_cpf_remetente")
        data_criacao_conta = st.text_input("Data Criação Conta", value="2020-05-10", placeholder="AAAA-MM-DD", key="meta_data_criacao_conta")
        limite_noturno = st.text_input("Limite Noturno", value="5000.00", placeholder="Ex: 5000.00", key="meta_limite_noturno")

        st.subheader("Destinatário")
        n_conta_destinatario = st.text_input("Conta Destinatário", value="65432-1", placeholder="Número da conta", key="meta_conta_destinatario")
        n_agencia_destinatario = st.text_input("Agência Destinatário", value="4321", placeholder="Número da agência", key="meta_agencia_destinatario")
        ispb_destino = st.text_input("ISPB Destino", value="12345678", placeholder="Código ISPB do banco", key="meta_ispb_destino")

        # O botão Salvar Metadados não precisa de uma chave aleatória se for único dentro do popover
        if st.button("Salvar Metadados", key="salvar_metadados_btn"):
            st.session_state.clear()
            st.session_state["pix_meta"] = {
                "data_hora": data + "T" + hora,
                "latitude": estados_brasil[local]["latitude"],
                "longitude": estados_brasil[local]["longitude"],
                "device_id": device_id,
                "modelo_dispositivo": modelo_dispositivo,
                "data_cadastro": data_cadastro,
                "n_conta_remetente": n_conta_remetente,
                "n_agencia_remetente": n_agencia_remetente,
                "nome_remetente": nome_remetente,
                "cpf_remetente": cpf_remetente,
                "data_criacao_conta": data_criacao_conta,
                "limite_noturno": limite_noturno,
                "n_conta_destinatario": n_conta_destinatario,
                "n_agencia_destinatario": n_agencia_destinatario,
                "ispb_destino": ispb_destino
            }

            
            st.write(st.session_state)
            st.success("✅ Metadados salvos com sucesso!")


def create_value_container():
    """Cria o container para input do valor da transferência."""
    with st.container(border=True):
        # CHAVE FIXA para acesso: st.session_state["pix_value"]
        valor = st.number_input("Digite o valor da transferência:",
                        format="%.2f",
                        placeholder="0,00",
                        value=0.0,
                        min_value=0.0,
                        key="pix_value")
       


def create_destinations_container(destinations_data):
    """Cria o container para seleção do destinatário (chave Pix e contatos frequentes)."""
    with st.container(border=True):
        # CHAVE FIXA para acesso: st.session_state["pix_key_input"]
        chave_pix = st.text_input(label="Digite a chave pix: ", placeholder="CPF / CNPJ / TELEFONE / ALEATÓRIA", key="pix_key_input")

        # CHAVE FIXA para acesso: st.session_state["contact_pill"]
        contato = st.pills(label="Contatos frequentes: ", options=destinations_data.keys(), key="contact_pill")

        # Exibir dados do contato selecionado
        if contato:
            with st.expander(f"Dados do contato selecionado: {contato}"):
                st.success(f"""
                           Nº conta: {destinations_data[contato][0]}\n
                           Agencia: {destinations_data[contato][1]}\n
                           Chave:: {destinations_data[contato][2]}""")

        # CHAVE FIXA para acesso: st.session_state["description_input"]
        st.text_input("Descrição (Opcional)",
                      placeholder="Digite aqui sua descrição",
                      key="description_input")


@st.dialog(title="Processando pagamento", width="large")
def processing_dialog():
    """
    Exibe um diálogo de processamento com resultado aleatório (sucesso/falha).
    Acessa e exibe os valores dos inputs via st.session_state.
    """
    # --- Acesso aos valores dos Inputs ---
    # Usamos .get para retornar um valor padrão caso a chave ainda não exista na session_state
    valor_pix = st.session_state.get("pix_value", 0.0)
   # st.session_state["pix_meta"]["valor"] = st.session_state.get("pix_value",0.0)
    st.session_state["pix_meta"]["valor"] = st.session_state.get("pix_value", 0.0)
    chave_pix_digitada = st.session_state.get("pix_key_input", "Não preenchida")
    contato_selecionado = st.session_state.get("contact_pill")
    descricao = st.session_state.get("description_input", "Nenhuma")
    metadados = st.session_state.get("pix_meta", "Metadados não salvos")

    # Determina a chave de destino final
    chave_final = chave_pix_digitada
    if contato_selecionado:
        # Pega a chave real do contato selecionado do dicionário DESTINATIONS_DATA
        chave_final = DESTINATIONS_DATA[contato_selecionado][2]

    st.subheader("Dados da Transação Coletados")
    st.markdown(f"""
        - **Valor:** R$ {valor_pix:.2f}
        - **Destinatário:** {contato_selecionado if contato_selecionado else "Via Chave Digitada"}
        - **Chave de Destino (Para Envio):** `{chave_final}`
        - **Descrição:** {descricao}
    """)
    
    #st.subheader("Metadados (Payload API)")
    #if isinstance(metadados, dict):
    #    st.json(metadados)
    #else:
     #   st.warning("Metadados não configurados. Clique em 🛠 e 'Salvar Metadados'.")
    
    st.markdown("---")
    
    with st.spinner("Aguarde, estamos processando...", show_time=True):
        time.sleep(3)  # Simula o tempo de processamento

    numero = random.randint(1, 100)

    if numero % 2 == 0:
        st.success("Transação aceita com sucesso! 🎉")
        st.markdown(
            """
            <div style="text-align: center; font-size: 100px; color: green; margin-top: 20px;">
                ✔
            </div>
            <div style="text-align: center; font-size: 36px; color: green; font-weight: bold;">
                Transação Aceita!
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("Transação negada. ❌")
        st.markdown(
            """
            <div style="text-align: center; font-size: 100px; color: red; margin-top: 20px;">
                ❌
            </div>
            <div style="text-align: center; font-size: 36px; color: red; font-weight: bold;">
                Transação Negada!
            </div>
            """,
            unsafe_allow_html=True
        )
    st.write(st.session_state)

def construct_pix_page(destinations_data):
    """
    Função principal que constrói a página de Pix.
    """
    container = st.container(border=True)
    with container:
        # Botão de metadados
        delta_button_method()

        st.html("""
            <h1 style="text-align: center;">Pix</h1>
            """)

        # Containers de valor e destino
        create_value_container()
        create_destinations_container(destinations_data)

# --- Configuração e Execução Principal do Streamlit (main) ---

def main():
    """
    Ponto de entrada da aplicação Streamlit.
    """
    # Layout de colunas
    colL, colMain, colR = st.columns([2, 7, 2])

    with colMain:
        # Constrói a página
        construct_pix_page(DESTINATIONS_DATA)

        # Botão de Enviar Pix, chamando o diálogo de processamento
        # O on_click chama processing_dialog que acessa st.session_state
        st.button(
            label="Enviar Pix",
            type="primary",
            use_container_width=True,
            # Chave única para o botão Enviar Pix (não precisa de session state, mas sim de exclusividade)
            key="send_pix_button",
            on_click=processing_dialog
        )

if __name__ == "__main__":
    main()