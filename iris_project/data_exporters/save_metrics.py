import os

# Import Mage's decorators only if they aren't already loaded
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_exporter
def export_metrics(df, *args, **kwargs):
    df.to_csv('iris_metrics.csv', index=False)
    print('Saved', len(df), 'metrics to iris_metrics.csv')

@test
def test_metrics_file(output, *args):
    import pandas as pd
    assert os.path.exists('iris_metrics.csv'), 'iris_metrics.csv was not created'
    metrics = pd.read_csv('iris_metrics.csv')
    assert len(metrics) == 4, 'expected 4 metrics'
    assert metrics['value'].between(0, 1).all(), 'metrics must be between 0 and 1'
