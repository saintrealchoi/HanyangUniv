import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("./mnist/data/",one_hot=True)

X = tf.placeholder(tf.float32,[None,784])
Y = tf.placeholder(tf.float32,[None,10])

# random initializer
# W1 = tf.Variable(tf.random_uniform([784,256],-1.,1.))
# b1 = tf.Variable(tf.random_uniform([256],-1.,1.))
# L1 = tf.nn.sigmoid(tf.matmul(X,W1)+b1)


# W2 = tf.Variable(tf.random_uniform([256,256],-1.,1.))
# b2 = tf.Variable(tf.random_uniform([256],-1.,1.))
# L2 = tf.nn.sigmoid(tf.matmul(L1,W2)+b2)

# W3 = tf.Variable(tf.random_uniform([256,10],-1.,1.))
# b3 = tf.Variable(tf.random_uniform([10],-1.,1.))
# logits = tf.nn.sigmoid(tf.matmul(L2,W3)+b3)

# Xavier initializer
W1 = tf.get_variable("W1",shape=[784,256],initializer=tf.contrib.layers.xavier_initializer())
b1 = tf.get_variable("b1",shape=[256],initializer=tf.contrib.layers.xavier_initializer())
L1 = tf.nn.sigmoid(tf.matmul(X,W1)+b1)

W2 = tf.get_variable("W2",shape=[256,256],initializer=tf.contrib.layers.xavier_initializer())
b2 = tf.get_variable("b2",shape=[256],initializer=tf.contrib.layers.xavier_initializer())
L2 = tf.nn.sigmoid(tf.matmul(L1,W2)+b2)


W3 = tf.get_variable("W3",shape=[256,10],initializer=tf.contrib.layers.xavier_initializer())
b3 = tf.get_variable("b3",shape=[10],initializer=tf.contrib.layers.xavier_initializer())
logits = tf.nn.sigmoid(tf.matmul(L2,W3)+b3)
# softmax 함수를 통해 0~9를 예측
hypothesis = tf.nn.softmax(logits)
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=Y,logits=logits))
# SGD optimizer를 통해 최적화
opt = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(cost)

batch_size = 100

# 체크포인트 path
ckpt_path = "model/"

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver()
    # check point로부터 params들을 불러와 모델에 weight들을 저장하는 함수
    saver.restore(sess, ckpt_path)
    #아래 부분은 학습부분
    #     for epoch in range(15):
    #         avg_cost = 0
    #         total_batch = int(mnist.train.num_examples/batch_size)
    #         for i in range(total_batch):
    #             batch_xs,batch_ys = mnist.train.next_batch(batch_size)
    #             c, _ = sess.run([cost,opt],feed_dict = {X:batch_xs, Y:batch_ys})
    #             avg_cost += c/ total_batch
    #         print('Eppoch:', '%d' % (epoch+1),'cost = ', '{:.9f}'.format(avg_cost))
    is_correct = tf.equal(tf.argmax(hypothesis, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))
    #     print("Accuracy",sess.run(accuracy, feed_dict={X: mnist.test.images,Y:mnist.test.labels}))

    #     saver.save(sess,ckpt_path)
    #     saver.restore(sess,ckpt_path)

    # accuracy 출력
    print("Accuracy", sess.run(accuracy, feed_dict={X: mnist.test.images, Y: mnist.test.labels}))