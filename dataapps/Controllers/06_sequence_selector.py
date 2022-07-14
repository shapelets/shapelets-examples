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

from util import upload_enernoc_dataset, get_enernoc_collection

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
    name="06_sequence_selector",
    description="06_sequence_selector"
)

# These lines below ensure that EnerNOC dataset is in shapelets platform
upload_enernoc_dataset(client)
enernoc = get_enernoc_collection(client)

# Create a sequence_selector
sequence_selector = app.sequence_selector(title="Select a sequence:", collection=enernoc)
# Place sequence_selector into the Dataapp
app.place(sequence_selector)

# Register the Dataapp
client.register_data_app(app)
