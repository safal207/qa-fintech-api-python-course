from decimal import Decimal


def get_balance(client, account_id):
    return Decimal(str(client.get(f'/accounts/{account_id}').json()['balance']))


def test_transfer_updates_balances_with_fee(client):
    before_alex = get_balance(client, 'acc_alex')
    before_yura = get_balance(client, 'acc_yura')

    response = client.post(
        '/transfer',
        json={
            'from_account': 'acc_alex',
            'to_account': 'acc_yura',
            'amount': '100.00',
            'idempotency_key': 'idem-transfer-001',
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body['status'] == 'completed'
    assert Decimal(str(body['fee'])) == Decimal('1.00')

    after_alex = get_balance(client, 'acc_alex')
    after_yura = get_balance(client, 'acc_yura')

    assert after_alex == before_alex - Decimal('101.00')
    assert after_yura == before_yura + Decimal('100.00')


def test_same_idempotency_key_does_not_charge_twice(client):
    payload = {
        'from_account': 'acc_alex',
        'to_account': 'acc_yura',
        'amount': '100.00',
        'idempotency_key': 'idem-transfer-retry-001',
    }

    first = client.post('/transfer', json=payload)
    balance_after_first = get_balance(client, 'acc_alex')

    second = client.post('/transfer', json=payload)
    balance_after_second = get_balance(client, 'acc_alex')

    assert first.status_code == 200
    assert second.status_code == 200
    assert second.json()['transfer_id'] == first.json()['transfer_id']
    assert balance_after_second == balance_after_first


def test_transfer_fails_when_insufficient_funds(client):
    response = client.post(
        '/transfer',
        json={
            'from_account': 'acc_yura',
            'to_account': 'acc_alex',
            'amount': '100000.00',
            'idempotency_key': 'idem-too-large-001',
        },
    )

    assert response.status_code == 409
    assert response.json()['detail']['code'] == 'INSUFFICIENT_FUNDS'


def test_transfer_fails_with_domain_error_for_invalid_amount(client):
    response = client.post(
        '/transfer',
        json={
            'from_account': 'acc_alex',
            'to_account': 'acc_yura',
            'amount': '-1.00',
            'idempotency_key': 'idem-invalid-amount-001',
        },
    )

    assert response.status_code == 422
    assert response.json()['detail']['code'] == 'INVALID_AMOUNT'
