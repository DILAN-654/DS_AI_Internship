from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris

# Load data
X, y = load_iris(return_X_y=True)

# 1. Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# 2. Initialize model
knn = KNeighborsClassifier(n_neighbors=5)

# 3. Fit model
knn.fit(X_train, y_train)

# 4. Predict
predictions = knn.predict(X_test)

# 5. Evaluate
acc = accuracy_score(y_test, predictions)
print(f"Final Accuracy: {acc:.4f}")
print(f"First 5 predictions: {predictions[:5]}")
print(f"First 5 actual labels: {y_test[:5]}")