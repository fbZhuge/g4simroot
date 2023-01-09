import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import time

BATCH_SIZE = 7*7*256

# prepare data
# We have a list of water voxels of size 1000x10x10x10 of edeps

# (train_voxels, train_labels), (test_voxels, test_labels) = tf.keras.datasets.mnist.load_data()
train_voxels = train_voxels.reshape(train_voxels.shape[0], 10, 10, 10, 1).astype('float32')
# train_dataset = tf.data.Dataset.from_tensor_slices(train_voxels).shuffle(600).batch(100)

# train voxel shape [batchs, 10, 10, 10]
# load csv data
# convert the data into a tensor voxel

# the generator net
def create_generator():
    model = tf.keras.Sequential()
    # creating Dense layer with units 7*7*256(batch_size) and input_shape of (1000,)
    model.add(layers.Dense(7*7*256, use_bias=False, input_shape=(1000,)))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Reshape((7, 7, 256)))

    model.add(layers.Conv2DTranspose(128, (5, 5), strides=(1, 1), padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(64, (5, 5), strides=(2, 2), padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(1, (5, 5), strides=(2, 2), padding='same', use_bias=False, activation='tanh'))

    return model

# the discriminator net
def create_discriminator():
    model = tf.keras.Sequential()
    model.add(layers.Conv2D(64, (5, 5), strides=(2, 2), padding='same', input_shape=[10, 10, 10, 1]))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Conv2D(128, (5, 5), strides=(2, 2), padding='same'))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Flatten())
    model.add(layers.Dense(1))

    return model

# loss functions
cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)

def D_loss(real_output, fake_output):
    real_loss = cross_entropy(tf.ones_like(real_output), real_output)
    fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
    total_loss = real_loss + fake_loss
    return total_loss

def G_loss(fake_output):
    return cross_entropy(tf.ones_like(fake_output), fake_output)

# optimizer
generator_optimizer = tf.keras.optimizers.Adam(1e-4)
discriminator_optimizer = tf.keras.optimizers.Adam(1e-4)

noise_dim = 1000
num_of_generated_examples = 16

seed = tf.random.normal([num_of_generated_examples, noise_dim])

generator = create_generator()
discriminator = create_discriminator()

# the training loop
@tf.function
def train_step(images):
    noise = tf.random.normal([BATCH_SIZE, noise_dim])

    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
      generated_images = generator(noise, training=True)

      real_output = discriminator(images, training=True)
      fake_output = discriminator(generated_images, training=True)

      gen_loss = G_loss(fake_output)
      disc_loss = D_loss(real_output, fake_output)

    gradients_of_generator = gen_tape.gradient(gen_loss, generator.trainable_variables)
    gradients_of_discriminator = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

    generator_optimizer.apply_gradients(zip(gradients_of_generator, generator.trainable_variables))
    discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, discriminator.trainable_variables))

def train_GAN(dataset, epochs):
  for epoch in range(epochs):
    start = time.time()
    for image_batch in dataset:
      train_step(image_batch)
    print ('Time for epoch {} is {} sec'.format(epoch + 1, time.time()-start))

train_GAN(train_dataset, 500)
