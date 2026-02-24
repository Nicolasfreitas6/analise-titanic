import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =========================
#Carregando dados do CSV
# =========================
def carregar_dados(caminho):
    return pd.read_csv(caminho)

# =========================
#Visualização inicial da analise exploratória dos dados
# =========================
def visualizar_primeiras_linhas(df):
    print("\nPrimeiras linhas do dataset:")
    print(df.head())

def informacoes_gerais(df):
    print("\nInformações gerais e iniciais do dataset:")
    df.info()

def resumo_estatistico(df):
    print("\nResumo estatístico:")
    print(df.describe())

# =========================
#Analisando dados faltantes:
# =========================
def calcular_dados_faltantes(df):
    nulos = df.isnull().sum()
    percentual = (nulos / len(df))*100

    resultado = pd.DataFrame({
        "Valores Nulos": nulos,
        "Percentual (%)": percentual
    })

    return resultado[resultado["Valores Nulos"] > 0]

# =========================
#Verificando dados duplicados
# =========================
def verificar_duplicados(df):
    duplicados = df.duplicated().sum()
    print("\nQuantidade de registros duplicados:", duplicados)
    return duplicados

# =========================
#Gráfico de proporção de Cabin
# =========================
def grafico_cabin_nulos(df):
    dados = df["Cabin"].notnull().value_counts(normalize=True)*100
    dados_df = dados.reset_index()
    dados_df.columns = ["Tem_Cabine", "Percentual"]

    plt.figure(figsize=(8,5))
    sns.barplot(
        x="Tem_Cabine",
        y="Percentual",
        data=dados_df,
        palette="pastel"
    )
    plt.title("Proporção de Registros com Cabine")
    plt.ylabel("Percentual (%)")
    plt.savefig("outputs/proporcao_cabin.png")
    plt.close()
    
# =========================
#Tratando os dados nulos de Cabines
# =========================
def tratar_dados(df):
    #Criando variável binária de cabine
    df["Tem_cabine"] = df["Cabin"].notnull().astype(int)

    #Removendo coluna original Cabin
    df = df.drop(columns=["Cabin"])

    #Preencher Embarked com moda
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

    #Preencher Age por mediana por classe
    def preencher_mediana(grupo):
        return grupo.fillna(grupo.median())

    #Aplicando no Age
    df["Age"] = df.groupby("Pclass")["Age"].transform(preencher_mediana)

    return df

# =========================
#Realizando a tipagem de colunas
# =========================
def ajustar_tipos(df):
    df["Pclass"] = df["Pclass"].astype("category")
    df["Sex"] = df["Sex"].astype("category")
    df["Embarked"] = df["Embarked"].astype("category")

    return df

# =========================
#Criando faixas categoricas de idade
# =========================
def faixa_etaria(df):
    df["Faixa_Etaria"] = pd.cut(
        df["Age"],
        bins=[0,12,18,35,60,100],
        labels=["Criança","Adolescente","Adulto Jovem","Adulto","Idoso"]
    )
    return df

# =========================
#Visualização das análises
# =========================

#Gráfico de dados nulos
def grafico_dados_faltantes(df):
    os.makedirs("outputs", exist_ok=True)

    dados = calcular_dados_faltantes(df)
    dados = dados.sort_values(by="Percentual (%)", ascending=False)

    plt.figure(figsize=(8,5))
    sns.barplot(x=dados.index, y=dados["Percentual (%)"])
    plt.xlabel("")
    plt.title("Percentual de Valores Nulos por Coluna")
    plt.savefig("outputs/dados_faltantes.png")
    plt.close()

#Gráfico de distribuição de Embarked
def grafico_dados_embarked(df):
    os.makedirs("outputs", exist_ok=True)
    plt.figure(figsize=(8,5))
    sns.countplot(x="Embarked", data=df)
    plt.title("Distribuição de Porto de Embarque")
    plt.savefig("outputs/distribuicao_embarked.png")
    plt.close()

#Gráfico boxplot de idade para identificar outliers
def grafico_outliers_idade(df):
    os.makedirs("outputs", exist_ok=True)

    plt.figure(figsize=(6,4))
    sns.boxplot(x=df["Age"])
    plt.title("Boxplot de Idade")
    plt.xlabel("Idade")
    plt.savefig("outputs/boxplot_idade.png")
    plt.close()

#Gráfico de distribuição de idade
def grafico_idade(df):
    os.makedirs("outputs", exist_ok=True)
    plt.figure(figsize=(8,5))
    sns.histplot(df["Age"], bins=30, kde=True)
    plt.title("Distribuição de idade")
    plt.savefig("outputs/distribuicao_idade.png")
    plt.close()

# =========================
#EDA focado em análises dos sobreviventes
# =========================

#Sobreviventes por sexo
def sobreviventes_sexo(df):
    resultado = df.groupby("Sex")["Survived"].mean()*100
    print("\nTaxa de Sobrevivência por sexo:")
    print(resultado.round(2))

    return resultado

#Gráfico de sobreviventes por sexo
def grafico_sobrevivencia_sexo(resultado):
    os.makedirs("outputs", exist_ok=True)
    resultado_df = resultado.reset_index()
    plt.figure(figsize=(8, 5))
    sns.barplot(
        x="Sex",
        y="Survived",
        data=resultado_df,
        palette="pastel"
    )

    plt.title("Taxa de Sobrevivência por Sexo")
    plt.ylabel("Taxa de Sobrevivência (%)")
    plt.xlabel("Sexo")
    plt.savefig("outputs/sobrevivencia_por_sexo.png")
    plt.close()

#Sobreviventes por idade
def sobreviventes_idade(df):
    resultado_idade = df.groupby("Faixa_Etaria")["Survived"].mean()*100
    print("\nTaxa de sobrevivência por Faixa Etária (%):")
    print(resultado_idade.round(2))

    return resultado_idade

#Gráfico de sobreviventes por idade
def grafico_sobreviventes_idade(resultado):
    os.makedirs("outputs", exist_ok=True)
    resultado_df = resultado.reset_index()

    plt.figure(figsize=(8,5))
    sns.barplot(
        x="Faixa_Etaria",
        y="Survived",
        data=resultado_df,
        palette="deep"
    )
    plt.title("Distribuição de idade dos sobreviventes")
    plt.ylabel("Taxa de Sobrevivência (%)")
    plt.xlabel("Faixa Etária")
    plt.savefig("outputs/distribuicao_idade_sobreviventes.png")
    plt.close()

#Sobreviventes por Classe
def sobreviventes_classe(df):
    resultado_classe = df.groupby("Pclass")["Survived"].mean()*100
    print("\nTaxa de Sobrevivência por classe:")
    print(resultado_classe.round(2))

    return resultado_classe

#Gráfico de sobreviventes por Classe
def grafico_sobreviventes_classe(resultado):
    os.makedirs("outputs", exist_ok=True)
    resultado_df = resultado.reset_index()
    plt.figure(figsize=(8,5))

    sns.barplot(
        x="Pclass",
        y="Survived",
        data=resultado_df,
        palette="crest"
    )

    plt.title("Taxa de Sobrevivência por Classe")
    plt.ylabel("Taxa de Sobrevivência (%)")
    plt.xlabel("Classe")
    plt.savefig("outputs/sobrevivencia_por_classe.png")
    plt.close()

#Sobreviventes por Fare por Quartil
def sobreviventes_fare(df):
    df["Fare_Quartil"] = pd.qcut(
        df["Fare"],
        4,
        labels=["Q1 - Mais Barato", "Q2", "Q3", "Q4 - Mais Caro"],
        duplicates="drop"
    )

    resultado_fare = df.groupby("Fare_Quartil")["Survived"].mean()*100
    print("\nTaxa de Sobrevivência por Quartil de Preço Pago:")
    print(resultado_fare.round(2))

    return resultado_fare

#Gráfico de sobreviventes por Fare
def grafico_sobreviventes_fare(resultado):
    os.makedirs("outputs", exist_ok=True)
    resultado_df = resultado.reset_index()

    plt.figure(figsize=(8,5))
    sns.barplot(
        x="Fare_Quartil",
        y="Survived",
        data=resultado_df,
        palette="magma"
    )
    
    plt.title("Taxa de Sobrevivência por Quartil de Preço")
    plt.ylabel("Taxa de Sobrevivência (%)")
    plt.xlabel("Quartil de Preço")
    plt.savefig("outputs/sobrevivencia_por_fare.png")
    plt.close()

#Correlação entre Fare e Classe
def fare_por_classe(df):
    resultado_fare_classe = df.groupby("Pclass")["Fare"].mean()

    print("\nMédia de Preço por Classe:")
    print(resultado_fare_classe.round(2))

    return resultado_fare_classe

#Heatmap de correlação entre Fare e Classe
def grafico_media_fare_classe(resultado):
    os.makedirs("outputs", exist_ok=True)
    tabela = resultado.to_frame()

    plt.figure(figsize=(8,5))
    sns.heatmap(
        tabela,
        annot=True,
        fmt=".2f",
        cmap="YlGnBu"
    )

    plt.title("Média de Preços por Classe")
    plt.ylabel("Classe")
    plt.xlabel("")
    plt.savefig("outputs/heatmap_media_fare_classe.png")
    plt.close()

#Sobreviventes por Embarked
def sobreviventes_embarked(df):
    resultado_embarked = df.groupby("Embarked")["Survived"].mean()*100
    print("\nTaxa de Sobrevivência por Embarcação:")
    print(resultado_embarked.round(2))

    return resultado_embarked

#Gráfico de sobreviventes por Embarked
def grafico_sobreviventes_embarked(resultado):
    os.makedirs("outputs", exist_ok=True)
    resultado_df = resultado.reset_index()
    plt.figure(figsize=(8,5))

    sns.barplot(
        x="Embarked",
        y="Survived",
        data=resultado_df,
        palette="crest"
    )

    plt.title("Taxa de Sobrevivência por Embarcação")
    plt.ylabel("Taxa de Sobrevivência (%)")
    plt.xlabel("Embarcação")
    plt.savefig("outputs/sobrevivencia_por_embarked.png")
    plt.close()

#Sobreviventes por Classe e Embarked
def distribuicao_embarked_classe(df):
    tabela = (
        df.groupby(["Embarked", "Pclass"])
          .size()
          .unstack()
    )

    tabela_percentual = tabela.div(tabela.sum(axis=1), axis=0) * 100

    print("\nDistribuição Percentual de Classe por Porto de Embarque:")
    print(tabela_percentual.round(2))

    return tabela_percentual

#Gráfico de Classe e Embarked
def grafico_embarked_classe_heatmap(tabela_percentual):
    os.makedirs("outputs", exist_ok=True)

    plt.figure(figsize=(8,5))
    sns.heatmap(
        tabela_percentual,
        annot=True,
        fmt=".1f",
        cmap="YlGnBu"
    )

    plt.title("Distribuição Percentual de Classe\npor Porto de Embarque")
    plt.ylabel("Porto de Embarque")
    plt.xlabel("Classe")
    plt.savefig("outputs/heatmap_embarked_classe.png")
    plt.close()

#Sobreviventes por classe e sexo
def sobreviventes_sexo_classe(df):
    resultado_sexo_classe = df.groupby(["Pclass", "Sex"])["Survived"].mean()*100
    print("\nTaxa de Sobrevivência por classe e sexo:")
    print(resultado_sexo_classe.round(2))

    return resultado_sexo_classe

#Heatmap do cruzamento de classe e sexo
def grafico_classe_sexo_heatmap(df):
    os.makedirs("outputs", exist_ok=True)
    tabela = df.groupby(["Pclass", "Sex"])["Survived"].mean().unstack()*100

    plt.figure(figsize=(6,4))
    sns.heatmap(
        tabela,
        annot=True,
        fmt=".1f",
        cmap="YlGnBu"
    )

    plt.title("Taxa de Sobrevivência (%)\nClasse x Sexo")
    plt.ylabel("Classe")
    plt.xlabel("Sexo")
    plt.savefig("outputs/heatmap_classe_sexo.png")
    plt.close()

#Sobreviventes por Classe e Faixa Etária
def sobreviventes_classe_idade(df):
    resultado_classe_idade = df.groupby(["Pclass", "Faixa_Etaria"])["Survived"].mean()*100
    print("\nTaxa de Sobrevivência por Classe e Faixa Etária")
    print(resultado_classe_idade.round(2))

    return resultado_classe_idade

#Heatmap do cruzamento de Classe e Faixa Etaria
def grafico_classe_idade_heatmap(df):
    os.makedirs("outputs", exist_ok=True)
    tabela = df.groupby(["Pclass", "Faixa_Etaria"])["Survived"].mean().unstack()*100

    plt.figure(figsize=(8,5))
    sns.heatmap(
        tabela,
        annot=True,
        fmt=".1f",
        cmap="YlGnBu"
    )

    plt.title("Taxa de Sobrevivência (%)\nClasse x Faixa_Etaria")
    plt.ylabel("Classe")
    plt.xlabel("Faixa_Etaria")
    plt.savefig("outputs/heatmap_classe_idade.png")
    plt.close()

#Sobreviventes por sexo e idade
def sobreviventes_sexo_idade(df):
    resultado_sexo_idade = df.groupby(["Sex", "Faixa_Etaria"])["Survived"].mean()*100
    print("\nTaxa de Sobrevivência por Sexo e Faixa Etária")
    print(resultado_sexo_idade.round(2))

    return resultado_sexo_idade

#Heatmap do cruzamento de Sexo e Faixa Etaria
def grafico_sexo_idade_heatmap(df):
    os.makedirs("outputs", exist_ok=True)
    tabela = df.groupby(["Sex", "Faixa_Etaria"])["Survived"].mean().unstack()*100

    plt.figure(figsize=(8,5))
    sns.heatmap(
        tabela,
        annot=True,
        fmt=".1f",
        cmap="YlGnBu"
    )

    plt.title("Taxa de Sobrevivência (%)\nSexo x Faixa_Etaria")
    plt.ylabel("Sexo")
    plt.xlabel("Faixa_Etaria")
    plt.savefig("outputs/heatmap_sexo_idade.png")
    plt.close()

#Função principal/main para o restante
def main():
    caminho = "data/titanic_dataset.csv"
    
    # =========================
    # Carregando o CSV
    # =========================
    df = carregar_dados(caminho)

    # =========================
    # Conhecendo o dataset
    # =========================
    visualizar_primeiras_linhas(df)
    informacoes_gerais(df)
    resumo_estatistico(df)

    # =========================
    # Encontrando nulos
    # =========================
    print("\nDados faltantes por coluna:")
    print(calcular_dados_faltantes(df))

    verificar_duplicados(df)
    grafico_cabin_nulos(df)

    # =========================
    # Tratando dados
    # =========================
    df = tratar_dados(df)
    df = faixa_etaria(df)

    print("\nDados faltantes após tratamento:")
    print(calcular_dados_faltantes(df))

    # =========================
    # Ajustando tipagem dos dados
    # =========================
    df = ajustar_tipos(df)

    # =========================
    # Garantindo a criação da pasta, caso necessário
    # =========================
    os.makedirs("outputs", exist_ok=True)

    # =========================
    # EDA Inicial
    # =========================
    grafico_dados_faltantes(df)
    grafico_dados_embarked(df)
    grafico_idade(df)
    grafico_outliers_idade(df)

    # =========================
    # EDA com Survived
    # =========================

    # Sexo
    resultado_sexo = sobreviventes_sexo(df)
    grafico_sobrevivencia_sexo(resultado_sexo)

    # Faixa Etária
    resultado_idade = sobreviventes_idade(df)
    grafico_sobreviventes_idade(resultado_idade)

    # Classe
    resultado_classe = sobreviventes_classe(df)
    grafico_sobreviventes_classe(resultado_classe)

    # Fare + Classe
    resultado_fare_classe = fare_por_classe(df)
    grafico_media_fare_classe(resultado_fare_classe)

    # Embarked
    resultado_embarked = sobreviventes_embarked(df)
    grafico_sobreviventes_embarked(resultado_embarked)

    # Fare
    resultado_fare = sobreviventes_fare(df)
    grafico_sobreviventes_fare(resultado_fare)

    # Embarked + Classe
    tabela_embarked_classe = distribuicao_embarked_classe(df)
    grafico_embarked_classe_heatmap(tabela_embarked_classe)

    # Classe + Sexo
    sobreviventes_sexo_classe(df)
    grafico_classe_sexo_heatmap(df)

    # Classe + Faixa Etária
    sobreviventes_classe_idade(df)
    grafico_classe_idade_heatmap(df)

    # Sexo + Faixa Etária
    sobreviventes_sexo_idade(df)
    grafico_sexo_idade_heatmap(df)

if __name__ == "__main__":
    main()