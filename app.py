from groq import Groq
import streamlit as st

st.set_page_config(
    page_title="CryptoCIn Tutor", page_icon="🛡️️", layout="centered"
)

st.title("🛡️ CryptoCIn Tutor (CIn/UFPE)")
st.markdown(
    "O seu assistente virtual para ajudar na disciplina de Criptografia,"
    " baseado no livro de **Dan Boneh & Victor Shoup**."
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
  # Base de Conhecimento
  base_conhecimento = """
    # Base de Conhecimento Tira-Dúvidas - CryptoCIn Tutor (CIn/UFPE)
    # Referência: 'A Graduate Course in Applied Cryptography' (Dan Boneh & Victor Shoup)

    ## Módulo 1: Fundamentos, Sigilo Perfeito e Segurança Computacional
    - Princípios e Modelos de Adversário e Reduções matemáticas.
    - Sigilo Perfeito (Shannon) & One-Time Pad (OTP).
    - Segurança Computacional e Geradores Pseudoaleatórios (PRG).

    ## Módulo 2: Cifras de Fluxo, CPA e Encriptação Múltipla
    - Segurança CPA (Chosen-Plaintext Attack) e uso de nonces/IV.
    - Modos de Operação de Cifras de Bloco (CBC, CTR, GCM).

    ## Módulo 3: Integridade, MACs e Funções de Hash
    - MACs (Message Authentication Codes) e Funções de Hash (Resistência à Colisão).

    ## Módulo 4: Criptografia Assimétrica, Diffie-Hellman e Assinaturas
    - Funções Trapdoor, RSA, Diffie-Hellman e Curvas Elípticas (ECC).

    ## Módulo 5: Provas de Conhecimento Zero (ZKP)
    - Completude, Solidez e Propriedade Zero-Knowledge.
    """

  # System Prompt sem LaTeX
  system_instruction = f"""
    Você é o CryptoCIn Tutor, um assistente virtual acadêmico e monitor especialista da disciplina de Criptografia do CIn/UFPE, baseando-se estritamente no livro 'A Graduate Course in Applied Cryptography' (Dan Boneh & Victor Shoup).

    Sua missão principal é ajudar os alunos a resolverem e entenderem dúvidas sobre questões, exercícios, teoremas e conceitos específicos da disciplina. 

    DIRETRIZES DE ATUAÇÃO PARA O TIRA-DÚVIDAS:
    1. Quando o aluno trouxer uma dúvida teórica ou sobre uma questão, explique o conceito passo a passo de forma didática, clara e analítica.
    2. Utilize os conceitos formais e matemáticos presentes na base de conhecimento.
    3. Guie o raciocínio mostrando a intuição por trás da resposta.
    4. Escreva todas as explicações e fórmulas matemáticas usando texto normal, português claro e símbolos legíveis (como Pr[], XOR, somatório), evitando completamente o uso de formatação LaTeX ($...$ ou blocos de equação).
    5. Mantenha um tom encorajador, acadêmico e colaborativo.

    --- BASE DE CONHECIMENTO ---
    {base_conhecimento}
    ----------------------------
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

          # Monta as mensagens incluindo a instrução de sistema e todo o histórico
          messages_payload = [{"role": "system", "content": system_instruction}]
          for msg in st.session_state.messages:
            messages_payload.append(
                {"role": msg["role"], "content": msg["content"]}
            )

          response = client.chat.completions.create(
              model="llama-3.1-8b-instant",
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
