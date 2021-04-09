import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("./mnist/data/",one_hot = True)

X = tf.placeholder(tf.float32,[None,784])
Y = tf.placeholder(tf.float32,[None,10])

andom_uniform([784,256],-1.,1.))
b1 = tf.Variable(tf.random_uniform([256],-1.,1.))

# # Dropout
keep_prob = tf.placeholder(tf.float32)
L1 = tf.sigmoid(tf.matmul(X,W1)+b1)
L1 = tf.nn.dropout(L1,keep_prob)
W2 = tf.Variable(tf.random_uniform([256,256],-1.,1.))
b2 = tf.Variable(tf.random_uniform([256],-1.,1.))
L2 = tf.sigmoid(tf.matmul(L1,W2)+b2)

W3 = tf.Variable(tf.random_uniform([256,10],-1.,1.))
b3 = tf.Variable(tf.random_uniform([10],-1.,1.))
logits = tf.matmul(L2,W3)+b3

hypothesis = tf.nn.softmax(logits)
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels = Y, logits=logits))


# # Using Adam Optimizer
# GD
# opt = tf.train.GradientDescentOptimizer(learning_rate = 0.1).minimize(cost)
# Adam
opt = tf.train.AdamOptimizer(learning_rate = 0.001,
                            beta1 = 0.9,
                            beta2 = 0.999,
                            epsilon = 1e-08,
                            use_locking=False,
                            name='Adam').minimize(cost)

batch_size = 100

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for epoch in range(15):
        avg_cost = 0
        total_batch = int(mnist.train.num_examples/batch_size)
        for i in range(total_batch):
            batch_xs,batch_ys = mnist.train.next_batch(batch_size)
            c, _ = sess.run([cost,opt], feed_dict = {X:batch_xs,Y:batch_ys,keep_prob:0.75})
            avg_cost += c / total_batch
        print('Epoch:', '%d' % (epoch+1), 'cost = ', '{:.9f}'.format(avg_cost))
    is_correct = tf.equal(tf.argmax(hypothesis,1),tf.argmax(Y,1))
    accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))
    print("Accuracy", sess.run(accuracy, feed_dict = {X:mnist.test.images, Y:mnist.test.labels,keep_prob:1}))

