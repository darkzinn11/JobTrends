import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud


df = pd.read_csv('vagas_ti_limpo_realistas.csv')


df['Tecnologias'] = df['Tecnologias'].apply(eval) 
df['Benefícios'] = df['Benefícios'].apply(eval)


df['Salário'] = pd.to_numeric(df['Salário'], errors='coerce')  


todas_tecnologias = [tec for sublist in df['Tecnologias'] for tec in sublist]
contagem_tecnologias = Counter(todas_tecnologias).most_common(10)
tecs, counts = zip(*contagem_tecnologias)

plt.figure(figsize=(10, 6))
sns.barplot(x=list(counts), y=list(tecs))
plt.title('Top 10 Tecnologias Mais Exigidas')
plt.xlabel('Número de Vagas')
plt.ylabel('Tecnologia')
plt.tight_layout()
plt.savefig('top_tecnologias_realistas.png')
plt.show()


plt.figure(figsize=(10, 6))
df['Localização'].value_counts().head(10).plot(kind='bar')
plt.title('Distribuição de Vagas por Localização')
plt.xlabel('Cidade/Estado')
plt.ylabel('Número de Vagas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('distribuicao_localizacao_realistas.png')
plt.show()


plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='Nível', order=['Júnior', 'Pleno', 'Sênior'])
plt.title('Distribuição por Nível')
plt.xlabel('Nível')
plt.ylabel('Número de Vagas')
plt.tight_layout()
plt.savefig('distribuicao_nivel_realistas.png')
plt.show()


salarios = df[df['Salário'].notna()]['Salário']  
plt.figure(figsize=(10, 6))
sns.histplot(salarios, bins=20, kde=True)
plt.title('Distribuição Salarial')
plt.xlabel('Salário (R$)')
plt.ylabel('Frequência')
plt.tight_layout()
plt.savefig('distribuicao_salarial_realistas.png')
plt.show()


texto_tecnologias = ' '.join(todas_tecnologias)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto_tecnologias)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Nuvem de Palavras - Tecnologias')
plt.tight_layout()
plt.savefig('nuvem_tecnologias_realistas.png')
plt.show()


salarios_por_nivel = df[df['Salário'].notna()].groupby('Nível')['Salário'].mean().reindex(['Júnior', 'Pleno', 'Sênior'])
plt.figure(figsize=(8, 5))
salarios_por_nivel.plot(kind='bar')
plt.title('Salário Médio por Nível')
plt.xlabel('Nível')
plt.ylabel('Salário Médio (R$)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('salario_por_nivel_realistas.png')
plt.show()


todos_beneficios = [ben for sublist in df['Benefícios'] for ben in sublist]
contagem_beneficios = Counter(todos_beneficios).most_common(10)
bens, counts = zip(*contagem_beneficios)

plt.figure(figsize=(10, 6))
sns.barplot(x=list(counts), y=list(bens))
plt.title('Top 10 Benefícios Mais Oferecidos')
plt.xlabel('Número de Vagas')
plt.ylabel('Benefício')
plt.tight_layout()
plt.savefig('top_beneficios_realistas.png')
plt.show()