# 🐍 ClassUP Converter API (Python + Flask)

API auxiliar em **Python + Flask** usada pela aplicação [ClassUP](https://github.com/felipexxxxx/classup) para converter arquivos de usuários em formatos como `.csv`, `.json`, `.sql` ou `.xlsx` em um JSON padronizado compatível com o backend Java.

---

## 🎯 Objetivo

Permitir que administradores da plataforma façam **upload de arquivos com dados de alunos e professores**, para que sejam automaticamente convertidos para o formato necessário para importação no sistema ClassUP.

---

## 📦 Formatos Suportados

- `.csv`
- `.json`
- `.xlsx` / `.xls`
- `.sql` com inserts no padrão:

```
INSERT INTO usuarios (...) VALUES ('Nome', 'Email', 'CPF', 'Tipo');
```

---

## 📂 Estrutura do Projeto

```
📁 classup-converter-api/
├── app.py                  # API Flask principal
├── converterArquivoAPI.py  # Lógica de conversão
├── uploads/                # Diretório temporário para uploads
├── requirements.txt        # Dependências do projeto
```

---

## ⚙️ Funcionalidade

Esta API funciona como um **serviço externo** para o frontend da aplicação. O fluxo é:

1. O **administrador** faz upload de um arquivo.
2. O frontend envia esse arquivo para esta API Python.
3. A API converte os dados e retorna um JSON padronizado.
4. O frontend envia esse JSON ao backend Java para registrar os usuários.

---

## 🔄 Fluxo Ilustrado

```
      Front 
        ↓
Python Flask (converter)
        ↓
JSON formatado
        ↓
      Front 
        ↓  
Java Spring Boot (importar)

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
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode a aplicação
python app.py
```

A aplicação ficará disponível em: [http://localhost:5000](http://localhost:5000)

---

## 🌐 Endpoints

### `POST /converterJson`

Converte um arquivo para JSON formatado para o backend Java.

#### Requisição:
- Tipo: `multipart/form-data`
- Campo: `file`

#### Resposta:
- `200 OK` com lista de usuários
- `400 Bad Request` se nenhum arquivo for enviado
- `500 Internal Server Error` em caso de falha na conversão

---

## 🔓 CORS

Ajuste o CORS para aceitar requisições de qualquer origem.

```python
CORS(app)
```



## 📜 Licença

Este projeto é de uso exclusivo da plataforma ClassUP.

---

## 👨‍💻 Autor

Desenvolvido por [Felipe de Paula](https://github.com/felipexxxxx)