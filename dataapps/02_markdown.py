# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
from shapelets import init_session
from shapelets.dsl.data_app import DataApp

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
  name="02_markdown",
  description="02_markdown"
)

# Create a markdown
md = app.markdown("""
  # Hello title

  ## Hello subtitle

  Hello paragraph with **bold** text and *italics*

  1. list item
  2. list item

  ```python
    # python code inside markdown
    from shapelets import init_session
    init_session("admin", "admin")
  ```
""")
# Place markdown into the Dataapp
app.place(md)

# Register the Dataapp
client.register_data_app(app)
