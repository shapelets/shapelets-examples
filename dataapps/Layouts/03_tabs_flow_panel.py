# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

from shapelets import init_session
from shapelets.dsl import DataApp

client = init_session("admin", "admin")

app = DataApp(name="03_tabs_flow_panel", description="This dataApp shows how to use tabs_flow_panel")

tabs_fp = app.tabs_flow_panel("My tab flow panel")

vf = app.vertical_flow_panel()
vf2 = app.vertical_flow_panel()

tabs_fp.place(vf, "Tab 1")
tabs_fp.place(vf2, "Tab 2")

vf.place(app.markdown("""
    # MD for tab 1
    This markdown is rendered into the first tab
"""))

vf2.place(app.markdown("""
    # MD for tab 2
    This markdown is rendered into the second tab
"""))

app.place(tabs_fp)

client.register_data_app(app)
