import streamlit as st
import random
import time
import json # Adicionado para melhor visualização do JSON
import datetime
from Client import SaferRequets



bancos_ispb = {
    "Agibank": "01330382",
    "Banco do Brasil": "00000000",
    "Banco da Amazônia": "00000208",
    "Banco do Nordeste": "00000236",
    "Banco Bradesco": "60746948",
    "Itaú Unibanco": "60701190",
    "Santander": "90400888",
    "Caixa Econômica Federal": "00360305",
    "Banco Safra": "58160789",
    "Banco BTG Pactual": "30306294",
    "Banco Inter": "00416968",
    "Nubank": "18236120",
    "Banco Original": "92894922",
    "Banco Pan": "62331228",
    "Banco C6": "31872495",
    "Banco Modal": "30723886",
    "Banco Votorantim (BV)": "59588111",
    "Banco Daycoval": "62232889",
    "Banco Sofisa": "60889128",
    "Banco XP": "33264668",
    "Banco BS2": "07192329",
    "Banco Topázio": "07117473"
}




@st.cache_data(ttl=500)
def loadClients():
    ContasCliente = SaferRequets.getAllAccounts()
    clientes = SaferRequets.formatarClientes(ContasCliente)
    return clientes

clientes = loadClients()

DESTINATIONS_DATA = {
    "Luan": {"conta": "000.222.333.44", "agencia": "452", "pix_key": "chavePixLuan", "ispb_destino":bancos_ispb["Agibank"],"cpf":"55845"}, 
    "Henrique": {"conta": "555.323.333.44", "agencia": "452", "pix_key": "chavePixHenrique","ispb_destino":bancos_ispb["Nubank"],"cpf":"55845"},
    "Pietra": {"conta": "111.222.333.44", "agencia": "492", "pix_key": "chavePixPietra","ispb_destino":bancos_ispb["Santander"],"cpf":"55845"},
    "Michel": {"conta": "333.888.333.44", "agencia": "492", "pix_key": "chavePixMichel","ispb_destino":bancos_ispb["Itaú Unibanco"],"cpf":"55845"},
    "João": {"conta": "111.444.333.44", "agencia": "892", "pix_key": "chavePixJoao","ispb_destino":bancos_ispb["Banco XP"],"cpf":"12345678901"}
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


if "pix_meta" not in st.session_state:
    st.session_state["pix_meta"] = {"meioPagamento": "pix"}

def delta_button_method():
    """
    Cria o popover de metadados para configuração do Payload da API.
    Salva os dados no st.session_state["pix_meta"].
    """
    with st.popover("🛠"):
        st.subheader("PayLoad API")
        # Foi necessário usar chaves fixas ou o valor do input em si para evitar o erro de 'key must be unique'
        st.subheader("Dispositivo")
        dispositivo = st.selectbox("Modelo do dispositivo", options=["MOBILE","DESKTOP","AUTO_ATENDIMENTO"], key="meta_modelo_dispositivo")
        
        st.subheader("Remetente")
        cliente = st.selectbox("Cliente remetente",key="cliente_remetente",options=clientes.keys())
        with st.expander(f"Dados de {cliente}"):
                st.success(f"""
                           Nº conta: {clientes[cliente]["numConta"]}\n
                           Agencia: {clientes[cliente]["numAgencia"]}\n
                           Chave: {clientes[cliente]["ispb"]}""")
        st.subheader("Informações gerais")
        data = st.date_input(label="Data da transação", format="DD/MM/YYYY", value="2025-10-04", max_value="today",key="meta_data_hora",min_value=datetime.date(2000, 1, 1)).strftime("%Y-%m-%d")
        hora = st.time_input(label="Horário da transação:",value=datetime.time(12,0), key="meta_hora").strftime("%H:%M:%S")
        local = st.selectbox(label="Local da transação: ", options=estados_brasil.keys(),placeholder="Selecione o estado de origem",)

        #st.subheader("Destinatário")
        #destinatario = st.selectbox(label="Digite a chave pix: ", options=DESTINATIONS_DATA.keys(), key="destination_key")

        # O botão Salvar Metadados não precisa de uma chave aleatória se for único dentro do popover
        if st.button("Salvar Metadados", key="salvar_metadados_btn"):
            st.session_state["pix_meta"] = {
                "dataHoraOperacao": data + "T" + hora,
                #Longitude - latitude
                "local": [estados_brasil[local]["longitude"],estados_brasil[local]["latitude"]],
                "dispositivo": dispositivo,
                "numContaOrigem": clientes[cliente]["numConta"],
                "numAgenciaOrigem": clientes[cliente]["numAgencia"],
                "ispbOrigem": clientes[cliente]["ispb"],
                "cpfOrigem": clientes[cliente]["cpf"],
                #"numContaDestino": DESTINATIONS_DATA[destinatario]["conta"],
                #"numAgenciaDestino": DESTINATIONS_DATA[destinatario]["agencia"],
                #"ispbDestino": DESTINATIONS_DATA[destinatario]["ispb_destino"],
                #"cpfCnpjDestino": DESTINATIONS_DATA[destinatario]["cpf"],
                "meioPagamento": "PIX",
                "conta" : clientes[cliente]["numConta"]
            
            }

            
            st.write(st.session_state["pix_meta"])
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
        chaves = []
        for contato in destinations_data.values():
            chaves.append(contato["pix_key"])
        chave_pix = st.text_input(label="Digite a chave pix: ", key="pix_key_input",
                                  placeholder="Ex: email, telefone, cpf ou chave aleatória",help="Você pode digitar uma chave Pix ou selecionar um contato frequente abaixo.")

        # CHAVE FIXA para acesso: st.session_state["contact_pill"]
        contato = st.pills(label="Contatos frequentes: ", options=destinations_data.keys(), key="contact_pill")

        # Exibir dados do contato selecionado
        if contato:
            st.session_state["pix_meta"]["numContaDestino"] = destinations_data[contato]["conta"]
            st.session_state["pix_meta"]["numAgenciaDestino"] = destinations_data[contato]["agencia"]
            st.session_state["pix_meta"]["ispbDestino"] = destinations_data[contato]["ispb_destino"]
            st.session_state["pix_meta"]["cpfCnpjDestino"] = destinations_data[contato]["cpf"]
            with st.expander(f"Dados do contato selecionado: {contato}"):
                st.success(f"""
                           Nº conta: {destinations_data[contato]["conta"]}\n
                           Agencia: {destinations_data[contato]["agencia"]}\n
                           Chave: {destinations_data[contato]["pix_key"]}""")

        # CHAVE FIXA para acesso: st.session_state["description_input"]
        st.text_input("Descrição (Opcional)",
                      placeholder="Digite aqui sua descrição",
                      key="description_input")


@st.dialog(title="Processando pagamento", width="large")
def processing_dialog():
    if st.session_state.get("pix_value") > 0:
        st.session_state["pix_meta"]["valor"] = st.session_state.get("pix_value", 0.0)
        valor_pix = st.session_state.get("pix_value", 0.0)
        payload = st.session_state["pix_meta"]
        response = SaferRequets.sendRequest(payload)
        # st.session_state["pix_meta"]["valor"] = st.session_state.get("pix_value",0.0)
        
        chave_pix_digitada = st.session_state.get("pix_key_input", "Não preenchida")
        contato_selecionado = st.session_state.get("contact_pill")
        descricao = st.session_state.get("description_input", "Nenhuma")
        metadados = st.session_state.get("pix_meta", "Metadados não salvos")

        # Determina a chave de destino final
        chave_final = chave_pix_digitada
        if contato_selecionado:
            # Pega a chave real do contato selecionado do dicionário DESTINATIONS_DATA
            chave_final = DESTINATIONS_DATA[contato_selecionado]["pix_key"]

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

        if response["scoreTransacao"] < 50:
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
        st.write(st.session_state["pix_meta"])
    else:
        st.warning("Digite o valor da transação!")

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