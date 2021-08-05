# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

"""Use this file to create example dataApps"""
from shapelets import init_session
from shapelets.dsl.data_app import DataApp
from urllib.request import urlopen


def register_image(client):
    """
    Create a dataApp with markdown
    """
    app = DataApp(
        name="Data app with image",
        description="Data app with image from internet"
    )

    url = 'https://shapelets.io/static/images/shapelets-logo.png'
    image_data = urlopen(url).read()

    image = app.image(image_data)
    app.place(image)

    print(app.to_json())
    client.register_data_app(app)


if __name__ == "__main__":
    client_login = init_session("admin", "admin", "https://127.0.0.1", 443)
    register_image(client_login)

