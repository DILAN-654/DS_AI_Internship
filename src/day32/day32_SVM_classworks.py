from sklearn.datasets import load_breast_cancer
from sklearn.svm import SVC
import numpy as np

# Load dataset
cancer = load_breast_cancer()
X = cancer.data[:, :2]   # Use first 2 features
y = cancer.target

# Create and train SVM classifier
svm = SVC(kernel="linear", C=1)
svm.fit(X, y)

# Print some results
print(f"Dataset shape: {X.shape}")
print(f"Number of support vectors: {len(svm.support_vectors_)}")
print(f"Accuracy on training data: {svm.score(X, y):.4f}")

# Predict for a new point
new_point = np.array([[15.0, 20.0]])
prediction = svm.predict(new_point)
print(f"Prediction for {new_point}: {'Malignant' if prediction[0] == 0 else 'Benign'}")