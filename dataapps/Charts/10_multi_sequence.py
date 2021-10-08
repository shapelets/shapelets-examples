# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

from shapelets import init_session
from shapelets.dsl import dsl_op
from shapelets.dsl.data_app import DataApp
from shapelets.model import Sequence


def register_sequence_line_chart(client):
    """
    Create a dataApp with sequence_line_chart
    """
    collections = client.get_collections()
    enernoc = next(col for col in collections if col.name == "EnerNOC Open Data")
    enernoc_sequences = client.get_collection_sequences(enernoc)
    seq1 = enernoc_sequences[0]
    seq2 = enernoc_sequences[1]
    seq3 = enernoc_sequences[2]

    app = DataApp(
        name="[MULTI SEQUENCE] simple",
        description="Data app with temporal context"
    )

    sequence_selector = app.sequence_selector(title="Select a sequence:", collection=enernoc)

    app.place(sequence_selector)

    multiple = app.line_chart(sequence=[seq1, seq2, seq3], title="Multiple sequences")
    multiple_selector = app.line_chart(sequence=[seq1, seq2, sequence_selector],
                                       title="Multiple sequences, third sequence from selector 1")

    app.place(multiple)
    app.place(multiple_selector)

    client.register_data_app(app)


if __name__ == "__main__":
    client_login = init_session("admin", "admin")
    register_sequence_line_chart(client_login)
