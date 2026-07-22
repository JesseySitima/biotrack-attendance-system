from app.utils.jwt import create_access_token


def test_create_token():

    token = create_access_token(
        {
            "sub": "admin"
        }
    )

    assert token is not None
    assert isinstance(token, str)