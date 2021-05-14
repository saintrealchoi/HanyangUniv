import tensorflow as tf
import numpy as np
import random
from sklearn.metrics import f1_score

# ADAM optimizer
LR = 0.001
BETA1= 0.9
BETA2= 0.999
EPSILON = 1e-08

# Batch Normalization
batch_prob = tf.placeholder(tf.bool)
BATCH_PROB = True

# Dropout
keep_prob = tf.placeholder(tf.float32)
KEEP_PROB = 0.75

training_epochs = 200
batch_size = 128

"""# for data augmentation"""

# x_train = np.load("/content/drive/MyDrive/Colab Notebooks/assignment/image classification/data/x_train.npy")
# y_train = np.load("/content/drive/MyDrive/Colab Notebooks/assignment/image classification/data/y_train.npy")

# def flip_image_tf(X):
#     X_img = tf.placeholder(dtype=tf.float32, shape=(32, 32, 3), name='X')
    
#     tf_flip = tf.image.random_flip_up_down(X_img)
#     tf_flip = tf.image.random_flip_left_right(tf_flip)
#     tf_flip = tf.image.rot90(tf_flip, tf.random_uniform(shape=[], minval=0, maxval=4, dtype=tf.int32))

#     tf.global_variables_initializer()
#     sess = tf.Session()
#     X_flip = []
#     for i in range(len(X)):
#         img = X[i].reshape((32, 32, 3))
#         img_flip = sess.run([tf_flip], feed_dict={X_img:img})
#         X_flip.append(img_flip[0])
#         if i % 1000 == 0:
#             print(i)
#     return X_flip

# x_aug = flip_image_tf(x_train)

# np.save('/content/drive/MyDrive/Colab Notebooks/assignment/image classification/data/x_aug2', x_aug) # x_save.npy

def batch_data(shuffled_idx, batch_size, data, labels, start_idx):
    idx = shuffled_idx[start_idx:start_idx+batch_size]
    data_shuffle = [data[i] for i in idx]
    labels_shuffle = [labels[i] for i in idx]

    return np.asarray(data_shuffle), np.asarray(labels_shuffle)

tf.reset_default_graph()

def build_CNN_classifier(x):
    x_image = x

    W1 = tf.get_variable(name="W1", shape=[3, 3, 3, 64], initializer=tf.contrib.layers.xavier_initializer())
    b1 = tf.get_variable(name="b1", shape=[64], initializer=tf.contrib.layers.xavier_initializer())
    c1 = tf.nn.conv2d(x_image, W1, strides=[1, 1, 1, 1], padding='SAME')
    l1 = tf.nn.relu(tf.nn.bias_add(c1, b1))
    n1 = tf.layers.batch_normalization(l1)#,center=True,scale=True,training=batch_prob)
    l1_pool = tf.nn.max_pool(n1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    # l1_pool_drop = tf.nn.dropout(l1_pool,keep_prob=KEEP_PROB)

    W2 = tf.get_variable(name="W2", shape=[3, 3, 64, 48], initializer=tf.contrib.layers.xavier_initializer())
    b2 = tf.get_variable(name="b2", shape=[48], initializer=tf.contrib.layers.xavier_initializer())
    c2 = tf.nn.conv2d(l1_pool, W2, strides=[1, 1, 1, 1], padding='SAME')
    l2 = tf.nn.relu(tf.nn.bias_add(c2, b2))
    l2_drop = tf.nn.dropout(l2,keep_prob=KEEP_PROB)
    n2 = tf.layers.batch_normalization(l2_drop)
    l2_pool = tf.nn.max_pool(n2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    
    W3 = tf.get_variable(name="W3", shape=[3, 3, 48, 32], initializer=tf.contrib.layers.xavier_initializer())
    b3 = tf.get_variable(name="b3", shape=[32], initializer=tf.contrib.layers.xavier_initializer())
    c3 = tf.nn.conv2d(l2_pool, W3, strides=[1, 1, 1, 1], padding='SAME')
    l3 = tf.nn.relu(tf.nn.bias_add(c3, b3))
    n3 = tf.layers.batch_normalization(l3)
    l3_pool = tf.nn.max_pool(n3, ksize=[1, 2, 2, 1], strides=[1, 1, 1, 1], padding='SAME')
    
    l3_flat = tf.reshape(l3_pool, [-1, 8*8*32])

    W_fc = tf.get_variable(name="W_fc", shape=[8*8*32, 10], initializer=tf.contrib.layers.xavier_initializer())
    b_fc = tf.get_variable(name="b_fc", shape=[10], initializer=tf.contrib.layers.xavier_initializer())
    logits = tf.nn.bias_add(tf.matmul(l3_flat, W_fc), b_fc)
    hypothesis = tf.nn.softmax(logits)

    return hypothesis, logits

ckpt_path = "/content/drive/MyDrive/Colab Notebooks/assignment/image classification/output"

x = tf.placeholder(tf.float32, shape=[None, 32, 32, 3])
y = tf.placeholder(tf.float32, shape=[None, 10])

x_train = np.load("/content/drive/MyDrive/Colab Notebooks/assignment/image classification/data/x_train.npy")
y_train = np.load("/content/drive/MyDrive/Colab Notebooks/assignment/image classification/data/y_train.npy")
x_aug = np.load("/content/drive/MyDrive/Colab Notebooks/assignment/image classification/data/x_aug.npy")
x_aug2 = np.load("/content/drive/MyDrive/Colab Notebooks/assignment/image classification/data/x_aug2.npy")

x_aug2 = x_aug2[:24000]
y_aug = np.load("/content/drive/MyDrive/Colab Notebooks/assignment/image classification/data/y_aug.npy")
y_aug = y_aug[:24000]

x_train = np.concatenate((x_train,x_aug),axis = 0)
x_train = np.concatenate((x_train,x_aug2),axis=0)
y_train = np.concatenate((y_train,y_train),axis = 0)
y_train = np.concatenate((y_train,y_aug),axis = 0)

# for ram
del(x_aug)
del(x_aug2)

x_train = x_train/255


# datagen.fit(x_train)

print(np.shape(x_train))

dev_num = len(x_train) // 4

x_dev = x_train[:dev_num]
y_dev = y_train[:dev_num]

x_train = x_train[dev_num:]
y_train = y_train[dev_num:]

y_train_one_hot = tf.squeeze(tf.one_hot(y_train, 10),axis=1)
y_dev_one_hot = tf.squeeze(tf.one_hot(y_dev, 10),axis=1)

y_pred, logits = build_CNN_classifier(x)

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=logits))
train_step = tf.train.AdamOptimizer(
    learning_rate=LR,
    beta1=BETA1,
    beta2=BETA2,
    epsilon=EPSILON,
    use_locking=False,
    name='Adam').minimize(cost)

total_batch = int(len(x_train)/batch_size) if len(x_train)%batch_size == 0 else int(len(x_train)/batch_size) + 1

with tf.name_scope('accruacy'):
    correct_prediction = tf.equal(tf.argmax(logits,1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    tf.summary.scalar('accruacy', accuracy)



with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print("학습시작")

    for epoch in range(training_epochs):
        # print("Epoch", epoch+1)
        start = 0
        avg_cost = 0
        shuffled_idx = np.arange(0, len(x_train))
        np.random.shuffle(shuffled_idx)
        

        for i in range(total_batch):
            batch = batch_data(shuffled_idx, batch_size, x_train, y_train_one_hot.eval(), i*batch_size)

            c, _ = sess.run([cost,train_step], feed_dict={x: batch[0], y: batch[1]})
            avg_cost+= c / total_batch
            
            
        [train_accruacy] = sess.run([accuracy], feed_dict={x:batch[0], y:batch[1]}) # works
        # [s, train_accruacy] = sess.run([summ, accuracy], feed_dict={x:batch[0], y:batch[1]}) #error!
        print("Epoch : %d, training accruacy : %g, cost : %g" % (epoch+1, train_accruacy, avg_cost))

        if epoch % 10 == 0:
            y_prediction = np.argmax(y_pred.eval(feed_dict={x: x_dev}), 1)
            y_true = np.argmax(y_dev_one_hot.eval(), 1)
            dev_f1 = f1_score(y_true, y_prediction, average="weighted") # f1 스코어 측정
            print(" dev 데이터 f1 score: %f" % dev_f1)
    
    saver = tf.train.Saver()
    saver.save(sess, ckpt_path)
    saver.restore(sess, ckpt_path)

    y_prediction = np.argmax(y_pred.eval(feed_dict={x: x_dev}), 1)
    y_true = np.argmax(y_dev_one_hot.eval(), 1)
    dev_f1 = f1_score(y_true, y_prediction, average="weighted") # f1 스코어 측정
    print("dev 데이터 f1 score: %f" % dev_f1)

    # 밑에는 건드리지 마세요
    x_test = np.load("data/x_test.npy")
    test_logits = y_pred.eval(feed_dict={x: x_test})
    np.save("result", test_logits)