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
  base_conhecimento = """
    # Ementa e Base de Conhecimento - Criptografia (CIn/UFPE)

    ## Unidade 1: Introdução e Criptografia Clássica
    - Histórico, conceitos básicos e objetivos da segurança da informação.
    - Cifras clássicas e criptoanálise básica.
    - Princípios de Kerckhoffs e noções de segurança teórica vs. computacional.

    ## Unidade 2: Criptografia Simétrica (Chave Secreta)
    - Cifras de Fluxo (Stream Ciphers) e OTP (One-Time Pad) - Ex: $c = m \oplus k$.
    - Cifras de Bloco (Block Ciphers): Estrutura de Feistel, DES e AES.
    - Modos de Operação de Cifras de Bloco (CBC, CTR, GCM) e malha de segurança.
    - Funções de Hash Criptográficas e MACs (HMAC).

    ## Unidade 3: Criptografia Assimétrica (Chave Pública)
    - Funções de mão única com alçapão (Trapdoor One-Way Functions).
    - Criptossistema RSA e Troca de Chaves Diffie-Hellman.
    - Assinaturas Digitais e Curvas Elípticas (ECC).
    """

  # Prompt ultra-rigoroso para proibir blocos LaTeX complexos e exigir formato limpo
  system_instruction = f"""
    Você é o CryptoCIn Tutor, um assistente virtual acadêmico e monitor especialista da disciplina de Criptografia do Centro de Informática da UFPE (CIn/UFPE).

    Sua missão principal é ajudar os alunos a resolverem e entenderem dúvidas sobre questões, exercícios, listas, provas e conceitos da ementa da disciplina.

    REGRAS ABSOLUTAS DE FORMATAÇÃO:
    1. PROIBIDO usar blocos LaTeX avançados como \\begin{{aligned}}, \\qquad, colchetes ao redor de equações como [ C2 = ... ] ou numeração de linhas fantasma.
    2. Escreva as contas e operações de forma simples, em texto corrido ou usando apenas cifrões simples para variáveis ($C_1$, $P_1$, $C_2$).
    3. Para mostrar operações de XOR ou substituição, escreva de maneira direta e limpa, por exemplo:
       C_2 = C_1 \\oplus (P_1 \\oplus P_2)
    4. Mantenha um tom didático, claro, direto ao ponto e acolhedor, típico de um monitor do CIn/UFPE.

    --- EMENTA / BASE DE CONHECIMENTO ---
    {base_conhecimento}
    -------------------------------------
    """

  if "messages" not in st.session_state:
    st.session_state.messages = []

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

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
