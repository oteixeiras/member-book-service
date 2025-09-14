from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/member_book_db"
    
    # API
    api_v1_str: str = "/members-book-service/v1"
    project_name: str = "Member Book Service"
    
    # CORS
    backend_cors_origins: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        env_file_encoding = "utf-8"


# Carregar configurações
settings = Settings()

# Verificar se as variáveis de ambiente foram carregadas
if os.getenv("DATABASE_URL"):
    print(f"✅ Carregando DATABASE_URL do arquivo .env: {settings.database_url}")
else:
    print(f"⚠️  Usando DATABASE_URL padrão: {settings.database_url}")
