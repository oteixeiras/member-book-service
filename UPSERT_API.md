# API de Upsert - Member Book Service

Este documento descreve a funcionalidade de upsert (criar ou atualizar) para todas as tabelas do sistema.

## 🏷️ **Tags das Rotas**

### **Data Management**
- `PUT /members/populate-data` - Endpoint principal para upsert de dados

### **Members**
- `GET /members/` - Listar membros
- `GET /members/{id}` - Buscar membro por ID
- `POST /members/` - Criar membro
- `PUT /members/{id}` - Atualizar membro
- `DELETE /members/{id}` - Remover membro

### **Market Segmentations**
- `POST /members/market-segmentations/bulk` - Criar múltiplas segmentações

## 🎯 **Funcionalidades Implementadas**

### ✅ **Endpoint Principal**

#### **PUT /members/populate-data**
Endpoint único para criar ou atualizar dados do sistema. Suporta upsert de todas as tabelas relacionadas.

**Tag**: `Data Management`

**Request Body:**
```json
{
  "companies": [
    {
      "name": "Tech Corp",
      "document": "12345678000195",
      "founded_year": "2020-01-01",
      "market_segmentation_id": 1,
      "address": {
        "street": "Rua da Tecnologia",
        "number": "100",
        "city": "São Paulo",
        "state": "SP",
        "postal_code": "01234567"
      }
    }
  ],
  "members": [
    {
      "name": "João Silva",
      "document": "12345678901",
      "position": "Desenvolvedor",
      "profile_id": 1,
      "address": {
        "street": "Rua das Flores",
        "number": "123",
        "city": "São Paulo",
        "state": "SP",
        "postal_code": "01234567"
      },
      "contact_channels": [
        {
          "type": "email",
          "content": "joao@email.com"
        },
        {
          "type": "whatsapp",
          "content": "11987654321"
        }
      ],
      "additional_info": {
        "hobby": "Programação",
        "role_duration": 24,
        "children_count": 2
      }
    }
  ],
  "performances": [
    {
      "count_closed_deals": 10,
      "value_closed_deals": 50000,
      "referrals_received": 5,
      "total_value_per_referral": 25000,
      "referrals_given": 3,
      "company_id": 1
    }
  ]
}
```

## 📋 **Estrutura de Dados**

### **Tabelas Suportadas**

#### **1. Companies**
- **Campos únicos**: `document` (CNPJ)
- **Comportamento**: Cria se não existir, atualiza se existir
- **Campos opcionais**: Todos
- **Relacionamentos**: `address`, `market_segmentation_id`
- **Otimização**: Objetos vazios são automaticamente desconsiderados

#### **2. Members**
- **Campos únicos**: `document` (CPF)
- **Comportamento**: Cria se não existir, atualiza se existir
- **Campos opcionais**: Todos
- **Relacionamentos**: `address`, `contact_channels`, `additional_info`, `profile_id`
- **Otimização**: Objetos vazios são automaticamente desconsiderados

#### **3. Performances**
- **Campos únicos**: Nenhum
- **Comportamento**: Sempre cria novo registro
- **Campos opcionais**: Todos
- **Relacionamentos**: `company_id`
- **Otimização**: Objetos vazios são automaticamente desconsiderados

## 🔄 **Lógica de Upsert**

### **Criação vs Atualização**

#### **Criação (INSERT)**
- Quando não existe registro com campo único
- Cria novo registro com dados fornecidos
- Campos não fornecidos ficam como `NULL`

#### **Atualização (UPDATE)**
- Quando existe registro com campo único
- Atualiza apenas campos fornecidos
- Campos não fornecidos mantêm valores existentes

#### **Ignorar Duplicatas**
- Se campo único já existe e dados são idênticos: **ignora**
- Se campo único já existe e dados são diferentes: **atualiza**
- Se campo único não existe: **cria**

#### **Desconsiderar Objetos Vazios**
- **Objetos sem campos populados**: **ignorados automaticamente**
- **Validação inteligente**: Verifica se pelo menos um campo tem valor
- **Relacionamentos**: Considera objetos aninhados (address, contact_channels, etc.)
- **Performance**: Evita operações desnecessárias no banco

### **Campos Únicos por Tabela**

| Tabela | Campo Único | Comportamento | Otimização |
|--------|-------------|---------------|------------|
| `companies` | `document` (CNPJ) | Upsert por CNPJ | Ignora objetos vazios |
| `members` | `document` (CPF) | Upsert por CPF | Ignora objetos vazios |
| `performances` | Nenhum | Sempre cria novo | Ignora objetos vazios |
| `profiles` | N/A | Criados automaticamente | Sempre presentes |

## 🚀 **Como Usar**

### **1. Popular dados completos**
```bash
curl -X PUT "http://localhost:8000/members-book-service/v1/members/populate-data" \
  -H "Content-Type: application/json" \
  -d '{
    "companies": [
      {
        "name": "Tech Corp",
        "document": "12345678000195",
        "market_segmentation_id": 1
      }
    ],
    "members": [
      {
        "name": "João Silva",
        "document": "12345678901",
        "profile_id": 1
      }
    ]
  }'
```

### **2. Criar apenas empresas**
```bash
curl -X PUT "http://localhost:8000/members-book-service/v1/members/populate-data" \
  -H "Content-Type: application/json" \
  -d '{
    "companies": [
      {
        "name": "Tech Corp",
        "document": "12345678000195",
        "address": {
          "street": "Rua da Tecnologia",
          "city": "São Paulo",
          "state": "SP",
          "postal_code": "01234567"
        }
      }
    ]
  }'
```

### **3. Criar apenas membros completos**
```bash
curl -X PUT "http://localhost:8000/members-book-service/v1/members/populate-data" \
  -H "Content-Type: application/json" \
  -d '{
    "members": [
      {
        "name": "João Silva",
        "document": "12345678901",
        "address": {
          "street": "Rua das Flores",
          "city": "São Paulo",
          "state": "SP",
          "postal_code": "01234567"
        },
        "contact_channels": [
          {
            "type": "email",
            "content": "joao@email.com"
          }
        ]
      }
    ]
  }'
```

### **4. Atualizar apenas dados existentes**
```bash
curl -X PUT "http://localhost:8000/members-book-service/v1/members/populate-data" \
  -H "Content-Type: application/json" \
  -d '{
    "members": [
      {
        "document": "12345678901",
        "position": "Desenvolvedor Sênior"
      }
    ]
  }'
```

### **5. Exemplo com objetos vazios (ignorados automaticamente)**
```bash
curl -X PUT "http://localhost:8000/members-book-service/v1/members/populate-data" \
  -H "Content-Type: application/json" \
  -d '{
    "companies": [
      {
        "name": "Tech Corp",
        "document": "12345678000195"
      },
      {}  // Objeto vazio - será ignorado
    ],
    "members": [
      {
        "name": "João Silva",
        "document": "12345678901"
      },
      {}  // Objeto vazio - será ignorado
    ]
  }'
```

## 📊 **Resposta da API**

### **Sucesso**
```json
{
  "message": "Dados processados com sucesso!",
  "status": "success",
  "data": {
    "created_count": {
      "profiles": 4,
      "companies": 1,
      "members": 1,
      "performances": 1
    },
    "updated_count": {
      "companies": 0,
      "members": 0
    },
    "errors": [],
    "timestamp": "2024-01-01T00:00:00Z"
  },
  "created_count": {
    "profiles": 4,
    "companies": 1,
    "members": 1,
    "performances": 1
  },
  "updated_count": {
    "companies": 0,
    "members": 0
  },
  "errors": []
}
```

### **Com Erros**
```json
{
  "message": "Dados processados com sucesso!",
  "status": "success",
  "data": {
    "created_count": {
      "members": 1
    },
    "updated_count": {},
    "errors": [
      "Market segmentation ID 0 não existe",
      "Profile ID 5 não existe"
    ],
    "timestamp": "2024-01-01T00:00:00Z"
  },
  "created_count": {
    "members": 1
  },
  "updated_count": {},
  "errors": [
    "Market segmentation ID 0 não existe",
    "Profile ID 5 não existe"
  ]
}
```

## 🔧 **Campos e Tipos**

### **CPF**
- Campo único para upsert
- Aceita qualquer formato (sem validação)

### **CNPJ**
- Campo único para upsert
- Aceita qualquer formato (sem validação)

### **CEP**
- Aceita qualquer formato (sem validação)

### **Email**
- Aceita qualquer formato (sem validação)

### **Telefone/WhatsApp**
- Aceita qualquer formato (sem validação)

### **Estados**
- Enum com todos os estados brasileiros
- Validação de sigla (apenas enum)

### **Foreign Keys**
- **Validação automática**: IDs de foreign keys são validados antes da inserção
- **Mensagens claras**: Erros específicos quando IDs não existem
- **Rollback seguro**: Transações são revertidas em caso de erro
- **IDs válidos**: 0 ou null são considerados inválidos

## 🎯 **Benefícios**

- ✅ **Endpoint único** para todas as operações
- ✅ **Upsert inteligente** (criar ou atualizar)
- ✅ **Campos opcionais** (flexibilidade)
- ✅ **Ignora duplicatas** (sem erros)
- ✅ **Transações seguras** com rollback
- ✅ **Relacionamentos automáticos**
- ✅ **Contadores detalhados** de operações
- ✅ **Tratamento de erros** granular
- ✅ **Sem validações restritivas** (máxima flexibilidade)
- ✅ **Performance otimizada** (sem validações desnecessárias)

## 🔄 **Fluxo de Processamento**

1. **Profiles**: Cria profiles padrão automaticamente
2. **Market Segmentations**: Upsert por nome
3. **Companies**: Upsert por CNPJ + endereço
4. **Members**: Upsert por CPF + relacionamentos
5. **Performances**: Cria novos registros
6. **Commit**: Salva todas as alterações
7. **Resposta**: Retorna contadores e erros

## 📝 **Exemplos de Uso**

### **Cenário 1: Primeira execução**
- Cria todos os dados fornecidos
- Profiles padrão são criados automaticamente

### **Cenário 2: Execução subsequente**
- Atualiza dados existentes
- Cria apenas novos dados
- Ignora duplicatas idênticas

### **Cenário 3: Dados parciais**
- Atualiza apenas campos fornecidos
- Mantém campos não fornecidos
- Cria relacionamentos se fornecidos

A API está otimizada para ser **idempotente** e **flexível**! 🎉
