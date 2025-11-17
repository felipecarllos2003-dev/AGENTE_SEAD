import os, json, numpy as np, faiss
from typing import List
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

INDEX_PATH = "embeddings/faiss.index"
META_PATH = "embeddings/meta.json"
MODEL_NAME = "all-MiniLM-L6-v2"
GEMINI_MODEL = "gemini-2.5-flash"

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Defina sua chave com: export GOOGLE_API_KEY='sua_chave_aqui'")
genai.configure(api_key=api_key)

embedder = SentenceTransformer(MODEL_NAME)
if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
    raise FileNotFoundError("Index ou meta não encontrados. Rode ingestao.py primeiro.")

index = faiss.read_index(INDEX_PATH)
with open(META_PATH, "r", encoding="utf-8") as f:
    meta = json.load(f)
texts = meta.get("texts", [])
metas = meta.get("metas", [])

def normalize(v):
    v = np.array(v, dtype=float)
    return v / (np.linalg.norm(v, axis=-1, keepdims=True) + 1e-12)

# função def retrieve melhorado
def retrieve(query: str, top_k: int = 8, score_threshold: float = 0.3):
    """Recuperação com filtro por score mínimo"""
    q_emb = embedder.encode([query], convert_to_numpy=True)
    q_emb = normalize(q_emb)
    
    # Buscar mais resultados para depois filtrar
    D, I = index.search(q_emb.astype('float32'), top_k * 2)
    
    hits = []
    for idx, (score, i) in enumerate(zip(D[0], I[0])):
        if score >= score_threshold and i < len(texts):  # Verificar índice válido
            hits.append({
                "text": texts[i], 
                "meta": metas[i], 
                "score": float(score), 
                "idx": int(i)
            })
        if len(hits) >= top_k:
            break
    
    # Ordenar por score (maior primeiro)
    hits.sort(key=lambda x: x["score"], reverse=True)
    return hits

def generate_with_gemini(prompt: str, max_output_tokens: int = 512):
    model = genai.GenerativeModel(GEMINI_MODEL)
    # gera conteúdo com o prompt; o SDK pode retornar diferentes estruturas dependendo da versão
    response = model.generate_content(prompt)
    # tentar extrair texto seguro
    text = ""
    try:
        text = response.text
    except Exception:
        try:
            # fallback para estruturas alternativas
            for item in response.output:
                for c in item.content:
                    if hasattr(c, "text"):
                        text += c.text
                    elif isinstance(c, dict) and "text" in c:
                        text += c["text"]
        except Exception:
            text = str(response)
    return text.strip()

#função ask melhorado
def ask(question: str, top_k: int = 8):
    hits = retrieve(question, top_k=top_k)
    
    if not hits:
        return "Não encontrei informações relevantes nos manuais para sua pergunta. Poderia reformular ou ser mais específico?"
    
    # Agrupar por arquivo para melhor organização
    context_by_file = {}
    for h in hits:
        arquivo = h['meta']['arquivo']
        if arquivo not in context_by_file:
            context_by_file[arquivo] = []
        context_by_file[arquivo].append(h['text'])
    
    # Construir contexto organizado
    context_parts = []
    for arquivo, textos in context_by_file.items():
        context_parts.append(f"=== {arquivo} ===")
        for i, texto in enumerate(textos[:3]):  # Máximo 3 chunks por arquivo
            context_parts.append(f"{i+1}. {texto}")
        context_parts.append("")
    
    context = "\n".join(context_parts)
    
    prompt = f"""# CONTEXTO DOS MANUAIS SEAD-GO

Base seu conhecimento exclusivamente nas informações abaixo:

{context}

# PERGUNTA DO USUÁRIO
{question}

# INSTRUÇÕES
- Responda baseado APENAS no contexto fornecido
- Seja conciso e direto
- Cite o manual de origem quando relevante
- Se não encontrar informação suficiente, diga isso claramente
- Mantenha linguagem profissional mas acessível

Resposta:"""
    
    return generate_with_gemini(prompt)
