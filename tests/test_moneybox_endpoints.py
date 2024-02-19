"""All moneybox endpoint tests are located here."""

import pytest
from httpx import AsyncClient

from src.custom_types import EndpointRouteType
from src.db.db_manager import DBManager


@pytest.mark.dependency(depends=["tests/test_db_manager.py::test_delete_moneybox"], scope="session")
async def test_endpoint_get_moneybox(client: AsyncClient) -> None:
    response = await client.get(
        f"/{EndpointRouteType.APP_ROOT}/{EndpointRouteType.MONEYBOX}/1",
    )
    expected_moneybox_data = {"name": "Test Box 1 - Updated", "id": 1, "balance": 0}

    assert response.status_code == 200
    assert response.json() == expected_moneybox_data


@pytest.mark.dependency(depends=["tests/test_db_manager.py::test_delete_moneybox"], scope="session")
async def test_endpoint_get_moneyboxes(db_manager: DBManager, client: AsyncClient) -> None:
    response = await client.get(
        f"/{EndpointRouteType.APP_ROOT}/{EndpointRouteType.MONEYBOXES}",
    )
    expected_moneyboxes = {
        "total": 3,
        "moneyboxes": [
            {"name": "Test Box 1 - Updated", "id": 1, "balance": 0},
            {"name": "Test Box 3", "id": 3, "balance": 333},
            {"name": "Test Box 4", "id": 4, "balance": 0},
        ],
    }
    moneyboxes = response.json()

    assert response.status_code == 200
    assert moneyboxes == expected_moneyboxes

    # delete money all boxes
    await db_manager.delete_moneybox(moneybox_id=1)
    await db_manager.delete_moneybox(moneybox_id=3)
    await db_manager.delete_moneybox(moneybox_id=4)

    response = await client.get(
        f"/{EndpointRouteType.APP_ROOT}/{EndpointRouteType.MONEYBOXES}",
    )

    assert response.status_code == 204

    # re-add deleted moneyboxes
    await db_manager.add_moneybox(moneybox_data=moneyboxes["moneyboxes"][0])
    await db_manager.add_moneybox(moneybox_data=moneyboxes["moneyboxes"][1])
    await db_manager.add_moneybox(moneybox_data=moneyboxes["moneyboxes"][2])

    response = await client.get(
        f"/{EndpointRouteType.APP_ROOT}/{EndpointRouteType.MONEYBOXES}",
    )

    # test to ensure if moneyboxes were added
    assert response.status_code == 200
    assert response.json() == expected_moneyboxes
