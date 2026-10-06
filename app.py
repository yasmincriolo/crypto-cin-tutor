import re
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


# Função para limpar e remover blocos indesejados de LaTeX gerados pela IA
def limpar_formatacao_matematica(texto):
  # Remove blocos \begin{aligned} ... \end{aligned} e transforma em quebras de linha limpas
  texto = re.sub(
      r"\\begin\{aligned\}(.*?)\\end\{aligned\}", r"\1", texto, flags=re.DOTALL
  )
  # Remove comandos de alinhamento e espaçamento excessivo
  texto = texto.replace(r"\&", "").replace(r"\quad", "").replace(r"\\", "\n")
  # Remove colchetes ao redor de equações [ ... ] transformando em texto simples
  texto = re.sub(r"\[\s*(.*?)\s*\]", r"\1", texto)
  # Remove parênteses em volta de variáveis isoladas indesejadas ex: (C_1) -> C_1
  texto = re.sub(r"\(([A-Za-z0-9_]+)\)", r"\1", texto)
  # Remove caixas de destaque \boxed{}
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
    - Cifras de Fluxo (Stream Ciphers) e OTP (One-Time Pad) - Ex: c = m XOR k.
    - Cifras de Bloco (Block Ciphers): Estrutura de Feistel, DES e AES.
    - Modos de Operação de Cifras de Bloco (CBC, CTR, GCM) e malha de segurança.
    - Funções de Hash Criptográficas e MACs (HMAC).

    ## Unidade 3: Criptografia Assimétrica (Chave Pública)
    - Funções de mão única com alçapão (Trapdoor One-Way Functions).
    - Criptossistema RSA e Troca de Chaves Diffie-Hellman.
    - Assinaturas Digitais e Curvas Elípticas (ECC).
    """

  system_instruction = f"""
    Você é o CryptoCIn Tutor, um assistente virtual acadêmico e monitor especialista da disciplina de Criptografia do Centro de Informática da UFPE (CIn/UFPE).

    Sua missão principal é ajudar os alunos a resolverem e entenderem dúvidas sobre questões, exercícios, listas, provas e conceitos da ementa da disciplina.

    DIRETRIZES DE ESCRITA:
    1. Explique os conceitos passo a passo de forma simples, clara e direta, como um monitor explicando num quadro.
    2. Escreva as equações matemáticas e contas linha por linha de forma natural, usando texto corrido e símbolos simples (como XOR ou +).
    3. Mantenha um tom didático, acolhedor e muito prestativo.

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

          # Limpa automaticamente qualquer formatação indesejada de colchetes ou LaTeX complexo
          bot_reply_limpo = limpar_formatacao_matematica(bot_reply)

          st.markdown(bot_reply_limpo)

          st.session_state.messages.append(
              {"role": "assistant", "content": bot_reply_limpo}
          )
        except Exception as e:
          st.error(f"Ocorreu um erro ao gerar a resposta: {e}")
else:
  st.info(
      "Por favor, insira a sua chave da API da Groq para iniciar o assistente."
  )
