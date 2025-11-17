print(f"RODANDO")

import google.generativeai as genai
import os

# Pega a chave API da variável de ambiente que você configurou
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("ERRO: Variável GOOGLE_API_KEY não encontrada.")
    print("Lembre-se de fechar e reabrir o terminal após usar o comando 'setx'.")
else:
    try:
        genai.configure(api_key=api_key)
        print("--- Modelos disponíveis para sua chave API ---")
        for m in genai.list_models():
            print(m.name)
        print("---------------------------------------------")

    except Exception as e:
        print(f"Ocorreu um erro ao conectar ao Google AI: {e}")