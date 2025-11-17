# 🤖 Agente RAG Local com Gemini (Google AI Studio)

Este projeto cria um assistente que responde perguntas com base nos seus documentos locais, utilizando **embeddings + recuperação semântica (RAG)** e o modelo **Gemini** do Google AI Studio.

## 🚀 Como usar

1. Crie um virtualenv e instale as dependências:
```bash
python -m venv venv
source venv/bin/activate   # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
```

2. Defina sua API key do Google AI Studio (Gemini). No Linux/macOS:
```bash
export GOOGLE_API_KEY="sua_chave_aqui"
```
No Windows (PowerShell):
```powershell
setx GOOGLE_API_KEY "sua_chave_aqui"
```

3. Coloque seus manuais na pasta `data/` (pdf, docx ou txt).

4. Gere a base vetorial:
```bash
python ingestao.py
python verificar_base.py  # Diagnóstico atual
python otimizar_base.py   # Recriar base melhorada *(caso necessário)
python verificar_base.py  # Verificar melhorias 
```

5. Inicie a interface Streamlit:
```bash
streamlit run app.py
--- ou rode a versão clara
streamlit run claro3.py
```

6. Acesse no navegador: http://localhost:8501. (O comando anterior deverá abrir automaticamente o seu navegador, caso não abra teste com a url).

---

Observações:
- Caso de falha no modelo do gemini, rodar a lista para trocar o modelo. (python verificar_base.py) - Troque o modelo de acordo com a lista 
- Mantenha sua chave segura e não a compartilhe.
- controll + C = parar de rodar no VSCODE
- PARA CONSEGUIR UMA CHAVE API KEY DO GOOGLE, BASTA CRIAR UMA GRATUITAMENTE NO GOOGLE STUDIO AI. 



CODÍGOS EM SEQUÊNCIA (VSCODE):
ABRIR O FOLDER DO PROJETO, ABRIR UM NOVO TERMINAL:

python -m venv venv
venv\Scripts\activate no Windows
pip install -r requirements.txt
setx GOOGLE_API_KEY "AIzaSyCcstDNaAShqseZ6QKYETqrDmCny3Bxw1I"
python ingestao.py
python verificar_base.py  # Diagnóstico atual
python otimizar_base.py   # Recriar base melhorada *(caso necessário)
python verificar_base.py  # Verificar melhorias
streamlit run claro3.py
