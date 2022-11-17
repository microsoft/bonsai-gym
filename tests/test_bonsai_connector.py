import numpy as np
import pytest

from bonsai_gym.bonsai_connector import BonsaiConnector


states = (
    ({'numpy': np.float_(10)}, False),
    ({'numpy': np.int_(10)}, False),
    ({'numpy': np.bool_(10)}, False),
    ({'numpy': np.arange(10)}, False),
    ({'accepted': 1}, True),
    ({'accepted': 1.0}, True),
    ({'accepted': [1.0, 2.0]}, True),
    ({'accepted': True}, True),
    ({'accepted': [True, False]}, True),
    ({'accepted': {'dict': 1}}, True),
    ({'invalid': [np.int_(2), np.int_(5)]}, False),
    ({'invalid': 'string'}, False),
    ({'invalid': {'dict': np.float_(100)}}, False),
)


@pytest.mark.parametrize('state, valid', states)
def test_bonsai_connector_validate_state(state, valid):
    if valid:
        assert BonsaiConnector.validate_state(state) is None
    else:
        with pytest.raises(TypeError):
            BonsaiConnector.validate_state(state)
