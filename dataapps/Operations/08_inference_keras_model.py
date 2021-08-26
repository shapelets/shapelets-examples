# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
import typing
from shapelets import init_session
from shapelets.dsl.data_app import DataApp, NDArray
from shapelets.dsl import dsl_op
import numpy as np

def trainAndRunKerasInference(train_x:NDArray, train_y:NDArray, input:NDArray)->typing.Tuple[float, float]:
    from keras import Sequential
    from keras.layers import Dense
    from numpy.random import seed
    from tensorflow import random

    # Set random seeds for numpy and tensorflow
    seed(1)
    random.set_seed(2)

    # Create model
    model = Sequential()
    model.add(Dense(64, input_dim=3, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(2))
    model.compile(loss='mse')

    # Train the model
    model.fit(train_x.values, train_y.values)

    # Run prediction on input values
    preds = model.predict(input.values)

    return preds[0][0], preds[0][1]

def buildStringWithOutput(result1:float, result2:float)->str:
    return '# Outputs are: **'+str(result1) + '** and **' + str(result2)+'**'

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
    name="08_inference_keras_model",
    description="This Dataapp creates a Keras model and performs inference of a given input"
)

app.place(app.markdown("""
  # This Dataapp creates a Keras model and performs inference of a given input
"""))

# Register two functions, one to run the inference and another one to format the output into a text string
client.register_custom_function(trainAndRunKerasInference,persist_results=False)
client.register_custom_function(buildStringWithOutput,persist_results=False)

# Create some training data, labels and an input array and convert them to NDArrays
train_x = client.create_nd_array(np.asarray([[0, 0, 0], [0, 1, 1], [1, 0, 0], [1, 1, 1]]))
train_y = client.create_nd_array(np.asarray([[0.0, 1.0],[1.0, 0.0],[0.5, 0.5],[1.0, 0.5]]))
input = client.create_nd_array(np.asarray([[0.5, 0.7, 0.9]]))

# Train, run inference and get two outputs from model
output1, output2 = dsl_op.trainAndRunKerasInference(train_x, train_y, input)

# Convert the output into a displayable string
output_string = dsl_op.buildStringWithOutput(output1, output2)

# Create button
button = app.button(text="Make inference")
button.on_click([output_string])
app.place(button)

# Create markdown to show results
app.place(app.markdown(output_string))

# Register the Dataapp
client.register_data_app(app)