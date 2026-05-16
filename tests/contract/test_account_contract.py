from jsonschema import validate


ACCOUNT_SCHEMA = {
    'type': 'object',
    'required': ['id', 'currency', 'balance'],
    'properties': {
        'id': {'type': 'string'},
        'currency': {'type': 'string'},
        'balance': {'type': 'number'},
    },
    'additionalProperties': False,
}


def test_account_response_contract(client):
    response = client.get('/accounts/acc_alex')

    assert response.status_code == 200
    validate(instance=response.json(), schema=ACCOUNT_SCHEMA)
