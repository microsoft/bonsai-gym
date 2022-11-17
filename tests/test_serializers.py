import json

import numpy as np
import pytest

from bonsai_gym.serializers import NumpyEncoder

states = (
    ({"float": np.float_(90)}, '{"float": 90.0}'),
    ({"int": np.int_(90)}, '{"int": 90}'),
    ({"bool": np.bool_(1)}, '{"bool": true}'),
    ({"list_float": np.arange(2, dtype=np.float_)}, '{"list_float": [0.0, 1.0]}'),
    ({"list_int": np.arange(2, dtype=np.int_)}, '{"list_int": [0, 1]}'),
)


@pytest.mark.parametrize("state, encoded", states)
def test_numpy_encoder(state, encoded):
    assert json.dumps(state, cls=NumpyEncoder) == encoded
