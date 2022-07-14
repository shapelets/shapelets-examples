# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.


from shapelets import init_session
from shapelets.dsl.data_app import DataApp
import os, sys, inspect 

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from util import upload_enernoc_dataset, get_enernoc_sequences

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
    name="01_linechart_sequence",
    description="01_linechart_sequence"
)

# These lines below ensure that EnerNOC dataset is in shapelets platform
upload_enernoc_dataset(client)
enernoc_sequences = get_enernoc_sequences(client)
sequence = enernoc_sequences[0]

# Create a line_chart rendering a sequence
line_chart = app.line_chart(title=sequence.name, sequence=sequence)
# Place line_chart into the Dataapp
app.place(line_chart)

# Register the Dataapp
client.register_data_app(app)
