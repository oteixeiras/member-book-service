#!/usr/bin/env python3
"""
Script para executar migrações do banco de dados
"""
import subprocess
import sys
import os

def run_migration():
    """Executa as migrações do Alembic"""
    try:
        # Executar migração
        result = subprocess.run([
            "poetry", "run", "alembic", "upgrade", "head"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Migrações executadas com sucesso!")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print("❌ Erro ao executar migrações:")
        print(e.stderr)
        sys.exit(1)

if __name__ == "__main__":
    print("🔄 Executando migrações do banco de dados...")
    run_migration()
