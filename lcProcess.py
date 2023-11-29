from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

class LangChainProcess:
      def __init__(self, file_path, encoding="utf-8",   chunk_size=300, chunk_overlap=50):
            self.file_path = file_path
            self.encoding = encoding
            self.chunk_size = chunk_size
            self.chunk_overlap = chunk_overlap
            self.docs = None
            self.texts = None
            self.db = None

      def load_text(self):
            loader = TextLoader(self.file_path, encoding=self.encoding)
            self.docs = loader.load()

      def split_text(self):
            text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=False
            )
            self.texts = text_splitter.split_documents(self.docs)

      def create_embeddings(self):
            embeddings_model = OpenAIEmbeddings()
            self.db = Chroma.from_documents(self.texts, embeddings_model)

      def ask_question(self, question):
            llm = ChatOpenAI(temperature=0)
            qa_chain = RetrievalQA.from_chain_type(llm, retriever=self.db.as_retriever())
            result = qa_chain({'query': question})
            return result