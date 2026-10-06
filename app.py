import re
from groq import Groq
import streamlit as st

st.set_page_config(
    page_title="CryptoCIn Tutor", page_icon="🛡️", layout="centered"
)

st.title("🛡️️ CryptoCIn Tutor (CIn/UFPE)")
st.markdown(
    "O seu assistente virtual oficial para a disciplina de Criptografia"
    " do CIn/UFPE!"
)


def limpar_texto_maquina(texto):
  # Remove blocos de alinhamento LaTeX
  texto = re.sub(
      r"\\begin\{aligned\}(.*?)\\end\{aligned\}", r"\1", texto, flags=re.DOTALL
  )
  # Remove comandos de barras e alinhamentos
  texto = (
      texto.replace(r"\&", "")
      .replace(r"\quad", "")
      .replace(r"\\", "\n")
      .replace(r"\oplus", "combinado com (XOR)")
  )
  # Remove colchetes ao redor de equações
  texto = re.sub(r"\[\s*(.*?)\s*\]", r"\1", texto)
  # Remove parênteses e formatações robóticas de variáveis ex: (C_1) -> C_1
  texto = re.sub(r"\(([A-Za-z0-9_]+)\)", r"\1", texto)
  # Remove caixas e blocos estranhos
  texto = re.sub(r"\\boxed\{(.*?)\}", r"\1", texto)
  return texto


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
    - Cifras de Fluxo (Stream Ciphers) e OTP (One-Time Pad).
    - Cifras de Bloco (Block Ciphers): Estrutura de Feistel, DES e AES.
    - Modos de Operação de Cifras de Bloco (CBC, CTR, GCM).
    - Funções de Hash Criptográficas e MACs (HMAC).

    ## Unidade 3: Criptografia Assimétrica (Chave Pública)
    - Funções de mão única com alçapão (Trapdoor One-Way Functions).
    - Criptossistema RSA e Troca de Chaves Diffie-Hellman.
    - Assinaturas Digitais e Curvas Elípticas (ECC).
    """

  system_instruction = f"""
    Você é o CryptoCIn Tutor, um assistente virtual acadêmico e monitor especialista da disciplina de Criptografia do Centro de Informática da UFPE (CIn/UFPE).

    Sua missão principal é ajudar os alunos a entenderem a intuição por trás das questões e conceitos de forma humana, clara e didática, como se estivesse a explicar a um colega num quadro branco.

    DIRETRIZES DE ESCRITA:
    1. Escreva em texto totalmente natural e corrido, explicando os passos lógicos de forma amigável.
    2. Evite ao máximo símbolos matemáticos abstratos ou notações artificiais. Se precisar de referir uma variável ou valor, escreva o nome de forma limpa.
    3. Mantenha um tom acolhedor e prestativo, típico de um monitor do CIn/UFPE.

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

          # Aplica a limpeza cirúrgica para remover qualquer padrão robótico
          bot_reply_final = limpar_texto_maquina(bot_reply)

          st.markdown(bot_reply_final)

          st.session_state.messages.append(
              {"role": "assistant", "content": bot_reply_final}
          )
        except Exception as e:
          st.error(f"Ocorreu um erro ao gerar a resposta: {e}")
else:
  st.info(
      "Por favor, insira a sua chave da API da Groq para iniciar o assistente."
  )
