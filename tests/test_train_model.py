import os
import tempfile
import pandas as pd
import joblib
from train_model import main


def make_small_dataset(path):
    # Create a very small dataset
    df = pd.DataFrame({
        'text': [
            'this is real news about health',
            'fake news about a celebrity',
            'real report on economy',
            'fake rumor spread online'
        ],
        'label': ['REAL', 'FAKE', 'REAL', 'FAKE']
    })
    df.to_csv(path, index=False)


def test_train_creates_artifacts(tmp_path):
    # Create temporary CSV
    csv_path = tmp_path / 'small.csv'
    make_small_dataset(str(csv_path))

    # Run training pointing to the temp CSV
    cwd = os.getcwd()
    try:
        # Run in tmp_path so artifacts are created there
        os.chdir(tmp_path)
        main(str(csv_path))

        # Check artifacts
        assert os.path.exists(tmp_path / 'model.pkl')
        assert os.path.exists(tmp_path / 'vectorizer.pkl')

        # Optionally try loading them
        m = joblib.load(tmp_path / 'model.pkl')
        v = joblib.load(tmp_path / 'vectorizer.pkl')
        assert m is not None
        assert v is not None
    finally:
        os.chdir(cwd)
