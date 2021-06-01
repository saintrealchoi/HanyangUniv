import numpy as np
import tensorflow as tf
import tensorflow.contrib.rnn as rnn_cell

def batch_data(shuffled_idx, batch_size, data, labels, start_idx):
    idx = shuffled_idx[start_idx:start_idx+batch_size]
    data_shuffle = [data[i] for i in idx]
    labels_shuffle = [labels[i] for i in idx]

    return np.asarray(data_shuffle), np.asarray(labels_shuffle)

def get_vocabulary_size(X):
    return max([max(x) for x in X]) + 1 # plus the 0th word

def fit_in_vocabulary(X, voc_size):
    return [[w for w in x if w < voc_size] for x in X]

def zero_pad(X, seq_len):
    return np.array([x[:seq_len - 1] + [0] * max(seq_len - len(x), 1) for x in X])

tf.reset_default_graph()
def build_classifier(x, vocabulary_size, EMBEDDING_DIM, HIDDEN_SIZE):
    n_layers = 4
    # Embedding layer
    embeddings_var = tf.Variable(tf.random_uniform([vocabulary_size, EMBEDDING_DIM], -1.0, 1.0), trainable=True)
    batch_embedded = tf.nn.embedding_lookup(embeddings_var, x)

    # RNN layer
    cells = [rnn_cell.BasicLSTMCell(HIDDEN_SIZE) for layer in range(n_layers)]
    cells_drop = [rnn_cell.DropoutWrapper(cell, output_keep_prob=KEEP_PROB)for cell in cells]
    multi_layer_cell = rnn_cell.MultiRNNCell(cells_drop)
    
    rnn_outputs, states = tf.nn.dynamic_rnn(multi_layer_cell, batch_embedded, dtype=tf.float32)
    
    # Fully connected layer
    W = tf.Variable(tf.random_uniform([HIDDEN_SIZE, 2], -1.0, 1.0), trainable=True)
    b = tf.Variable(tf.random_uniform([2], -1.0, 1.0), trainable=True)
    logits = tf.nn.bias_add(tf.matmul(rnn_outputs[:,-1], W), b)
    hypothesis = tf.nn.softmax(logits)

    return hypothesis, logits

ckpt_path = "output/"

SEQUENCE_LENGTH = 200
EMBEDDING_DIM = 500
HIDDEN_SIZE = 150
BATCH_SIZE = 256
NUM_EPOCHS = 10
learning_rate = 0.001
KEEP_PROB = 0.75

np.load.__defaults__=(None, True, True, 'ASCII')

x_train = np.load("/content/drive/MyDrive/Colab Notebooks/assignment2/data/x_train.npy")
y_train = np.load("/content/drive/MyDrive/Colab Notebooks/assignment2/data/y_train.npy")
x_test = np.load("/content/drive/MyDrive/Colab Notebooks/assignment2/data/x_test.npy")

# For EDA
# import json

# avg = 0
# max = -1
# for i in range(len(x_train)):
#     if max < len(x_train[i]):
#         max = len(x_train[i])
#     avg += len(x_train[i])/40000

# index_to_word = json.load(open("/content/drive/MyDrive/Colab Notebooks/assignment2/data/dictionary.json"))
# print("------------------------------------EDA------------------------------------")
# print("데이터의 개수는 총 {}개입니다".format(len(x_train)))
# print("데이터의 예시와 Label은 다음과 같습니다.")
# print(" Data : "+''.join([index_to_word[str(index)]+" " for index in x_train[0]]))
# print(" Label: {}".format("negative" if y_train[0]==0 else "positive"))
# print("  Data Average Length : {}".format(int(avg)))
# print("  Data Max Length     : {}".format(max))

dev_num = len(x_train) // 4

x_dev = x_train[:dev_num]
y_dev = y_train[:dev_num]

x_train = x_train[dev_num:]
y_train = y_train[dev_num:]

y_train_one_hot = tf.squeeze(tf.one_hot(y_train, 2))
y_dev_one_hot = tf.squeeze(tf.one_hot(y_dev, 2))


# Sequences pre-processing
vocabulary_size = get_vocabulary_size(x_train)
x_dev = fit_in_vocabulary(x_dev, vocabulary_size)
x_train = zero_pad(x_train, SEQUENCE_LENGTH)
x_dev = zero_pad(x_dev, SEQUENCE_LENGTH)

batch_ph = tf.placeholder(tf.int32, [None, SEQUENCE_LENGTH], name='batch_ph')
target_ph = tf.placeholder(tf.float32, [None, 2], name='target_ph')

y_pred, logits = build_classifier(batch_ph, vocabulary_size, EMBEDDING_DIM, HIDDEN_SIZE)

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=target_ph, logits=logits))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

# Accuracy metric
is_correct = tf.equal(tf.argmax(y_pred, 1), tf.argmax(target_ph, 1))
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))

total_batch = int(len(x_train)/BATCH_SIZE) if len(x_train)%BATCH_SIZE == 0 else int(len(x_train)/BATCH_SIZE) + 1
print(total_batch)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    print("학습시작")

    for epoch in range(NUM_EPOCHS):
        start = 0
        shuffled_idx = np.arange(0, len(x_train))
        np.random.shuffle(shuffled_idx)

        for i in range(total_batch):
            batch = batch_data(shuffled_idx, BATCH_SIZE, x_train, y_train_one_hot.eval(), i * BATCH_SIZE)
            sess.run(optimizer, feed_dict={batch_ph: batch[0], target_ph: batch[1]})

        dev_accuracy = accuracy.eval(feed_dict={batch_ph: x_dev, target_ph: np.asarray(y_dev_one_hot.eval())})
        print("Epoch : %d, Accuracy : %f" % (epoch+1,dev_accuracy))


        # for save  
        saver = tf.train.Saver()
        saver.save(sess, ckpt_path)
        saver.restore(sess, ckpt_path)

    dev_accuracy = accuracy.eval(feed_dict={batch_ph: x_dev, target_ph: np.asarray(y_dev_one_hot.eval())})
    print("dev 데이터 Accuracy: %f" % dev_accuracy)

    # 밑에는 건드리지 마세요
    x_test = fit_in_vocabulary(x_test, vocabulary_size)
    x_test = zero_pad(x_test, SEQUENCE_LENGTH)

    test_logits = y_pred.eval(feed_dict={batch_ph: x_test})
    np.save("result", test_logits)

