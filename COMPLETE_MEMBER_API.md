# API de Membros Completos - Member Book Service

Este documento descreve a nova funcionalidade de criação de membros completos com todas as informações relacionadas.

## 🎯 **Funcionalidades Implementadas**

### ✅ **Endpoints Disponíveis**

#### 1. **POST /members/complete**
Cria um membro completo com todas as informações relacionadas.

**Request Body:**
```json
{
  "name": "João Silva",
  "position": "Desenvolvedor Sênior",
  "biography": "Desenvolvedor com 8 anos de experiência...",
  "document": "12345678901",
  "photo_url": "https://example.com/photos/joao_silva.jpg",
  "status": "active",
  "profile_id": 1,
  "expired_at": "2024-12-31",
  "address": {
    "street": "Rua das Flores",
    "number": "123",
    "complement": "Apto 45",
    "neighborhood": "Centro",
    "city": "São Paulo",
    "state": "SP",
    "country": "Brazil",
    "postal_code": "01234567"
  },
  "contact_channels": [
    {
      "type": "email",
      "content": "joao.silva@email.com"
    },
    {
      "type": "whatsapp",
      "content": "11987654321"
    },
    {
      "type": "linkedin",
      "content": "https://linkedin.com/in/joaosilva"
    }
  ],
  "additional_info": {
    "hobby": "Fotografia e viagens",
    "role_duration": 24,
    "children_count": 2
  }
}
```

#### 2. **PUT /members/populate-data**
Popula o sistema com dados completos fornecidos pelo usuário.

**Request Body:**
```json
{
  "members": [
    {
      "name": "João Silva",
      "position": "Desenvolvedor Sênior",
      "document": "12345678901",
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
          "content": "joao.silva@email.com"
        }
      ]
    }
  ],
  "clear_existing": false
}
```

#### 3. **PUT /members/populate-sample-data**
Popula o sistema com dados de exemplo completos (5 membros).

**Query Parameters:**
- `clear_existing` (boolean, opcional): Se deve limpar dados existentes

**Exemplo:**
```
PUT /members/populate-sample-data?clear_existing=true
```

#### 4. **PUT /members/populate-data-simple**
Endpoint mantido para compatibilidade (apenas profiles).

## 📋 **Estrutura de Dados**

### **Membro Completo**
- **Dados básicos**: nome, posição, biografia, documento, foto, status, perfil
- **Endereço**: rua, número, complemento, bairro, cidade, estado, país, CEP
- **Canais de contato**: email, WhatsApp, LinkedIn, Instagram, telefone
- **Informações adicionais**: hobby, tempo de trabalho, número de filhos

### **Validações Implementadas**

#### **CPF**
- Deve ter 11 dígitos
- Validação básica de formato
- Verificação de duplicatas

#### **CEP**
- Deve ter 8 dígitos
- Formato brasileiro

#### **Email**
- Deve conter @
- Validação de formato

#### **Telefone/WhatsApp**
- Deve ter 10 ou 11 dígitos
- Apenas números

#### **Estados**
- Enum com todos os estados brasileiros
- Validação de sigla

## 🚀 **Como Usar**

### **1. Popular com Dados de Exemplo**
```bash
curl -X PUT "http://localhost:8000/members-book-service/v1/members/populate-sample-data?clear_existing=true"
```

### **2. Criar Membro Individual Completo**
```bash
curl -X POST "http://localhost:8000/members-book-service/v1/members/complete" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "document": "12345678901",
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
        "content": "joao.silva@email.com"
      }
    ]
  }'
```

### **3. Popular com Dados Customizados**
```bash
curl -X PUT "http://localhost:8000/members-book-service/v1/members/populate-data" \
  -H "Content-Type: application/json" \
  -d '{
    "members": [...],
    "clear_existing": false
  }'
```

## 📊 **Resposta da API**

### **Sucesso**
```json
{
  "message": "Dados populados com sucesso!",
  "status": "success",
  "data": {
    "profiles_updated": true,
    "members_created": 5,
    "errors_count": 0,
    "timestamp": "2024-01-01T00:00:00Z"
  },
  "created_members": [...],
  "errors": []
}
```

### **Erro**
```json
{
  "detail": "Erro ao popular dados completos: Já existe um membro com este documento"
}
```

## 🔧 **Configuração**

### **Dependências**
- `pydantic` - Validação de dados
- `sqlalchemy` - ORM
- `fastapi` - Framework web

### **Banco de Dados**
- PostgreSQL
- Tabelas relacionadas: members, addresses, contact_channels, additional_infos, profiles

## 📝 **Exemplos de Dados**

### **Membros de Exemplo Incluídos**
1. **João Silva** - Desenvolvedor Sênior (eternity)
2. **Maria Santos** - Product Manager (infinity)
3. **Pedro Oliveira** - UX/UI Designer (admin)
4. **Ana Costa** - Data Scientist (standalone_profile)
5. **Carlos Ferreira** - DevOps Engineer (eternity)

### **Tipos de Perfil**
- `eternity` - Perfil eterno
- `infinity` - Perfil infinito
- `admin` - Perfil administrativo
- `standalone_profile` - Perfil standalone (com expiração)

### **Status de Membro**
- `pending` - Pendente
- `active` - Ativo
- `inactive` - Inativo
- `canceled` - Cancelado

### **Canais de Contato**
- `email` - Email
- `whatsapp` - WhatsApp
- `phone` - Telefone
- `linkedin` - LinkedIn
- `instagram` - Instagram
- `others` - Outros

## 🎯 **Benefícios**

- ✅ **Criação completa** de membros em uma única operação
- ✅ **Validação robusta** de todos os dados
- ✅ **Transações seguras** com rollback em caso de erro
- ✅ **Dados de exemplo** para testes
- ✅ **Compatibilidade** com endpoints existentes
- ✅ **Documentação completa** da API

## 🔄 **Próximos Passos**

1. **Testes automatizados** para todos os endpoints
2. **Logs estruturados** para auditoria
3. **Cache** para consultas frequentes
4. **Paginação** para listagens grandes
5. **Filtros avançados** por perfil, status, etc.
