# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
import typing
from shapelets import init_session
from shapelets.dsl.data_app import DataApp
from shapelets.model import Capsule
from shapelets.dsl import dsl_op
import numpy as np
from keras import Sequential
from keras.layers import Dense
from numpy.random import seed
from tensorflow import random

def trainAndRunKerasInference(model_json:Capsule,
                              train_x:Capsule,
                              train_y:Capsule,
                              input:Capsule)->typing.Tuple[float, float]:
    from keras.models import model_from_json
    model = model_from_json(model_json.data)

    # Compile and train the model
    model.compile(loss='mse')
    model.fit(train_x.data, train_y.data)

    # Run prediction on input values
    preds = model.predict(input.data)

    return preds[0][0], preds[0][1]

def buildStringWithOutput(result1:float, result2:float)->str:
    return '# Outputs are: **'+str(result1) + '** and **' + str(result2)+'**'

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
    name="10_inference_keras_model_capsules",
    description="This Dataapp creates a Keras model, passes the training data and an input, and performs inference using data capsules"
)

app.place(app.markdown("""
  # This Dataapp creates a Keras model, passes the training data and an input, and performs inference using data capsules
"""))

# Register two functions, one to run the inference and another one to format the output into a text string
client.register_custom_function(trainAndRunKerasInference,persist_results=False)
client.register_custom_function(buildStringWithOutput,persist_results=False)

# Set random seeds for numpy and tensorflow
seed(1)
random.set_seed(2)

# Create model
model = Sequential()
model.add(Dense(64, input_dim=3, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(2))

# Convert the model into a Capsule
model_json = Capsule(data=model.to_json(), name='model')

# Create some training data, labels and an input array and convert them to Capsules
train_x = Capsule(data = np.asarray([[0, 0, 0], [0, 1, 1], [1, 0, 0], [1, 1, 1]]),name='train_x')
train_y = Capsule(data = np.asarray([[0.0, 1.0],[1.0, 0.0],[0.5, 0.5],[1.0, 0.5]]),name='train_y')
input = Capsule(data = np.asarray([[0.5, 0.7, 0.9]]),name='input')

# Pass model, training data and sample and run inference
output1, output2 = dsl_op.trainAndRunKerasInference(model_json, train_x, train_y, input)

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