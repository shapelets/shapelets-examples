# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

from shapelets import init_session
from shapelets.dsl import DataApp

# This example work under 0.3.8 and above

client = init_session("admin", "admin")

app = DataApp(name="09_selector", description="09_selector")

selector = app.selector(["hello", "world", "example"])

app.place(selector)

selector2 = app.selector([1, 2, 3])

app.place(selector2)

selector3 = app.selector([{"id": 1, "hello": "world"}, {"id": 2, "hello": "moon"}], index_by="id", label_by="hello", value_by="hello")

app.place(selector3)

print(app.to_json())

client.register_data_app(app)