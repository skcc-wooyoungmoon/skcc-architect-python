# data_loader.py

import os
import chromadb
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

def load_documents():
    """지정된 디렉토리에서 .txt 파일들을 로드하여 내용과 파일명을 반환합니다."""
    docs = []
    doc_dir = "rag/docs"
    if not os.path.isdir(doc_dir):
        print(f"오류: 문서 디렉토리 '{doc_dir}'를 찾을 수 없습니다. 'rag/docs' 디렉토리를 생성하고 참고 문서를 넣어주세요.")
        return docs

    for fname in os.listdir(doc_dir):
        if fname.endswith(".txt"):
            try:
                with open(os.path.join(doc_dir, fname), encoding="utf-8") as f:
                    docs.append({"content": f.read(), "source": fname})
            except Exception as e:
                print(f"'{fname}' 파일 로드 중 오류 발생: {e}")
    return docs

def build_vector_db():
    """문서를 로드하고, 임베딩을 생성하여 ChromaDB에 벡터 데이터베이스를 구축합니다."""
    client = chromadb.Client()

    collection_name = "archi_docs"
    # 컬렉션을 가져오거나, 없으면 생성합니다. 이미 데이터가 있다면 초기화합니다.
    if collection_name in [c.name for c in client.list_collections()]:
        client.delete_collection(name=collection_name)
    collection = client.create_collection(name=collection_name)

    docs_to_embed = load_documents()
    if not docs_to_embed:
        print("임베딩할 문서가 없습니다. rag/docs 디렉토리를 확인해주세요.")
        return None

    try:
        embeddings = AzureOpenAIEmbeddings(
            openai_api_key=os.getenv("AOAI_API_KEY"),
            azure_endpoint=os.getenv("AOAI_ENDPOINT"),
            azure_deployment=os.getenv("AOAI_DEPLOY_EMBED_3_LARGE"),
            openai_api_version=os.getenv("AOAI_API_VERSION")
        )
    except Exception as e:
        print(f"AzureOpenAIEmbeddings 초기화 중 오류 발생: {e}")
        print("환경 변수(AOAI_API_KEY, AOAI_ENDPOINT, AOAI_DEPLOY_EMBED_3_LARGE, AOAI_API_VERSION) 설정을 확인해주세요.")
        return None

    contents, metadatas, ids = [], [], []
    print(f"총 {len(docs_to_embed)}개의 문서를 처리합니다...")
    for i, doc in enumerate(docs_to_embed):
        contents.append(doc["content"])
        metadatas.append({"source": doc["source"]})
        ids.append(str(i)) # 고유 ID는 문자열이어야 함

    try:
        # ChromaDB는 문서와 ID를 받으면 자동으로 임베딩을 생성할 수 있지만,
        # 여기서는 명시적으로 LangChain의 임베딩 컴포넌트를 사용하여 추가합니다.
        # 이렇게 하면 임베딩 모델을 유연하게 교체할 수 있습니다.
        doc_embeddings = embeddings.embed_documents([doc['content'] for doc in docs_to_embed])
        collection.add(
            embeddings=doc_embeddings,
            documents=contents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"총 {len(contents)}개의 문서가 ChromaDB 컬렉션 '{collection_name}'에 추가되었습니다.")
    except Exception as e:
        print(f"ChromaDB에 데이터 추가 중 오류 발생: {e}")

    return collection

if __name__ == "__main__":
    print("벡터DB 구축을 시작합니다...")
    vector_db_collection = build_vector_db()
    if vector_db_collection:
        print(f"벡터DB 구축 완료! 컬렉션 이름: {vector_db_collection.name}, 문서 수: {vector_db_collection.count()}")
    else:
        print("벡터DB 구축에 실패했습니다.")