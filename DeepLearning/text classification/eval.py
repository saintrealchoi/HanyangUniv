import sys
import numpy as np

result_path = sys.argv[1] # result.npy
GT = sys.argv[2] # data/y_test.npy

result = np.load(result_path)
y_prediction = np.argmax(result, 1)
y_test = np.load(GT)


is_correct = np.equal(y_prediction, y_test)
accuracy = np.mean(is_correct)

print(accuracy)