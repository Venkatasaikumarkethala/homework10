import pytest

@pytest.mark.asyncio
async def test_update_only_bio(async_client, admin_user, admin_token):
    payload = {"bio": "Updated bio content."}
    response = await async_client.put(
        f"/users/{admin_user.id}",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["bio"] == "Updated bio content."
    assert response.json()["profile_picture_url"] == admin_user.profile_picture_url


@pytest.mark.asyncio
async def test_update_only_profile_picture(async_client, admin_user, admin_token):
    new_url = "https://cdn.example.com/images/avatar1.jpg"
    payload = {"profile_picture_url": new_url}
    response = await async_client.put(
        f"/users/{admin_user.id}",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["profile_picture_url"] == new_url
    assert response.json()["bio"] == admin_user.bio


@pytest.mark.asyncio
async def test_update_bio_and_profile_picture(async_client, admin_user, admin_token):
    payload = {
        "bio": "Full profile update",
        "profile_picture_url": "https://cdn.example.com/images/avatar2.png"
    }
    response = await async_client.put(
        f"/users/{admin_user.id}",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["bio"] == "Full profile update"
    assert data["profile_picture_url"] == payload["profile_picture_url"]


@pytest.mark.asyncio
async def test_invalid_profile_picture_format(async_client, admin_user, admin_token):
    payload = {
        "profile_picture_url": "https://cdn.example.com/docs/resume.pdf"
    }
    response = await async_client.put(
        f"/users/{admin_user.id}",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 422
    assert "valid image file" in response.text


@pytest.mark.asyncio
async def test_empty_payload_update(async_client, admin_user, admin_token):
    response = await async_client.put(
        f"/users/{admin_user.id}",
        json={},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code in (400, 422)
    assert "At least one field must be provided" in response.text
