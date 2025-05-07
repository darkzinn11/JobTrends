import pandas as pd
import numpy as np


df = pd.read_csv('vagas_ti_simuladas_realistas.csv')


print("Valores ausentes antes da limpeza:")
print(df.isnull().sum())


df['Salário'] = df['Salário'].fillna('Não informado')


df = df.drop_duplicates()


df['Tecnologias'] = df['Tecnologias'].str.title()
df['Benefícios'] = df['Benefícios'].str.title()


df['Tecnologias'] = df['Tecnologias'].apply(lambda x: x.split(', '))
df['Benefícios'] = df['Benefícios'].apply(lambda x: x.split(', '))


df['Localização'] = df['Localização'].replace({
    'Sao Paulo/Sp': 'São Paulo/SP', 'Rio De Janeiro/Rj': 'Rio de Janeiro/RJ',
    'Belo Horizonte/Mg': 'Belo Horizonte/MG', 'Sao Luis/Ma': 'São Luís/MA'
})


df.to_csv('vagas_ti_limpo_realistas.csv', index=False)
print("\nDataset limpo e salvo como 'vagas_ti_limpo_realistas.csv'!")
print("Valores ausentes após a limpeza:")
print(df.isnull().sum())