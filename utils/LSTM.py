'''
E4040 2023Fall Assignment3
LSTM
'''

import tensorflow as tf


class LSTMCell(tf.keras.Model):
    '''
    Build your own LSTMCell as a trainable model inherited from TensorFlow base model. 

    Methods: 
    - __init__: initialize the model
    - build   : build the parameters
    - call    : implement the forward pass

    Once you have built this model, TensorFlow will be able to calculate the gradients 
    and update the parameters like a regular keras.layer object that you're familiar with. 

    This is a useful technique when you need to create something uncommon on your own. 
    See details at https://www.tensorflow.org/api_docs/python/tf/keras/Model
    '''

    def __init__(
        self, units, 
        kernel_initializer=tf.keras.initializers.GlorotUniform, 
        recurrent_initializer=tf.keras.initializers.Orthogonal, 
        bias_initializer=tf.keras.initializers.Zeros
    ):
        ''' Initialize the model '''

        # Save the useful arguments
        # Number of units (dimensions) for LSTM
        self.units = units
        # Weight initializers
        self.kernel_initializer = kernel_initializer
        self.recurrent_initializer = recurrent_initializer
        self.bias_initializer = bias_initializer

        # For RNN layer
        self.state_size = (units, units)

        # When deriving your own model on top of tf.keras.model, 
        # Firstly, you need to initialize this base model
        super().__init__()


    def build(self, input_shape):
        '''
        Build the parameters

        When calling a model, Tensorflow will build it before feeding in input data. 
        This is done when you call "model.build()" or specify an "input_shape". 

        When building the model, each component (layer) will be built by calling this
        "build" method with an argument of "input_shape", which allows for more 
        flexibility because you don't need to specify the data shape until runtime. 

        :param input_shape: the shape of "inputs" of "call" method [batch_size, time_steps, dim]
        '''

        kernel_shape, recurrent_shape, bias_shape = None, None, None

        ###################################################
        # TODO: Specify the parameter shapes              #
        ###################################################
        
        input_dim = input_shape[-1]

        # Defining the shapes for kernel, recurrent kernel, and biases
        kernel_shape = (input_dim + self.units, 4 * self.units)
        recurrent_shape = (self.units, 4 * self.units)  # Recurrent kernel shape
        bias_shape = (4 * self.units,)

        # Initialize the parameters 
        self.kernel = self.add_weight(shape=kernel_shape, initializer=self.kernel_initializer, name='kernel')
        self.recurrent_kernel = self.add_weight(shape=recurrent_shape, initializer=self.recurrent_initializer, name='recurrent_kernel')
        self.bias = self.add_weight(shape=bias_shape, initializer=self.bias_initializer, name='bias')
        
        ###################################################
        # END TODO                                        #
        ###################################################
        

        # Build the parameters using "add_weights"
        # This is a method inherited from keras.Model
        self.kernel = self.add_weight(
            shape=kernel_shape, 
            name='kernel', 
            initializer=self.kernel_initializer
        )
        self.recurrent_kernel = self.add_weight(
            shape=recurrent_shape, 
            name='recurrent_kernel', 
            initializer=self.recurrent_initializer
        )
        self.bias = self.add_weight(
            shape=bias_shape, 
            name='bias', 
            initializer=self.bias_initializer
        )
        # The weights will then be readily available for use
        # in the "call" method, and they are added automatically
        # to backpropagation and optimization

        # Set build flag to true
        self.built = True


    def call(self, inputs, states):
        '''
        Forward pass for LSTM cell. 

        :param inputs: cell inputs of one time step, 
            a tf.Tensor of shape [batch_size, dims]
        :param states: cell states from last time step, 
            a tuple of (hidden_states, carry_states)

        Return
        : a tuple of new hidden states and cell states
        '''

        h, c = None, None

        ###################################################
        # TODO: LSTMCell forward pass                     #
        ###################################################
        
        h_prev, c_prev = states

        # Concatenating inputs and previous hidden states
        combined = tf.concat([inputs, h_prev], axis=1)

        # Computing the gate activations
        gate_inputs = tf.matmul(combined, self.kernel) + self.bias

        # Split gate inputs into four parts for different gates
        i, f, c_bar, o = tf.split(gate_inputs, num_or_size_splits=4, axis=1)

        # Applying the forget gate
        f = tf.sigmoid(f)
        c = f * c_prev

        # Updating the cell state
        i = tf.sigmoid(i)
        c_bar = tf.tanh(c_bar)
        c = c + i * c_bar  # Updated to use += operator for clarity

        # Computing the new hidden state
        o = tf.sigmoid(o)
        h = o * tf.tanh(c)
        
        ###################################################
        # END TODO                                        #
        ###################################################
        

        return h, [h, c]


class LSTMModel(tf.keras.Model):
    ''' Define your own LSTM Model '''

    def __init__(self, units, output_dim, activation, input_shape):
        '''
        Initialize the model. 

        :params units: number of units for LSTMCell
        :params output_dim: final output dimension 
        :params activation: activation of the final layer
        :params input_shape: shape of model input
        '''

        # initialize the base class first
        super().__init__()

        ###################################################
        # TODO: Add the RNN and other layers              #
        ###################################################
        
        
        # Initializing the LSTMCell
        self.lstm_cell = LSTMCell(units)

        # RNN layer using the custom LSTMCell
        self.rnn_layer = tf.keras.layers.RNN(self.lstm_cell, return_sequences=True, return_state=False)

        # Output layer
        self.dense = tf.keras.layers.Dense(output_dim, activation=activation)

        ###################################################
        # END TODO                                        #
        ###################################################


    def call(self, inputs):
        '''
        LSTM model forward pass. 
        '''

        # Don't forget this conversion because we have 
        # initialized our weights to be float
        # certain operations must require identical types
        x = tf.cast(inputs, float)

        ###################################################
        # TODO: Feedforward through your model            #
        ###################################################
        
        
        x = tf.cast(inputs, dtype=tf.float32)

        # Forward pass through LSTM layer
        x = self.rnn_layer(x)

        # Forward pass through output Dense layer
        x = self.dense(x)


        ###################################################
        # END TODO                                        #
        ###################################################
        
        return x

