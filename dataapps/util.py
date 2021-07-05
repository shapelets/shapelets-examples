# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

from typing import List
from shapelets.model import Sequence
from shapelets.shapelets import Shapelets

# EnerNOC is a dataset of energetic consumtion
# We use this dataset to show you a battery of examples
# For this reason we provide an utility to make sure
# EnerNOC dataset is part of shapelets platform
def upload_enernoc_dataset(client: Shapelets):
  collections = client.get_collections()
  enernoc = [col for col in collections if col.name == "EnerNOC Open Data"]
  if len(enernoc) == 0:
    print("-- Uploading EnerNOC dataset --")
    print("-- This action can take a few seconds --")
    client.create_default_collections("ENERNOC")

def get_enernoc_collection(client: Shapelets):
  collections = client.get_collections()
  return next(col for col in collections if col.name == "EnerNOC Open Data")

def get_enernoc_sequences(client: Shapelets) -> List[Sequence]:
  collections = client.get_collections()
  enernoc = next(col for col in collections if col.name == "EnerNOC Open Data")
  return client.get_collection_sequences(enernoc)