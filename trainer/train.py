import argparse
import os
import tensorflow as tf
import tensorflow_datasets as tfds
from . import gce


parser = argparse.ArgumentParser()
parser.add_argument("--output_dir", type=str, default="outputs")
parser.add_argument("--batch_size", type=int, default=64)
parser.add_argument("--epochs", type=int, required=True)

args, unknown_args = parser.parse_known_args()

BATCH_SIZE = args.batch_size
EPOCHS = args.epochs
OUTPUT_DIR = args.output_dir


def train_dataset():

    ds = tfds.load('mnist', split=tfds.Split.TRAIN)
    ds = ds.map(lambda x: (tf.cast(x['image'], tf.float32)/255., x['label']))
    ds = ds.repeat().shuffle(1024).batch(BATCH_SIZE)
    ds = ds.prefetch(tf.data.experimental.AUTOTUNE)

    return ds


def eval_dataset():

    ds = tfds.load('mnist', split=tfds.Split.TEST)
    ds = ds.map(lambda x: (tf.cast(x['image'], tf.float32)/255., x['label']))
    ds = ds.repeat().batch(BATCH_SIZE)
    ds = ds.prefetch(tf.data.experimental.AUTOTUNE)

    return ds


def create_model():

    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPool2D(pool_size=(2, 2)),
        tf.keras.layers.Dropout(rate=0.5),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(rate=0.5),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    return model


def main():

    model = create_model()
    model.compile(
        optimizer=tf.keras.optimizers.SGD(lr=0.01, nesterov=True),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    ds_train = train_dataset()
    ds_eval = eval_dataset()

    checkpoint_dir = os.path.join(OUTPUT_DIR, 'checkpoints')
    savedmodel_dir = os.path.join(OUTPUT_DIR, 'models/model-epoch-{epoch:03d}')
    tensorboard_dir = os.path.join(OUTPUT_DIR, 'tensorboard')
    checkpoint_name = 'checkpoint-{epoch:03d}'

    # Callbacks
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=os.path.join(checkpoint_dir, checkpoint_name),
        verbose=1,
        save_weights_only=True,
        save_best_only=False,
        # period=1,
        save_freq='epoch',
    )
    savedmodel_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=savedmodel_dir,
        verbose=1,
        save_weights_only=False,
        save_best_only=True,
        # period=1,
        save_freq='epoch',
    )
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=tensorboard_dir)

    # Resume training from latest checkpoint
    latest_checkpoint = tf.train.latest_checkpoint(checkpoint_dir)
    if latest_checkpoint:
        model.load_weights(latest_checkpoint)
        initial_epoch = int(latest_checkpoint.split('.')[0].split('-')[-1])
    else:
        initial_epoch = 0

    model.fit(
        ds_train,
        epochs=EPOCHS,
        steps_per_epoch=int(60000/BATCH_SIZE),
        validation_data=ds_eval,
        validation_steps=100,
        callbacks=[
            checkpoint_callback,
            savedmodel_callback,
            tensorboard_callback,
        ],
        initial_epoch=initial_epoch,
    )

    # Make instance group size zero
    gce.self_resize_instance_group(0)


if __name__ == '__main__':
    main()
