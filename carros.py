#   Integrantes:
#   Arthur Bezerra
#   Danilo Pinheiro

import pandas as pd
import matplotlib.pyplot as plt

# Ler o arquivo CSV
data = pd.read_csv('used_car_dataset.csv')

# Pré-processamento dos dados

## 1. Remover espaços em branco das colunas
data.columns = data.columns.str.strip()

## 2. Converter "AskPrice" para um valor numérico
data['AskPrice'] = data['AskPrice'].str.replace(r'[₹,]', '', regex=True).str.strip()
data['AskPrice'] = pd.to_numeric(data['AskPrice'], errors='coerce')  # Converter para numérico
data = data.dropna(subset=['AskPrice'])  # Remover valores NaN gerados por erros de conversão
data['AskPrice'] = data['AskPrice'].astype(float)  # Garantir que esteja no formato float

## 3. Tratar a coluna "kmDriven"
data['kmDriven'] = data['kmDriven'].str.replace(r'[^\d]', '', regex=True).str.strip()
data['kmDriven'] = pd.to_numeric(data['kmDriven'], errors='coerce')  # Converter para numérico
data = data.dropna(subset=['kmDriven'])  # Remover valores NaN
data['kmDriven'] = data['kmDriven'].astype(int)

## 4. Verificar valores duplicados e removê-los, se houver
data = data.drop_duplicates()

## 5. Normalizar colunas categóricas
data['Brand'] = data['Brand'].str.strip()
data['model'] = data['model'].str.strip()
data['FuelType'] = data['FuelType'].str.strip()
data['Transmission'] = data['Transmission'].str.strip()

# Análises e insights

## 1. Média de preços por marca
avg_price_by_brand = data.groupby('Brand')['AskPrice'].mean().sort_values(ascending=False)
print("Média de preços por marca:\n", avg_price_by_brand)

## 2. Contagem de carros por tipo de combustível
fuel_type_counts = data['FuelType'].value_counts()
print("\nContagem de carros por tipo de combustível:\n", fuel_type_counts)

## 3. Relação entre preço e quilometragem (kmDriven)
print("\nCorrelação entre preço e quilometragem (kmDriven):")
print(data[['AskPrice', 'kmDriven']].corr())

# Visualizações

## 1. Gráfico de barras: Preço médio por marca
plt.figure(figsize=(10, 6))
avg_price_by_brand.plot(kind='bar', color='skyblue')
plt.title('Preço médio por marca', fontsize=16)
plt.xlabel('Marca', fontsize=14)
plt.ylabel('Preço médio (₹)', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

## 2. Gráfico de pizza: Distribuição de carros por tipo de combustível
plt.figure(figsize=(8, 8))
fuel_type_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['lightblue', 'lightgreen', 'coral', 'gold'])
plt.title('Distribuição de carros por tipo de combustível', fontsize=16)
plt.ylabel('')  # Remove o rótulo do eixo Y
plt.tight_layout()
plt.show()

## 3. Dispersão: Relação entre preço e quilometragem
plt.figure(figsize=(10, 6))
plt.scatter(data['kmDriven'], data['AskPrice'], alpha=0.7, color='purple')
plt.title('Relação entre preço e quilometragem', fontsize=16)
plt.xlabel('Quilometragem (km)', fontsize=14)
plt.ylabel('Preço (₹)', fontsize=14)
plt.grid(alpha=0.5)
plt.tight_layout()
plt.show()

# Exportar dados tratados para um novo arquivo CSV
data.to_csv('car_dataset_cleaned.csv', index=False)

print("\nAnálises concluídas. Dados tratados salvos em 'car_dataset_cleaned.csv'.")
