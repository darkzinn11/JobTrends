import pandas as pd
import numpy as np
import random
from faker import Faker


fake = Faker('pt_BR')


cargos = [
    'Desenvolvedor Full Stack', 'Desenvolvedor Backend', 'Desenvolvedor Frontend',
    'Analista de Dados', 'Cientista de Dados', 'Engenheiro de Software',
    'DevOps', 'Desenvolvedor Mobile', 'Analista de Sistemas', 'Engenheiro de Machine Learning'
]
cargo_pesos = [0.25, 0.20, 0.15, 0.15, 0.10, 0.05, 0.05, 0.03, 0.01, 0.01]

cargo_pesos = np.array(cargo_pesos) / np.sum(cargo_pesos)

niveis = ['Júnior', 'Pleno', 'Sênior']
nivel_pesos = [0.35, 0.40, 0.25]

nivel_pesos = np.array(nivel_pesos) / np.sum(nivel_pesos)

tecnologias = [
    'Python', 'JavaScript', 'SQL', 'Java', 'TypeScript', 'React', 'Node.js',
    'AWS', 'Docker', 'PostgreSQL', 'MongoDB', 'Django', 'Spring', 'Angular',
    'C#', '.NET', 'Git', 'Kubernetes', 'Flask', 'Vue.js', 'Linux', 'Terraform'
]
tecnologia_pesos = [0.15, 0.12, 0.10, 0.08, 0.07, 0.07, 0.06, 0.05, 0.05, 0.04,
                    0.04, 0.03, 0.03, 0.03, 0.02, 0.02, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01]

tecnologia_pesos = np.array(tecnologia_pesos) / np.sum(tecnologia_pesos)

cidades = [
    'São Paulo/SP', 'Remoto', 'Rio de Janeiro/RJ', 'Belo Horizonte/MG',
    'Curitiba/PR', 'Porto Alegre/RS', 'Recife/PE', 'Florianópolis/SC',
    'Salvador/BA', 'Brasília/DF', 'São Luís/MA'
]
cidade_pesos = [0.40, 0.25, 0.15, 0.08, 0.05, 0.03, 0.02, 0.01, 0.01, 0.01, 0.01]

cidade_pesos = np.array(cidade_pesos) / np.sum(cidade_pesos)

beneficios = [
    'Plano de saúde', 'Vale-refeição', 'Vale-transporte', 'Home office',
    'Plano odontológico', 'Horário flexível', 'Bônus anual', 'Gympass',
    'Auxílio-creche', 'Cursos e certificações'
]
beneficio_pesos = [0.25, 0.25, 0.20, 0.15, 0.05, 0.05, 0.02, 0.01, 0.01, 0.01]

beneficio_pesos = np.array(beneficio_pesos) / np.sum(beneficio_pesos)


def gerar_tecnologias():
    return np.random.choice(tecnologias, size=random.randint(2, 5), replace=False, p=tecnologia_pesos)


def gerar_beneficios():
    return np.random.choice(beneficios, size=random.randint(1, 4), replace=False, p=beneficio_pesos)


def gerar_salario(nivel):
    if random.random() < 0.7:  
        return None
    if nivel == 'Júnior':
        return round(random.uniform(3000, 6000), 2)
    elif nivel == 'Pleno':
        return round(random.uniform(6000, 10000), 2)
    else:  # Sênior
        return round(random.uniform(10000, 18000), 2)


n_vagas = 500
dados = {
    'Título': np.random.choice(cargos, size=n_vagas, p=cargo_pesos),
    'Empresa': [fake.company() for _ in range(n_vagas)],
    'Localização': np.random.choice(cidades, size=n_vagas, p=cidade_pesos),
    'Nível': np.random.choice(niveis, size=n_vagas, p=nivel_pesos),
    'Tecnologias': [', '.join(gerar_tecnologias()) for _ in range(n_vagas)],
    'Salário': [gerar_salario(nivel) for nivel in np.random.choice(niveis, size=n_vagas, p=nivel_pesos)],
    'Benefícios': [', '.join(gerar_beneficios()) for _ in range(n_vagas)]
}


df = pd.DataFrame(dados)


df.to_csv('vagas_ti_simuladas_realistas.csv', index=False)
print("Dataset realista gerado e salvo como 'vagas_ti_simuladas_realistas.csv'!")