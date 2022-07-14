# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

from shapelets import init_session
from shapelets.dsl.data_app import DataApp
from shapelets.model.metadata_item import MetadataType

import os, sys, inspect 

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from util import upload_enernoc_dataset, get_enernoc_sequences, get_enernoc_collection

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
    name="02_filtering_context",
    description="02_filtering_context"
)

upload_enernoc_dataset(client)
enernoc = get_enernoc_collection(client)
enernoc_sequences = get_enernoc_sequences(client)

# Filter by industry metadata by clicking bars
industry = app.metadata_field(field_name="INDUSTRY", field_type=MetadataType.STRING, collection=enernoc)
# Filter by sq_ft metadata by presing shift and brushing over the chart
sq_ft = app.metadata_field(field_name="SQ_FT", field_type=MetadataType.DOUBLE, collection=enernoc)

# Create a filtering context
fc = app.filtering_context("My filtering context", input_filter=[industry, sq_ft])

# Create an horizontal_flow_panel and place metadata filters inside
hf = app.horizontal_flow_panel("Filters")
hf.place(industry, width=6)
hf.place(sq_ft, width=6)

# Place horizontal_flow_panel into the Dataapp
app.place(hf)

# Place all enernoc_sequences
# Add filtering context into line_chart allow us filter sequences sequences
# by metadata with cross filters
for seq in enernoc_sequences:
    line_chart = app.line_chart(title=seq.name, sequence=seq, filtering_context=fc)
    app.place(line_chart)

# Register the Dataapp
client.register_data_app(app)
