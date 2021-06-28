# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
from util import get_enernoc_collection, upload_enernoc_dataset
from shapelets import init_session
from shapelets.dsl.data_app import DataApp
from shapelets.dsl import dsl_op

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
    name="18_plusTSTS",
    description="This Dataapp adds two sequences"
)

app.place(app.markdown("""
  # This Dataapp adds two sequences

  Be sure these two sequences have the same number of points
"""))

upload_enernoc_dataset(client)
enernoc = get_enernoc_collection(client)

sequence_selected = app.sequence_selector(collection=enernoc)

app.place(sequence_selected)

line_chart = app.line_chart(title="Selected sequence 1:", sequence=sequence_selected)
app.place(line_chart)

sequence_selected2 = app.sequence_selector(collection=enernoc)

app.place(sequence_selected2)

line_chart = app.line_chart(title="Selected sequence 2:", sequence=sequence_selected2)
app.place(line_chart)

button = app.button(text="Execute plusTSTS")

sequence_result = dsl_op.plusTSTS(sequence_selected, sequence_selected2)

button.on_click(sequence_result)

app.place(button)

result_line_chart = app.line_chart(title="Result:", sequence=sequence_result)
app.place(result_line_chart)

# Register the Dataapp
client.register_data_app(app)
