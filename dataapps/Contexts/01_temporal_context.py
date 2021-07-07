# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
from shapelets import init_session
from shapelets.dsl.data_app import DataApp

from dataapps.util import get_enernoc_sequences, upload_enernoc_dataset

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
    name="01_temporal_context",
    description="01_temporal_context"
)

upload_enernoc_dataset(client)
enernoc_sequences = get_enernoc_sequences(client)

# Create a temporal context
tc = app.temporal_context("My temporal context")

# Place all enernoc_sequences
# Add temporal context into line_chart allow us to coordinate all sequences
# zoom in, zoom out and panning at the same time

for seq in enernoc_sequences:
    line_chart = app.line_chart(title=seq.name, sequence=seq, temporal_context=tc)
    app.place(line_chart)

# Register the Dataapp
client.register_data_app(app)
