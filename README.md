
# 🐍 ClassUP Converter API (Python + Flask)

API auxiliar desenvolvida em **Python + Flask** usada pela aplicação [ClassUP](https://github.com/felipexxxxx/AgendaEdu-Frontend) para **converter arquivos de usuários** (`.csv`, `.json`, `.sql`, `.xlsx`) em um **JSON padronizado** compatível com o backend Java.

---

## 🎯 Objetivo

Permitir que **administradores da plataforma** façam upload de arquivos contendo dados de alunos e professores, para que sejam automaticamente convertidos para o formato esperado pela API Java da aplicação ClassUP.

---

## 📦 Formatos Suportados

- `.csv`
- `.json`
- `.xlsx` / `.xls`
- `.sql` com comandos `INSERT INTO` no padrão:

```sql
INSERT INTO usuarios (...) VALUES ('Nome', 'Email', 'CPF', 'Tipo');
```

---

## 📂 Estrutura do Projeto

```bash
📁 classup-converter-api/
├── app.py                  # API principal em Flask
├── converterArquivoAPI.py  # Lógica de conversão de arquivos
├── uploads/                # Diretório temporário para arquivos enviados
├── requirements.txt        # Dependências do projeto
├── Procfile                # Configuração para deploy no Railway
```

---

## ⚙️ Funcionamento da API

Esta API funciona como um **microserviço auxiliar**, sendo chamada diretamente pelo frontend do ClassUP. O fluxo completo:

1. O **administrador** faz upload de um arquivo pelo frontend.
2. O frontend envia o arquivo para a API Python (Flask).
3. A API processa o conteúdo e retorna um **JSON estruturado**.
4. O frontend envia esse JSON para o backend Java da aplicação.

---

## 🔄 Fluxo Ilustrado

```
  Frontend (Admin)
      ↓
API Flask (Conversão)
      ↓
 JSON padronizado
      ↓
  Frontend 
      ↓
Backend Java (Cadastro)
```

---

## 🧠 Exemplo de JSON gerado

```json
[
  {
    "nomeCompleto": "Ana Souza",
    "email": "ana@email.com",
    "cpf": "12345678900",
    "role": "ALUNO",
    "dataNascimento": "2001-05-20"
  },
  {
    "nomeCompleto": "Carlos Lima",
    "email": "carlos@email.com",
    "cpf": "98765432100",
    "role": "PROFESSOR",
    "dataNascimento": "1985-03-10"
  }
]
```

---

## 🚀 Como Executar Localmente

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/classup-converter-api.git
cd classup-converter-api

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate   # No Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode a aplicação
python app.py
```

A API estará disponível em: [http://localhost:5000](http://localhost:5000)

---

## 🌐 Endpoint

### `POST /converterJson`

Converte um arquivo enviado para JSON padronizado para o backend Java.

#### Requisição:
- Tipo: `multipart/form-data`
- Campo: `file`
- 
---

## 🔓 CORS

A API já vem configurada com CORS para aceitar chamadas do frontend:

```python
CORS(app, origins=["https://classup-web.netlify.app", "http://localhost:5173"])
```

---

## 🧩 Dependências Principais

As bibliotecas usadas neste projeto estão listadas em `requirements.txt`. As principais são:

- **Flask**: microframework web para construção da API.
- **flask-cors**: para permitir requisições entre frontend e backend.
- **pandas**: manipulação de dados tabulares de arquivos como `.csv` e `.xlsx`.
- **openpyxl**: suporte à leitura de arquivos Excel.
- **gunicorn**: servidor WSGI usado para deploy em produção (ex: Railway).

Para instalar todas as dependências:

```bash
pip install -r requirements.txt
```

---

## 📜 Licença

Este projeto é de uso exclusivo da plataforma ClassUP.

---

## 👨‍💻 Autor

Desenvolvido por [Felipe de Paula](https://github.com/felipexxxxx)
