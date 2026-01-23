import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Setting up the brain architecture!
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # We need to initialize our weights with some random values to start.
        # It's like giving the car a clueless brain that barely knows how to function initially.
        
        # These weights connect the input sensors to the hidden processing layer.
        self.weights_ih = np.random.uniform(-1, 1, (self.input_size, self.hidden_size))
        
        # These weights connect the hidden layer to the final output (steering/speed).
        self.weights_ho = np.random.uniform(-1, 1, (self.hidden_size, self.output_size))
        
        # Biases are like personal preferences for neurons, helping shift the activation function.
        self.bias_h = np.random.uniform(-1, 1, (1, self.hidden_size))
        self.bias_o = np.random.uniform(-1, 1, (1, self.output_size))

    def feed_forward(self, inputs):
        # Thinking time! passing inputs through the network to get an output.
        
        # First, let's make sure our input is in the right shape for matrix math.
        inputs = np.array(inputs).reshape(1, -1)
        
        # Calculate the activation for the hidden layer.
        # It's basically: (Input * Weights) + Bias
        hidden_inputs = np.dot(inputs, self.weights_ih) + self.bias_h
        
        # Apply the activation function. We use Tanh here to squash values between -1 and 1.
        hidden_outputs = self.tanh(hidden_inputs)
        
        # Now pass those hidden results to the output layer.
        final_inputs = np.dot(hidden_outputs, self.weights_ho) + self.bias_o
        final_outputs = self.tanh(final_inputs)
        
        # Flatten the result back to a simple list so it's easier to read.
        return final_outputs.flatten()

    def tanh(self, x):
        # A classic activation function. It maps any number to a value between -1 and 1.
        # Perfect for steering (left vs right) and speed (forward vs backward... though we usually go forward).
        return np.tanh(x)

    def copy(self):
        # This creates a clone of the brain.
        # We use this to copy the best performing cars to the next generation.
        new_nn = NeuralNetwork(self.input_size, self.hidden_size, self.output_size)
        new_nn.weights_ih = np.copy(self.weights_ih)
        new_nn.weights_ho = np.copy(self.weights_ho)
        new_nn.bias_h = np.copy(self.bias_h)
        new_nn.bias_o = np.copy(self.bias_o)
        return new_nn

    def mutate(self, rate=0.1):
        # Mutation is the spice of life (and evolution)!
        # We slightly tweak the weights to see if it makes the car smarter (or dumber).
        
        def mutate_val(val):
            # Roll the dice! If we hit the mutation rate, change the value slightly.
            if np.random.random() < rate:
                return val + np.random.normal(0, 0.1) # Add a tiny bit of random noise
            return val
        
        # Numpy's vectorize lets us apply this mutation logic to every weight very quickly.
        v_mutate = np.vectorize(mutate_val)
        
        self.weights_ih = v_mutate(self.weights_ih)
        self.weights_ho = v_mutate(self.weights_ho)
        self.bias_h = v_mutate(self.bias_h)
        self.bias_o = v_mutate(self.bias_o)
