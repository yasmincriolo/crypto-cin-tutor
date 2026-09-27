# CryptoCIn Tutor

Assistente virtual acadêmico e monitor inteligente desenvolvido para apoiar os estudantes da disciplina de **Criptografia do CIn/UFPE**, estruturado estritamente com base na referência mundial ***"A Graduate Course in Applied Cryptography"*** de Dan Boneh & Victor Shoup.

## Sobre o Projeto
O **CryptoCIn Tutor** atua como um plantão de dúvidas virtual e interativo para os alunos. Ele é capaz de:
* Explicar conceitos teóricos complexos (Sigilo Perfeito, IND-CPA/CCA, MACs, ZKP).
* Auxiliar na resolução e demonstração passo a passo de exercícios e listas de provas.
* Utilizar reduções matemáticas e jogos de segurança (*security games*) fundamentados no livro-texto oficial da disciplina.

## Tecnologias Utilizadas
* Python
* Google GenAI SDK
* Google Gemini (`gemini-3.8-flash`)
* Google Colab (como ambiente de execução)

## Estrutura do Repositório
crypto-cin-tutor/
├── data/
│   └── base_conhecimento.txt   # Repositório de conceitos teóricos do Boneh & Shoup
├── src/
│   └── app.py                  # Script principal do assistente interativo
└── README.md                   # Documentação do projeto

## Como Executar
1. Clone o repositório ou abra o código no Google Colab.
2. Certifique-se de ter a biblioteca do Gemini instalada (`pip install google-genai`).
3. Insira sua chave de API do Gemini (`GEMINI_API_KEY`) quando solicitada.
4. Execute o script `src/app.py` e comece a interagir com o tutor enviando dúvidas teóricas ou enunciados de exercícios!
