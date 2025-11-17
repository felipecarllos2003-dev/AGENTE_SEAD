import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def verificar_base():
    """Verifica a qualidade da base vetorial"""
    
    MODEL_NAME = "all-MiniLM-L6-v2"
    embedder = SentenceTransformer(MODEL_NAME)
    
    # Carregar base
    index = faiss.read_index("embeddings/faiss.index")
    with open("embeddings/meta.json", "r", encoding="utf-8") as f:
        meta = json.load(f)
    
    texts = meta.get("texts", [])
    metas = meta.get("metas", [])
    
    print(f"📊 Estatísticas da Base:")
    print(f"   - Total de chunks: {len(texts)}")
    print(f"   - Total no índice FAISS: {index.ntotal}")
    
    # Verificar distribuição de tamanhos
    tamanhos = [len(text.split()) for text in texts]
    print(f"   - Tamanho médio dos chunks: {np.mean(tamanhos):.1f} palavras")
    print(f"   - Menor chunk: {min(tamanhos)} palavras")
    print(f"   - Maior chunk: {max(tamanhos)} palavras")
    
    # Testar algumas consultas
    queries_teste = [
        "procedimento administrativo",
        "licitação",
        "documentação necessária",
        "normas de conduta"
    ]
    
    print("\n🔍 Testando recuperação...")
    for query in queries_teste:
        q_emb = embedder.encode([query], convert_to_numpy=True)
        norms = np.linalg.norm(q_emb, axis=1, keepdims=True) + 1e-12
        q_emb = q_emb / norms
        
        D, I = index.search(q_emb.astype('float32'), 3)
        
        print(f"   '{query}': scores = {[f'{s:.3f}' for s in D[0]]}")

if __name__ == "__main__":
    verificar_base()