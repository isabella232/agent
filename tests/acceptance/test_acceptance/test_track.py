import json
import os
import pytest
import requests

from tests.acceptance.helpers import create_and_validate_request_and_response
from tests.acceptance.helpers import ENDPOINT_TRACK


BASE_URL = os.getenv('host')


@pytest.mark.parametrize("event_key, status_code, bypass_validation", [
    ("myevent", 200, False),
    ("", 400, True),
    ("invalid_event_key", 200, False)
], ids=["Valid event key", "Empty event key", "Invalid event key"])
def test_track(session_obj, event_key, status_code,bypass_validation):
    """
    Track event for the given user.
    Track sends event and user details to Optimizely’s analytics backend
    for the analysis of a feature test or experiment.
    :param agent_server: starts agent server with default config
    :param session_obj: session fixture
    :param event_key: parameterized param
    :param status_code: parameterized param
    """
    # TODO - ADD EVENT TAGS - AND TEST DIFFERENT SCENARIONS WITH EVENT TAGS
    payload = '{"userId": "matjaz", "userAttributes": {"attr_1": "hola"}, "eventTags": {}}'
    params = {"eventKey": event_key}

    resp = create_and_validate_request_and_response(ENDPOINT_TRACK, 'post', session_obj, bypass_validation, payload=payload, params=params)

    assert resp.status_code == status_code, f'Status code should be {status_code}. {resp.text}'

    if event_key == "":
        with pytest.raises(requests.exceptions.HTTPError):
            assert resp.status_code == status_code
            assert resp.text == '{"error":"missing required path parameter: eventKey"}\n'
            resp.raise_for_status()

    if event_key == "invalid_event_key":
        assert resp.status_code == status_code
        assert resp.text == '{"userId":"matjaz","eventKey":"invalid_event_key","error":"event with key \\"invalid_event_key\\" not found"}\n'


def test_track_403(session_override_sdk_key):
    """
    Test that 403 Forbidden is returned. We use invalid SDK key to trigger 403.
    :param : session_obj
    """
    payload = '{"userId": "matjaz", "userAttributes": {"attr_1": "hola"}}'
    params = {"eventKey": "myevent"}

    with pytest.raises(requests.exceptions.HTTPError):
        resp = create_and_validate_request_and_response(ENDPOINT_TRACK, 'post', session_override_sdk_key,
                                                        payload=payload, params=params)

        assert resp.status_code == 403
        assert resp.json()['error'] == 'unable to fetch fresh datafile (consider ' \
                                       'rechecking SDK key), status code: 403 Forbidden'

        resp.raise_for_status()
