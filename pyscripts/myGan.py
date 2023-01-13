import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import time
import csv

BATCH_SIZE = 7*7*256

NbVoxelsPerAxe=10  # from 1 to 99, it must much numberOfDetectors in construction.cc in Geant4
water_voxel=np.zeros(shape=(NbVoxelsPerAxe,NbVoxelsPerAxe,NbVoxelsPerAxe),dtype=np.double)

def coordinates_from_chamber_nb(chamber_number, vox_per_axis):
    chamber_number=int(row[0])
    if(vox_per_axis<=9):
        i=chamber_number%10
        j=((chamber_number-i)//10)%10
        k=(((chamber_number-i)//10) - j)//10
        return (i,j,k)
    elif(10<=vox_per_axis<=99):
        i=chamber_number%100
        j=((chamber_number-i)//100)%100
        k=(((chamber_number-i)//100) - j)//100
        return (i,j,k)
    else:
        i=chamber_number%1000
        j=((chamber_number-i)//1000)%1000
        k=(((chamber_number-i)//1000) - j)//1000
        return (i,j,k)

def chamber_nb_from_coordinates(i, j, k, vox_per_axis):
    if(vox_per_axis<=9):
        return i+10*j+100*k
    elif(10<=vox_per_axis<=99):
        return i+100*j+10000*k
    else:
        return i+1000*j+1000000*k

# open the csv log file and stor the edp in each voxel in a tensor
# filename='/home/omoikane/github/research/g4simRoot/build/hits_csv.csv'
# with open(filename, newline='') as csvfile:
#     f = csv.reader(csvfile)
#     for row in f:
#         chamberNb=int(row[0])
#         edep=np.double(row[1])
#         i,j,k=coordinates_from_chamber_nb(chamberNb, NbVoxelsPerAxe)
#         water_voxel[i,j,k]+=edep

# train_voxels = tf.stack(water_voxel,water_voxel,water_voxel)

# print(train_voxels.shape)
# train_voxels = train_voxels.reshape(train_voxels.shape[0], 10, 10, 10, 1).astype('float32')
# train_dataset = tf.data.Dataset.from_tensor_slices(train_voxels).shuffle(600).batch(100)


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

noise_dim = 10*10*10

generator = create_generator()
generator.summary()
discriminator = create_discriminator()
discriminator.summary()

# the training loop
@tf.function
def train_step(real_samples):
    noise = tf.random.normal([BATCH_SIZE, noise_dim])

    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
      generated_samples = generator(noise, training=True)
      real_output = discriminator(real_samples, training=True)
      fake_output = discriminator(generated_samples, training=True)
      gen_loss = G_loss(fake_output)
      disc_loss = D_loss(real_output, fake_output)

    gradients_of_generator = gen_tape.gradient(gen_loss, generator.trainable_variables)
    gradients_of_discriminator = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

    generator_optimizer.apply_gradients(zip(gradients_of_generator, generator.trainable_variables))
    discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, discriminator.trainable_variables))

def train_GAN(dataset, epochs):
  for epoch in range(epochs):
    start = time.time()
    for sample_batch in dataset:
      train_step(sample_batch)
    print ('Time for epoch {} is {} sec'.format(epoch + 1, time.time()-start))

# train_GAN(train_dataset, 500)
