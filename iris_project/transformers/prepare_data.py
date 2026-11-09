import pandas as pd
from sklearn.model_selection import train_test_split

try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    def transformer(f):
        return f

    def test(f):
        return f


@transformer
def transform(df, *args, **kwargs):
    train, test_df = train_test_split(
        df, test_size=0.3, random_state=42, stratify=df["target"]
    )
    train, test_df = train.copy(), test_df.copy()
    train["split"] = "train"
    test_df["split"] = "test"
    return pd.concat([train, test_df])


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
    assert set(output["split"]) == {"train", "test"}