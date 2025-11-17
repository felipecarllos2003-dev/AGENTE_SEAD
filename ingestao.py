import os, json, glob, faiss, numpy as np
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
from docx import Document
from tqdm import tqdm

MODEL_NAME = "all-MiniLM-L6-v2"
embedder = SentenceTransformer(MODEL_NAME)
INDEX_PATH = "embeddings/faiss.index"
META_PATH = "embeddings/meta.json"

def ler_documento(path):
    ext = os.path.splitext(path)[1].lower()
    texto = ""
    if ext == ".pdf":
        reader = PdfReader(path)
        for page in reader.pages:
            texto += page.extract_text() or ""
    elif ext == ".docx":
        doc = Document(path)
        for p in doc.paragraphs:
            texto += p.text + "\\n"
    elif ext == ".txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            texto = f.read()
    return texto

#função chunk_text versão melhorada:

def chunk_text(texto, tamanho=400, sobreposicao=80):
    """Chunking mais inteligente que preserva estrutura"""
    import re
    
    # Limpeza inicial
    texto = re.sub(r'\s+', ' ', texto).strip()
    if not texto:
        return []
    
    # Tentar dividir por parágrafos primeiro
    paragraphs = [p.strip() for p in texto.split('\n') if p.strip()]
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for paragraph in paragraphs:
        para_words = paragraph.split()
        para_length = len(para_words)
        
        # Se o parágrafo sozinho for muito grande, dividir
        if para_length > tamanho:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_length = 0
            
            # Dividir parágrafo grande
            words = paragraph.split()
            for i in range(0, len(words), tamanho - sobreposicao):
                chunk = " ".join(words[i:i + tamanho])
                chunks.append(chunk)
            continue
        
        # Adicionar ao chunk atual se couber
        if current_length + para_length <= tamanho:
            current_chunk.append(paragraph)
            current_length += para_length
        else:
            # Salvar chunk atual e começar novo
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            
            # Overlap: manter parte do chunk anterior
            overlap_words = []
            if current_chunk:
                last_sentence = current_chunk[-1].split()
                overlap_words = last_sentence[-sobreposicao//2:] if len(last_sentence) > sobreposicao//2 else last_sentence
            
            current_chunk = [" ".join(overlap_words), paragraph] if overlap_words else [paragraph]
            current_length = len(" ".join(current_chunk).split())
    
    # Adicionar último chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return [chunk for chunk in chunks if chunk.strip()]

def processar_documentos(pasta="data"):
    arquivos = glob.glob(os.path.join(pasta, "*.*"))
    todos_chunks, metadados = [], []
    for arquivo in tqdm(arquivos, desc="Processando documentos"):
        try:
            texto = ler_documento(arquivo)
            chunks = chunk_text(texto)
            for idx, chunk in enumerate(chunks):
                todos_chunks.append(chunk)
                metadados.append({"arquivo": os.path.basename(arquivo), "chunk_id": idx, "len": len(chunk)})
        except Exception as e:
            print("Erro lendo", arquivo, e)
    return todos_chunks, metadados

def criar_base(pasta="data"):
    textos, metas = processar_documentos(pasta)
    if not textos:
        print("Nenhum documento/processamento encontrado em", pasta)
        return
    embeddings = embedder.encode(textos, convert_to_numpy=True, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    # normalizar para usar IndexFlatIP como aproximação de cosine
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True) + 1e-12
    embeddings = embeddings / norms

    d = embeddings.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump({"texts": textos, "metas": metas}, f, ensure_ascii=False, indent=2)
    print(f"✅ Base vetorial criada com {len(textos)} chunks. Salvos em {INDEX_PATH} e {META_PATH}")

if __name__ == "__main__":
    criar_base()
