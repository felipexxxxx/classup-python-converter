import pandas as pd
import json
import re
import os
import sys
from datetime import datetime

MAPEAMENTO_CAMPOS = {
    "nomeCompleto": ["nome", "nome completo", "nome_completo", "nomecompleto"],
    "email": ["email", "e-mail", "contato"],
    "cpf": ["cpf", "documento", "doc", "cpf_usuario"],
    "role": ["role", "tipo", "tipo_usuario", "perfil", "categoria", "função"],
    "dataNascimento": ["data_nascimento", "nascimento", "data de nascimento"]
}

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
    if not valor or not str(valor).strip():
        return None
    formatos = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"]
    for formato in formatos:
        try:
            data = datetime.strptime(str(valor).strip(), formato)
            return data.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None

def encontrar_coluna(df, campo_padrao, colunas_alternativas, colunas_usadas):
    for alt in colunas_alternativas:
        for coluna_df in df.columns:
            if coluna_df.lower().strip() not in colunas_usadas and \
               re.sub(r'\s+', '', coluna_df.strip().lower()) == re.sub(r'\s+', '', alt.strip().lower()):
                colunas_usadas.add(coluna_df.lower().strip())
                return coluna_df
    return None

def extrair_dados_de_sql(caminho_sql):
    with open(caminho_sql, "r", encoding="utf-8") as f:
        conteudo = f.read()
    matches = re.findall(r"INSERT INTO usuarios.*?VALUES\s*\((.*?)\);", conteudo, re.IGNORECASE)
    dados = []
    for match in matches:
        campos = [c.strip().strip("'") for c in re.findall(r"'(.*?)'", match)]
        if len(campos) == 4:
            dados.append({
                "nome do aluno": campos[0],
                "e-mail": campos[1],
                "cpf_usuario": campos[2],
                "tipo_usuario": campos[3]
            })
    return pd.DataFrame(dados)

def converter_arquivo_para_json(arquivo):
    extensao = os.path.splitext(arquivo)[1].lower()
    if extensao == ".csv":
        df = pd.read_csv(arquivo)
    elif extensao in [".xlsx", ".xls"]:
        df = pd.read_excel(arquivo)
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

    colunas_usadas = set()
    usuarios = []
    erros = []

    for _, row in df.iterrows():
        usuario = {}
        for campo_padrao, sinonimos in MAPEAMENTO_CAMPOS.items():
            coluna = encontrar_coluna(df, campo_padrao, sinonimos, colunas_usadas)
            if coluna:
                valor = str(row[coluna]).strip() if pd.notna(row[coluna]) else None
                if campo_padrao == "dataNascimento":
                    valor = normalizar_data_nascimento(valor)
                if campo_padrao == "role":
                    valor = normalizar_role(valor)
                usuario[campo_padrao] = valor

        if all(usuario.get(campo) for campo in ["nomeCompleto", "email", "cpf", "role", "dataNascimento"]):
            usuarios.append(usuario)
        else:
            erros.append(usuario)

    with open("usuarios_convertidos.json", "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=2, ensure_ascii=False)

    print(f"\n✅ {len(usuarios)} usuários convertidos com sucesso!")
    print(f"⚠️ {len(erros)} registros ignorados.")
    return {"usuarios": usuarios, "erros": erros}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❗ Uso: python converterArquivoAPI.py caminho/do/arquivo.csv|xlsx|json|sql")
    else:
        caminho_arquivo = sys.argv[1]
        try:
            resultado = converter_arquivo_para_json(caminho_arquivo)
        except Exception as e:
            print(f"❌ Erro ao processar arquivo: {e}")
