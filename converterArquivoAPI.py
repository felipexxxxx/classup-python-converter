import pandas as pd
import json
import re
import os
import unicodedata
from dateutil import parser

MAPEAMENTO_CAMPOS = {
    "nomeCompleto": ["nome", "nome completo", "nome_completo", "nomecompleto"],
    "email": ["email", "e-mail", "contato"],
    "cpf": ["cpf", "documento", "doc", "cpf_usuario"],
    "role": ["role", "tipo", "tipo_usuario", "perfil", "categoria", "função"],
    "dataNascimento": ["dataNascimento", "datanascimento", "data_nascimento", "nascimento", "data de nascimento"]
}

def normalizar_texto(texto):
    if not texto:
        return ""
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r'[^a-z0-9]', '', texto)
    return texto

def normalizar_role(valor):
    if not valor:
        return None
    valor = valor.strip().lower()
    if valor in ["aluno", "estudante", "discente", "aprendiz"]:
        return "ALUNO"
    elif valor in ["professor", "docente", "instrutor", "educador"]:
        return "PROFESSOR"
    return None

def normalizar_data_nascimento(valor):
    if pd.isna(valor):
        return None

    try:
        data = parser.parse(str(valor), dayfirst=True, fuzzy=True)
        return data.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return None



def encontrar_coluna(df, campo_padrao, sinonimos):
    for alt in sinonimos:
        alt_norm = normalizar_texto(alt)
        for coluna_df in df.columns:
            col_norm = normalizar_texto(coluna_df)
            if col_norm == alt_norm:
                return coluna_df
    return None

def extrair_dados_de_sql(caminho_sql):
    with open(caminho_sql, "r", encoding="utf-8") as f:
        conteudo = f.read()

    matches = re.findall(r"INSERT INTO usuarios.*?VALUES\s*\((.*?)\);", conteudo, re.IGNORECASE)
    dados = []

    for match in matches:
        campos = [c.strip().strip("'") for c in re.findall(r"'(.*?)'", match)]

        if len(campos) == 5:
            dados.append({
                "nome": campos[0],
                "email": campos[1],
                "cpf": campos[2],
                "role": campos[3],
                "nascimento": campos[4]
            })

    return pd.DataFrame(dados)

def converter_arquivo_para_json(arquivo):
    extensao = os.path.splitext(arquivo)[1].lower()

    if extensao == ".csv":
        df = pd.read_csv(arquivo)

    elif extensao in [".xlsx", ".xls"]:
        df = pd.read_excel(arquivo)  # sem dtype=str, porque não funciona para células "Data"

    elif extensao == ".json":
        try:
            df = pd.read_json(arquivo)
        except ValueError:
            with open(arquivo, "r", encoding="utf-8") as f:
                data = json.load(f)
            df = pd.json_normalize(data)

    elif extensao == ".sql":
        df = extrair_dados_de_sql(arquivo)

    else:
        raise ValueError("Formato de arquivo não suportado")

    df = df.astype(str)

    mapeamento = {
        campo: encontrar_coluna(df, campo, sinonimos)
        for campo, sinonimos in MAPEAMENTO_CAMPOS.items()
    }

    col_data = mapeamento.get("dataNascimento")
    if col_data and col_data in df.columns:
        df[col_data] = df[col_data].apply(normalizar_data_nascimento)

    usuarios = []
    erros = []

    for _, row in df.iterrows():
        usuario = {}
        for campo, coluna in mapeamento.items():
            valor = None
            if coluna and coluna in row and pd.notna(row[coluna]):
                valor = str(row[coluna]).strip()
                if campo == "role":
                    valor = normalizar_role(valor)
            usuario[campo] = valor

        if all(usuario.get(campo) for campo in MAPEAMENTO_CAMPOS):
            usuarios.append(usuario)
        else:
            motivos = [f"Campo '{campo}' ausente ou inválido" for campo in MAPEAMENTO_CAMPOS if not usuario.get(campo)]
            erros.append({"usuario": usuario, "motivos": motivos})

    with open("usuarios_convertidos.json", "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=2, ensure_ascii=False)

    print(f"\n✅ {len(usuarios)} usuários convertidos com sucesso!")
    print(f"⚠️ {len(erros)} registros ignorados.")
    return {"usuarios": usuarios, "erros": erros}


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("❗ Uso: python converterArquivoAPI.py caminho/do/arquivo.csv|xlsx|json|sql")
    else:
        converter_arquivo_para_json(sys.argv[1])
