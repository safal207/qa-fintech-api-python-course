from jsonschema import validate


TRANSFER_SCHEMA = {
    'type': 'object',
    'required': [
        'transfer_id',
        'status',
        'from_account',
        'to_account',
        'amount',
        'fee',
        'idempotency_key',
    ],
    'properties': {
        'transfer_id': {'type': 'string'},
        'status': {'type': 'string', 'enum': ['completed']},
        'from_account': {'type': 'string'},
        'to_account': {'type': 'string'},
        'amount': {'type': 'number'},
        'fee': {'type': 'number'},
        'idempotency_key': {'type': 'string'},
    },
    'additionalProperties': False,
}


def test_transfer_response_contract(client):
    response = client.post(
        '/transfer',
        json={
            'from_account': 'acc_alex',
            'to_account': 'acc_yura',
            'amount': '25.00',
            'idempotency_key': 'contract-transfer-001',
        },
    )

    assert response.status_code == 200
    validate(instance=response.json(), schema=TRANSFER_SCHEMA)
