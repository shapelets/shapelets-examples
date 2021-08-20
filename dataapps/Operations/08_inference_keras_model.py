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

def runKerasInference(input:NDArray)->typing.Tuple[float, float]:
    from keras import Sequential
    from keras.layers import Dense
    import numpy as np
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
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    # Create some training data and labels
    train_x = np.asarray([[0, 0, 0], [0, 1, 1], [1, 0, 0], [1, 1, 1]])
    train_y = np.asarray([0, 1, 1, 0])

    # Train the model
    model.fit(train_x, train_y)

    # Run prediction on input values
    preds = model.predict(input.values)

    return preds[0][0], preds[0][1]

def buildStringWithOutput(input1:float, input2:float)->str:
    return 'Outputs are: '+str(input1) + ' and ' + str(input2)

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

client.register_custom_function(runKerasInference)
client.register_custom_function(buildStringWithOutput)

# Create input as np array and convert it to NDArray
input = client.create_nd_array(np.asarray([[0.5, 0.8, 0.9]]))

# Run inference and get two outputs from model
output1, output2 = dsl_op.runTensorflowInference(input)

# Convert the output into a displayable string
output_string = dsl_op.buildStringWithOutput(output1,output2)

# Create button
button = app.button(text="Make inference")
button.on_click([output1, output2, output_string])
app.place(button)

# Create label to show results
label = app.label(output_string)
app.place(label)

# Register the Dataapp
client.register_data_app(app)