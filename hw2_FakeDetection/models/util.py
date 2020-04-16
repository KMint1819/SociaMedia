'''Sync the models directory
1. Copy the best model to models/
2. Rename new-trained directories to name validation accuracy first
'''
from pathlib import Path
import shutil


class SyncTool(object):
    def __init__(self):
        pass

    @staticmethod
    def execute(models_dir):
        models_dir = Path(models_dir)
        assert models_dir.is_dir(), f'{str(models_dir)} does not exist!'

        m = {'value': 999., 'path': '', 'tokenizer': ''}

        for p in models_dir.glob('*/*.hdf5'):
            loss = float(str(p.stem.split('-')[0]))
            if loss < m['value']:
                m['value']=loss
                m['path']=p
                m['tokenizer']=p.parent / 'tokenizer.pickle'
        shutil.copy2(m['path'], models_dir / 'best.hdf5')
        shutil.copy2(m['tokenizer'], models_dir / 'best_tokenizer.pickle')

if __name__ == "__main__":
    SyncTool.execute('.')
