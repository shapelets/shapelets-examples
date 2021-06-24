# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
from shapelets.model.metadata_item import MetadataType
from util import get_enernoc_collection, get_enernoc_sequences, upload_enernoc_dataset
from shapelets import init_session
from shapelets.dsl.data_app import DataApp

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
    name="17_fc_tc_composition",
    description="This Dataapp shows how different filtering and temporal contexts can work concurrently"
)

app.markdown("""
    # Multiple Filtering contexts and temporal context

    This Dataapp shows how different filtering and temporal contexts can work concurrently
""")

upload_enernoc_dataset(client)
enernoc = get_enernoc_collection(client)
enernoc_sequences = get_enernoc_sequences(client)

# Filter by industry metadata by clicking bars
industry = app.metadata_field(field_name="INDUSTRY", field_type=MetadataType.STRING, collection=enernoc)
# Filter by subindustry metadata by clicking bars
sub_industry = app.metadata_field(field_name="SUB_INDUSTRY", field_type=MetadataType.STRING, collection=enernoc)
# Filter by sq_ft metadata by presing shift and brushing over the chart
sq_ft = app.metadata_field(field_name="SQ_FT", field_type=MetadataType.DOUBLE, collection=enernoc)

# Create a filtering context
fc = app.filtering_context("My filtering context 1", input_filter=[industry, sq_ft])
fc2 = app.filtering_context("My filtering context 2", input_filter=[industry, sub_industry])

# Create an horizontal_flow_panel and place metadata filters inside
hf = app.horizontal_flow_panel("Filters")
hf.place(industry, width=4)
hf.place(sub_industry, width=4)
hf.place(sq_ft, width=4)

# Place horizontal_flow_panel into the Dataapp
app.place(hf)

tc = app.temporal_context("My temporal context")

# Place all enernoc_sequences
# Add filtering context into line_chart allow us filter sequences sequences
# by metadata with cross filters
for index, seq in enumerate(enernoc_sequences):
    line_chart = app.line_chart(title=seq.name, sequence=seq, filtering_context=(fc if index % 2 == 0 else fc2), temporal_context=tc)
    app.place(line_chart)

# Register the Dataapp
client.register_data_app(app)
