# vector_db.py

import os
import chromadb
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# 모듈 레벨에서 임베딩 객체를 한 번만 생성하여 재사용
try:
    embeddings = AzureOpenAIEmbeddings(
        openai_api_key=os.getenv("AOAI_API_KEY"),
        azure_endpoint=os.getenv("AOAI_ENDPOINT"),
        azure_deployment=os.getenv("AOAI_DEPLOY_EMBED_3_LARGE"),
        openai_api_version=os.getenv("AOAI_API_VERSION")
    )
except Exception as e:
    print(f"임베딩 모델 로딩 실패: {e}. 환경변수를 확인하세요.")
    embeddings = None

def get_vector_db_collection():
    """ChromaDB 클라이언트를 초기화하고 컬렉션을 반환합니다."""
    client = chromadb.Client()
    try:
        # get_collection은 컬렉션이 없으면 오류를 발생시키므로 get_or_create_collection 사용
        return client.get_or_create_collection("archi_docs")
    except Exception as e:
        print(f"ChromaDB 컬렉션 가져오기 실패: {e}")
        return None

def search_docs(query: str, top_k: int = 2) -> list[dict]:
    """주어진 쿼리와 가장 관련성 높은 문서를 VectorDB에서 검색합니다."""
    if not embeddings:
        print("임베딩 모델이 로드되지 않아 검색을 수행할 수 없습니다.")
        return []
    
    collection = get_vector_db_collection()
    if not collection:
        print("VectorDB 컬렉션을 가져올 수 없어 검색을 수행할 수 없습니다.")
        return []

    try:
        q_emb = embeddings.embed_query(query)
        results = collection.query(
            query_embeddings=[q_emb],
            n_results=top_k
        )
        
        docs = []
        # results['documents']는 리스트의 리스트 형태 [[doc1, doc2]]
        if results and results.get("documents"):
            for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                docs.append({"content": doc, "source": meta.get("source", "Unknown")})
        return docs
    except Exception as e:
        print(f"문서 검색 중 오류 발생: {e}")
        return []