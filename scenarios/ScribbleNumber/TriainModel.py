import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import numpy as np

# Load the MNIST dataset
mnist = fetch_openml('mnist_784', version=1, as_frame=False)
X, y = mnist["data"], mnist["target"]

# Normalize the data
X = X / 255.0

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a neural network model
clf = MLPClassifier(hidden_layer_sizes=(100,), max_iter=10, random_state=42, verbose=1)
clf.fit(X_train, y_train)

# Function to generate and display a handwritten-like digit
def generate_handwritten_digit(digit, model):
    # Create a random noise vector
    noise = np.random.normal(0, 1, (1, 784))
  
    # Predict the digit from the noise using the trained model
    predicted_digit = model.predict(noise)

    # If the prediction matches the desired digit, reshape and display it
    if str(predicted_digit[0]) == str(digit):
        image = noise.reshape(28, 28)
        plt.imshow(image, cmap='gray')
        plt.title(f"Generated Digit: {digit}")
        plt.show()
        return True
    return False
  
# Generate and display a handwritten-like '3'
digit_to_generate = 3
max_attempts = 100

for attempt in range(max_attempts):
    if generate_handwritten_digit(digit_to_generate, clf):
        break
    if attempt == max_attempts -1:
        print(f"Failed to generate digit {digit_to_generate} after {max_attempts} attempts.")

