import pandas as pd

# Load both datasets
fake = pd.read_csv('Fake.csv')
true = pd.read_csv('True.csv')

# Add labels
fake['label'] = 'FAKE'
true['label'] = 'REAL'

# Combine and shuffle
df = pd.concat([fake, true])
df = df[['text', 'label']].dropna()
df = df.sample(frac=1).reset_index(drop=True)

# Save as news.csv
df.to_csv('news.csv', index=False)
print("news.csv created successfully!")