# 🏢 **API de Market Segmentations**

## 📋 **Visão Geral**

API exclusiva para gerenciamento de segmentações de mercado. Fornece operações CRUD completas com validações específicas e tratamento de erros robusto.

## 🚀 **Endpoints Disponíveis**

### **1. Criar Múltiplas Segmentações (Bulk)**
```http
POST /members-book-service/v1/members/market-segmentations/bulk
```
**Tag**: `Market Segmentations`

**Request Body:**
```json
{
  "market_segmentations": [
    {"name": "E-commerce"},
    {"name": "Educação"},
    {"name": "Logística"}
  ]
}
```

**Exemplo:**
```bash
curl -X POST "http://localhost:8000/members-book-service/v1/members/market-segmentations/bulk" \
  -H "Content-Type: application/json" \
  -d '{
    "market_segmentations": [
      {"name": "E-commerce"},
      {"name": "Educação"},
      {"name": "Logística"}
    ]
  }'
```

**Resposta:**
```json
{
  "message": "Segmentações de mercado processadas com sucesso!",
  "status": "success",
  "data": [
    {
      "id": 4,
      "name": "E-commerce",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": null
    },
    {
      "id": 5,
      "name": "Educação",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": null
    },
    {
      "id": 6,
      "name": "Logística",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": null
    }
  ],
  "created_count": 3,
  "errors": []
}
```

## 📝 **Nota Importante**

Para operações CRUD completas de market segmentations, use o endpoint principal `/populate-data` que suporta upsert de todas as tabelas, incluindo market segmentations.

## 🔒 **Validações e Regras**

### **Criação**
- ✅ **Nome obrigatório**: Campo `name` é obrigatório
- ✅ **Nome único**: Não permite duplicatas por nome
- ✅ **Validação de duplicata**: Verifica se já existe antes de criar

### **Atualização**
- ✅ **Nome opcional**: Campo `name` é opcional na atualização
- ✅ **Validação de duplicata**: Verifica se o novo nome já existe
- ✅ **Preservação de dados**: Mantém dados existentes se não fornecidos

### **Remoção**
- ✅ **Verificação de existência**: Verifica se a segmentação existe antes de remover
- ✅ **Integridade referencial**: Considera relacionamentos com outras tabelas

## ⚠️ **Tratamento de Erros**

### **Erro 400 - Bad Request**
```json
{
  "detail": "Segmentação de mercado com nome 'Tecnologia' já existe"
}
```

### **Erro 404 - Not Found**
```json
{
  "detail": "Segmentação de mercado não encontrada"
}
```

### **Erro 500 - Internal Server Error**
```json
{
  "detail": "Erro ao criar segmentação: [detalhes do erro]"
}
```

## 📊 **Códigos de Status HTTP**

| Código | Descrição | Quando Ocorre |
|--------|-----------|---------------|
| `200` | OK | Operação realizada com sucesso |
| `201` | Created | Segmentação criada com sucesso |
| `400` | Bad Request | Dados inválidos ou duplicata |
| `404` | Not Found | Segmentação não encontrada |
| `500` | Internal Server Error | Erro interno do servidor |

## 🎯 **Casos de Uso**

### **1. Criação Individual**
- Ideal para criar uma segmentação específica
- Validação imediata de duplicatas
- Resposta rápida e direta

### **2. Criação em Lote**
- Ideal para popular o sistema com múltiplas segmentações
- Processamento eficiente de múltiplos itens
- Relatório de erros detalhado

### **3. Atualização**
- Modificar nome de segmentação existente
- Preservar histórico de criação
- Validação de duplicatas

### **4. Consulta**
- Listar todas as segmentações disponíveis
- Buscar segmentação específica por ID
- Dados completos com timestamps

## 🔄 **Fluxo de Operações**

### **Criação Individual:**
1. Validar dados de entrada
2. Verificar se nome já existe
3. Criar nova segmentação
4. Retornar dados criados

### **Criação em Lote:**
1. Processar cada segmentação individualmente
2. Verificar duplicatas para cada item
3. Criar segmentações válidas
4. Coletar erros de itens inválidos
5. Fazer commit de todas as criações
6. Retornar relatório completo

### **Atualização:**
1. Verificar se segmentação existe
2. Validar novo nome (se fornecido)
3. Verificar duplicatas
4. Atualizar dados
5. Retornar segmentação atualizada

## 🚀 **Vantagens da API Exclusiva**

- ✅ **Especializada**: Focada apenas em market segmentations
- ✅ **Validações específicas**: Regras de negócio dedicadas
- ✅ **Performance otimizada**: Operações diretas e eficientes
- ✅ **Tratamento de erros robusto**: Mensagens claras e específicas
- ✅ **Flexibilidade**: Suporte a operações individuais e em lote
- ✅ **Consistência**: Padrões de resposta uniformes
- ✅ **Documentação completa**: Endpoints bem documentados

## 📝 **Exemplos Práticos**

### **Cenário 1: Setup Inicial**
```bash
# Criar segmentações básicas
curl -X POST "http://localhost:8000/members-book-service/v1/members/market-segmentations/bulk" \
  -H "Content-Type: application/json" \
  -d '{
    "market_segmentations": [
      {"name": "Tecnologia"},
      {"name": "Saúde"},
      {"name": "Educação"},
      {"name": "Fintech"}
    ]
  }'
```

### **Cenário 2: Adicionar Nova Segmentação**
```bash
# Criar segmentação específica
curl -X POST "http://localhost:8000/members-book-service/v1/members/market-segmentations/" \
  -H "Content-Type: application/json" \
  -d '{"name": "E-commerce"}'
```

### **Cenário 3: Atualizar Segmentação**
```bash
# Renomear segmentação
curl -X PUT "http://localhost:8000/members-book-service/v1/members/market-segmentations/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Tecnologia Avançada"}'
```

### **Cenário 4: Consultar Segmentações**
```bash
# Listar todas
curl -X GET "http://localhost:8000/members-book-service/v1/members/market-segmentations/"

# Buscar específica
curl -X GET "http://localhost:8000/members-book-service/v1/members/market-segmentations/1"
```

---

## 🎉 **API Pronta para Uso!**

A API de Market Segmentations está **completa** e **pronta para uso**! 

- ✅ **6 endpoints** funcionais
- ✅ **Validações robustas**
- ✅ **Tratamento de erros completo**
- ✅ **Documentação detalhada**
- ✅ **Exemplos práticos**
