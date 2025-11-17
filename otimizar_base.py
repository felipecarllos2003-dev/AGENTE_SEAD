import os
from ingestao import criar_base, embedder
import faiss
import numpy as np

def otimizar_base_existente():
    """Otimiza a base existente recriando com parâmetros melhores"""
    
    # Verificar se existe base atual
    if os.path.exists("embeddings/faiss.index"):
        print("📊 Analisando base atual...")
        index = faiss.read_index("embeddings/faiss.index")
        print(f"Base atual tem {index.ntotal} chunks")
    
    print("🔄 Recriando base com parâmetros otimizados...")
    criar_base()
    
    print("✅ Base otimizada criada com sucesso!")

if __name__ == "__main__":
    otimizar_base_existente()