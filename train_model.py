import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score
import joblib


def main(dataset_path: str = 'news.csv'):
	# Verify dataset exists
	if not os.path.exists(dataset_path):
		print(f"Dataset not found: {dataset_path}")
		print("Run prepare_dataset.py first to create 'news.csv', or pass the correct path.")
		sys.exit(1)

	# Load dataset
	df = pd.read_csv(dataset_path)
	if 'text' not in df.columns or 'label' not in df.columns:
		print(f"Dataset {dataset_path} must contain 'text' and 'label' columns")
		sys.exit(1)

	df = df[['text', 'label']].dropna()

	# Vectorize text (use built-in english stop words so nltk download isn't required)
	vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
	X = vectorizer.fit_transform(df['text'])
	y = df['label']

	# Train/test split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

	# Train model
	model = PassiveAggressiveClassifier(random_state=42, max_iter=1000)
	model.fit(X_train, y_train)

	# Evaluate
	acc = accuracy_score(y_test, model.predict(X_test))
	print("Accuracy:", acc)

	# Save model and vectorizer
	joblib.dump(model, 'model.pkl')
	joblib.dump(vectorizer, 'vectorizer.pkl')
	print("Saved model and vectorizer to:", os.getcwd())


if __name__ == '__main__':
	# Allow optional dataset path as first CLI argument
	# Default to 'merged-csv-files.csv' (user-provided), fall back to 'news.csv'
	dataset = sys.argv[1] if len(sys.argv) > 1 else 'merged-csv-files.csv'
	if not os.path.exists(dataset) and os.path.exists('news.csv'):
		dataset = 'news.csv'
	main(dataset)