# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
from sys import path
path.append("../")

from shapelets import init_session
from shapelets.dsl.data_app import DataApp

from dataapps.util import get_enernoc_sequences, upload_enernoc_dataset

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
