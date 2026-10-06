from groq import Groq
import streamlit as st

st.set_page_config(
    page_title="CryptoCIn Tutor", page_icon="🛡️", layout="centered"
)

st.title("🛡️ CryptoCIn Tutor (CIn/UFPE)")
st.markdown(
    "O seu assistente virtual oficial para a disciplina de Criptografia"
    " do CIn/UFPE!"
)

# Gestão segura da Chave de API da Groq
api_key = None
try:
  api_key = st.secrets["GROQ_API_KEY"]
except Exception:
  pass

if not api_key:
  api_key = st.text_input("Cole a sua GROQ_API_KEY aqui:", type="password")

if api_key:
  # Base de Conhecimento ampla baseada na grade da disciplina
  base_conhecimento = """
    # Ementa e Base de Conhecimento - Criptografia (CIn/UFPE)

    ## Unidade 1: Introdução e Criptografia Clássica
    - Histórico, conceitos básicos e objetivos da segurança da informação (Confidencialidade, Integridade, Disponibilidade).
    - Cifras clássicas (Cifra de César, Vigenère, Cifra de Substituição e Transposição) e criptoanálise básica.
    - Princípios de Kerckhoffs e noções iniciais de segurança teórica vs. computacional.

    ## Unidade 2: Criptografia Simétrica (Chave Secreta)
    - Cifras de Fluxo (Stream Ciphers) e OTP (One-Time Pad).
    - Cifras de Bloco (Block Ciphers): Estrutura de Feistel, DES e AES.
    - Modos de Operação de Cifras de Bloco (ECB, CBC, CFB, OFB, CTR, GCM) e ataques por CPA/CCA.
    - Funções de Hash Criptográficas e integridade (SHA-256, SHA-3, resistência a colisões).
    - Códigos de Autenticação de Mensagem (MACs, HMAC).

    ## Unidade 3: Criptografia Assimétrica (Chave Pública)
    - Conceito de funções de mão única com alçapão (Trapdoor One-Way Functions).
    - Criptossistema RSA (geração de chaves, cifragem, decifragem e segurança).
    - Troca de Chaves Diffie-Hellman e o problema do logaritmo discreto.
    - Criptografia de Curvas Elípticas (ECC).
    - Assinaturas Digitais e Infraestrutura de Chaves Públicas (PKI / Certificados Digitais).

    ## Unidade 4: Protocolos Criptográficos e Tópicos Avançados
    - Acordo de chaves, autenticação de entidades e protocolos de canal seguro (ex: SSL/TLS, IPsec).
    - Conceitos básicos de Provas de Conhecimento Zero (Zero-Knowledge Proofs).
    - Noções de Criptografia Pós-Quântica e aplicações modernas.
    """

  # System Prompt focado na disciplina do CIn/UFPE como um todo
  system_instruction = f"""
    Você é o CryptoCIn Tutor, um assistente virtual acadêmico e monitor especialista da disciplina de Criptografia do Centro de Informática da UFPE (CIn/UFPE).

    Sua missão principal é ajudar os alunos a resolverem e entenderem dúvidas sobre questões, exercícios, listas, provas, teoremas e conceitos da ementa oficial da disciplina.

    DIRETRIZES DE ATUAÇÃO PARA O TIRA-DÚVIDAS:
    1. Quando o aluno trouxer uma dúvida teórica, um exercício de lista ou uma questão de prova, explique o conceito passo a passo de forma didática, clara e analítica.
    2. Utilize a ementa e os tópicos da grade curricular de Criptografia do CIn/UFPE como referência principal para guiar as respostas.
    3. Guie o raciocínio mostrando a intuição lógica e prática por trás da resposta, contextualizando com segurança da informação.
    4. Escreva todas as explicações e fórmulas matemáticas usando texto normal, português claro e símbolos legíveis (como Pr[], XOR, somatório), evitando completamente o uso de formatação LaTeX ($...$ ou blocos de equação).
    5. Mantenha um tom encorajador, acadêmico, parceiro e colaborativo, típicos de um monitor do CIn.

    --- EMENTA / BASE DE CONHECIMENTO ---
    {base_conhecimento}
    -------------------------------------
    """

  # Inicializa o histórico de mensagens
  if "messages" not in st.session_state:
    st.session_state.messages = []

  # Exibir mensagens anteriores na interface
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  # Caixa de entrada de texto do chat web
  if user_query := st.chat_input(
      "Digite a sua dúvida de criptografia ou cole uma questão..."
  ):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
      st.markdown(user_query)

    with st.chat_message("assistant"):
      with st.spinner("O CryptoCIn Tutor está a analisar a sua dúvida..."):
        try:
          client = Groq(api_key=api_key)

          messages_payload = [{"role": "system", "content": system_instruction}]
          for msg in st.session_state.messages:
            messages_payload.append(
                {"role": msg["role"], "content": msg["content"]}
            )

          response = client.chat.completions.create(
              model="openai/gpt-oss-20b",
              messages=messages_payload,
              temperature=0.3,
          )

          bot_reply = response.choices[0].message.content
          st.markdown(bot_reply)

          st.session_state.messages.append(
              {"role": "assistant", "content": bot_reply}
          )
        except Exception as e:
          st.error(f"Ocorreu um erro ao gerar a resposta: {e}")
else:
  st.info(
      "Por favor, insira a sua chave da API da Groq para iniciar o assistente."
  )
