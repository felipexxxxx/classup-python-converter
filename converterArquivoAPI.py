import pandas as pd
import json
import re
import os
from datetime import datetime

MAPEAMENTO_CAMPOS = {
    "nomeCompleto": ["nome", "nome completo", "nome_completo", "nomecompleto", "nome do aluno"],
    "email": ["email", "e-mail", "contato"],
    "cpf": ["cpf", "documento", "doc", "cpf_usuario"],
    "role": ["role", "tipo", "tipo_usuario", "perfil", "categoria", "função"],
    "dataNascimento": ["data_nascimento", "nascimento", "data de nascimento", "dt_nascimento", "dn"]
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
    formatos = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d", "%d/%m/%y", "%d-%m-%y"]
    for formato in formatos:
        try:
            data = datetime.strptime(str(valor).strip(), formato)
            return data.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None

def encontrar_coluna(df, campo_padrao, sinonimos):
    for alt in sinonimos:
        for coluna_df in df.columns:
            comparacao = re.sub(r'\s+', '', coluna_df.strip().lower()) == re.sub(r'\s+', '', alt.strip().lower())
            if comparacao:
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
        else:
            print(f"⚠️ Ignorado: {campos} (esperado 5 campos)")

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

    usuarios = []
    erros = []

    for _, row in df.iterrows():
        usuario = {}
        for campo_padrao, sinonimos in MAPEAMENTO_CAMPOS.items():
            coluna = encontrar_coluna(df, campo_padrao, sinonimos)
            if coluna:
                valor = str(row[coluna]).strip() if pd.notna(row[coluna]) else None
                if campo_padrao == "dataNascimento":
                    valor = normalizar_data_nascimento(valor)
                elif campo_padrao == "role":
                    valor = normalizar_role(valor)
                usuario[campo_padrao] = valor

        if all(usuario.get(campo) for campo in ["nomeCompleto", "email", "cpf", "role", "dataNascimento"]):
            usuarios.append(usuario)
        else:
            motivos = []
            for campo in ["nomeCompleto", "email", "cpf", "role", "dataNascimento"]:
                if not usuario.get(campo):
                    motivos.append(f"Campo '{campo}' ausente ou inválido")
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
        resultado = converter_arquivo_para_json(sys.argv[1])
        print("Resultado:", resultado)
