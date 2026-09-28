import os
from google import genai
from google.genai import types
import streamlit as st

st.set_page_config(
    page_title="CryptoCIn Tutor", page_icon="🛡️", layout="centered"
)

st.title("🛡️ CryptoCIn Tutor (CIn/UFPE)")
st.markdown(

     "O teu assistente virtual para a disciplina de Criptografia (CIn/UFPE)" 
    " **Baseado nas referências teóricas do curso**."
)

# Gestão da Chave de API de forma segura
api_key = os.environ.get("GEMINI_API_KEY")

try:
  if not api_key:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
  pass

if not api_key:
  api_key = st.text_input("Cole a sua GEMINI_API_KEY aqui:", type="password")

if api_key:
  os.environ["GEMINI_API_KEY"] = api_key

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
    Você é o CryptoCIn Tutor, um assistente virtual académico e monitor especialista da disciplina de Criptografia do CIn/UFPE, baseando-se estritamente no livro 'A Graduate Course in Applied Cryptography' (Dan Boneh & Victor Shoup).

    Sua missão principal é ajudar os alunos a resolverem e entenderem dúvidas sobre questões, exercícios, teoremas e conceitos específicos da disciplina. 

    DIRETRIZES DE ATUAÇÃO PARA O TIRA-DÚVIDAS:
    1. Quando o aluno trouxer uma dúvida teórica ou sobre uma questão, explique o conceito passo a passo de forma didática, clara e analítica.
    2. Utilize os conceitos formais e matemáticos presentes na base de conhecimento.
    3. Guie o raciocínio mostrando a intuição por trás da resposta.
    4. Escreva todas as explicações e fórmulas matemáticas usando texto normal, português claro e símbolos legíveis (como Pr[], XOR, somatório), evitando completamente o uso de formatação LaTeX ($...$ ou blocos de equação).
    5. Mantenha um tom encorajador, académico e colaborativo.

    --- BASE DE CONHECIMENTO ---
    {base_conhecimento}
    ----------------------------
    """

  # Inicializa apenas o histórico de mensagens no session_state
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
    # Adiciona a mensagem do utilizador ao histórico visual
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
      st.markdown(user_query)

    with st.chat_message("assistant"):
      with st.spinner("O CryptoCIn Tutor está a analisar a sua dúvida..."):
        try:
          # Instancia o cliente de forma fresca e segura a cada requisição para evitar timeout/fecho de socket
          client = genai.Client(api_key=api_key)

          # Constrói o histórico de conversação para o formato esperado pelo Gemini
          chat_history = []
          for msg in st.session_state.messages[:-1]:  # Exclui a última query atual
            role = "user" if msg["role"] == "user" else "model"
            chat_history.append(
                types.Content(
                    role=role, parts=[types.Part.from_text(text=msg["content"])]
                )
            )

          # Cria a sessão de chat passando o histórico prévio
          chat = client.chats.create(
              model="gemini-3.8-flash",
              history=chat_history,
              config=types.GenerateContentConfig(
                  system_instruction=system_instruction, temperature=0.3
              ),
          )

          response = chat.send_message(user_query)
          bot_reply = response.text
          st.markdown(bot_reply)

          # Adiciona a resposta ao histórico
          st.session_state.messages.append(
              {"role": "assistant", "content": bot_reply}
          )
        except Exception as e:
          st.error(f"Ocorreu um erro ao gerar a resposta: {e}")
else:
  st.info(
      "Por favor, insira a sua chave da API do Gemini para iniciar o"
      " assistente."
  )
