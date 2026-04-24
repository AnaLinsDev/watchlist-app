from sqlalchemy.exc import IntegrityError


# ------------------------
# GET PROFILE
# ------------------------

def test_get_profile(client, override_auth, fake_user):
    response = client.get("/user/profile")

    assert response.status_code == 200
    data = response.json()

    assert data["email"] == fake_user.email
    assert data["username"] == fake_user.username


# ------------------------
# UPDATE USER - SUCCESS
# ------------------------

def test_update_user_success(client, override_auth, override_db, mocker, fake_user):
    override_db.get.return_value = fake_user

    mocker.patch(
        "app.services.user_service.verify_password",
        return_value=True
    )

    response = client.put(
        "/user/edit",
        json={
            "id": 1,
            "email": "new@test.com",
            "username": "newuser",
            "current_password": "123456"
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["email"] == "new@test.com"
    assert data["username"] == "newuser"

    # stronger assertions
    assert override_db.commit.called
    assert override_db.refresh.called


# ------------------------
# UPDATE USER - INVALID PASSWORD
# ------------------------

def test_update_user_invalid_password(client,
                                      override_auth,
                                      override_db,
                                      mocker,
                                      fake_user):
    override_db.get.return_value = fake_user

    mocker.patch(
        "app.services.user_service.verify_password",
        return_value=False
    )

    response = client.put(
        "/user/edit",
        json={
            "id": 1,
            "current_password": "wrong"
        }
    )

    assert response.status_code == 400


# ------------------------
# UPDATE USER - EMAIL CONFLICT
# ------------------------

def test_update_user_email_conflict(client,
                                    override_auth,
                                    override_db,
                                    mocker,
                                    fake_user):
    override_db.get.return_value = fake_user

    mocker.patch(
        "app.services.user_service.verify_password",
        return_value=True
    )

    override_db.commit.side_effect = IntegrityError(
        statement=None,
        params=None,
        orig=Exception("email already exists")
    )

    response = client.put(
        "/user/edit",
        json={
            "id": 1,
            "email": "existing@test.com",
            "current_password": "123456"
        }
    )

    assert response.status_code == 409


# ------------------------
# UPDATE USER - USERNAME CONFLICT
# ------------------------

def test_update_user_username_conflict(client,
                                       override_auth,
                                       override_db,
                                       mocker,
                                       fake_user):
    override_db.get.return_value = fake_user

    mocker.patch(
        "app.services.user_service.verify_password",
        return_value=True
    )

    override_db.commit.side_effect = IntegrityError(
        statement=None,
        params=None,
        orig=Exception("username already exists")
    )

    response = client.put(
        "/user/edit",
        json={
            "id": 1,
            "username": "existinguser",
            "current_password": "123456"
        }
    )

    assert response.status_code == 409


# ------------------------
# DELETE USER - SUCCESS
# ------------------------

def test_delete_user_success(client, override_auth, override_db, fake_user):
    override_db.get.return_value = fake_user

    response = client.delete("/user/delete")

    assert response.status_code == 200

    cookies = response.headers.get("set-cookie", "")
    assert "access_token=" in cookies.lower()


# ------------------------
# DELETE USER - NOT FOUND
# ------------------------

def test_delete_user_not_found(client, override_auth, override_db):
    override_db.get.return_value = None

    response = client.delete("/user/delete")

    assert response.status_code == 404
