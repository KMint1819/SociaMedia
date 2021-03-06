
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow import keras
import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from datetime import datetime
import shutil
import os
# Suppress extra logs from tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
# tf.config.set_visible_devices([], 'GPU')

from models.util import SyncTool

################### Hyperparameters ###################
MAX_BAG = 13000
MAX_LEN = 512
TRAIN_RATIO = 0.9
BATCH_SIZE = 128
EPOCHS = 25
DATASET_DIR = Path.cwd().parent / 'data' / 'hw2' / 'smm-hw2-fakenewsdetecion'
#######################################################


def get_network():
    net = keras.Sequential()
    net.add(keras.layers.Embedding(MAX_BAG, 128))
    # net.add(keras.layers.Conv1D(128, 5, padding='same', activation=tf.nn.relu))
    # net.add(keras.layers.Conv1D(128, 5, padding='same',activation=tf.nn.relu))
    net.add(keras.layers.GlobalAveragePooling1D())
    net.add(keras.layers.Dense(128, activation=tf.nn.relu))
    net.add(keras.layers.Dense(64, activation=tf.nn.relu))
    net.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))
    net.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['acc']
    )
    return net


def main():
    start_time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    save_dir = Path.cwd() / 'models' / start_time
    save_dir.mkdir(parents=True)

    # Get data numbers
    df = pd.read_csv(DATASET_DIR / 'train.csv').fillna(np.nan)
    df['text'].replace('', np.nan, inplace=True)
    df.dropna(subset=['text'], inplace=True)
    n_data = df.shape[0]
    n_train = int(n_data * TRAIN_RATIO)
    n_val = n_data - n_train
    print(f'Total number of data: {n_data}. Num of train and val: {n_train}, {n_val}')

    # Tokenize
    tokenizer = Tokenizer(num_words=MAX_BAG, oov_token="<OOB>")
    tokenizer.fit_on_texts(df['text'])
    print('Finished fitting text to tokenizer.')
    tokenizer.word_index['<PAD>'] = 0
    tokenizer_save_path = save_dir / 'tokenizer.pickle'
    with tokenizer_save_path.open('wb') as f:
        pickle.dump(tokenizer, f)

    # Text to sequence and padding
    sequences = np.array(tokenizer.texts_to_sequences(df['text']))  # Sequences
    sequences = np.array(pad_sequences(
        sequences,
        value=tokenizer.word_index['<PAD>'],
        padding='pre',
        maxlen=MAX_LEN
    ))
    print('Finished padding')

    # Split train, val
    train_data = sequences[:n_train]
    train_label = np.array(df['label'][:n_train].tolist())
    val_data = sequences[n_train:]
    val_label = np.array(df['label'][n_train:].tolist())

    # Save path
    save_prefix = save_dir / f'{start_time}'
    save_callback = keras.callbacks.ModelCheckpoint(
        str(save_dir / ('{val_acc:.3f}-{epoch:02d}_' + start_time + '.hdf5')))

    #
    print('Start training...')
    net = get_network()
    history = net.fit(
        train_data,
        train_label,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_data=(val_data, val_label),
        callbacks=[save_callback],
        verbose=1
    )

    # Get best prefix
    m = 0
    best_name = None
    for p in save_dir.iterdir():
        if p.suffix != '.hdf5':
            continue
        score = float(str(p.stem).split('-')[0])
        if score > m:
            m > score
            best_name = str(p.stem)
    shutil.move(save_dir, save_dir.parent / best_name)
    SyncTool.execute('models/')

if __name__ == "__main__":
    main()
