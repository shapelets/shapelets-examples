# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
from shapelets import init_session
from shapelets.dsl.data_app import DataApp

from dataapps.util import get_enernoc_collection, upload_enernoc_dataset

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
    name="07_sequence_selector_multiple",
    description="07_sequence_selector_multiple"
)

# These lines below ensure that EnerNOC dataset is in shapelets platform
upload_enernoc_dataset(client)
enernoc = get_enernoc_collection(client)

# Create a multi_sequence_selector
multi_sequence_selector = app.multi_sequence_selector(title="Select multiple sequences:", collection=enernoc)
# Place multi_sequence_selector into the Dataapp
app.place(multi_sequence_selector)

# Register the Dataapp
client.register_data_app(app)
