# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

"""Use this file to create example dataApps"""
from shapelets import init_session
from shapelets.dsl.data_app import DataApp
from shapelets.model.image import Image
from shapelets.dsl import dsl_op
import numpy as np


def generate_image(a: int, b: int, n: int) -> Image:
    import matplotlib.pyplot as plt

    x = np.linspace(a, b, n)
    y = np.sin(x ** 2) + np.cos(x)

    fig = plt.figure()
    plt.plot(x, y, label='Line 1')
    plt.plot(x, y - 0.6, label='Line 2')
    plt.legend()
    fig.suptitle("""Function Example\n\n""", fontweight="bold")

    return Image(fig)

def register_image(client):
    """
    Create a dataApp with markdown
    """
    app = DataApp(
        name="Data app with image from Matplotlib",
        description="Data app with image from Matplotlib Figure"
    )

    client.register_custom_function(generate_image)

    a = app.number(value_type=int)
    b = app.number(value_type=int)
    n = app.number(value_type=int)

    app.place(a)
    app.place(b)
    app.place(n)

    fig = dsl_op.generate_image(a, b, n)

    button = app.button("Generate Matplotlib figure")
    button.on_click(fig)
    app.place(button)

    image = app.image(fig)
    app.place(image)

    print(app.to_json())
    client.register_data_app(app)


if __name__ == "__main__":
    client_login = init_session("admin", "admin", "https://127.0.0.1", 443)
    register_image(client_login)

