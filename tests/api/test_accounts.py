def test_get_existing_account(client):
    response = client.get('/accounts/acc_alex')

    assert response.status_code == 200
    body = response.json()
    assert body['id'] == 'acc_alex'
    assert body['currency'] == 'USD'
    assert body['balance'] == 1000.0


def test_get_missing_account_returns_404(client):
    response = client.get('/accounts/unknown')

    assert response.status_code == 404
    assert response.json()['detail']['code'] == 'ACCOUNT_NOT_FOUND'
