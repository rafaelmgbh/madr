from http import HTTPStatus


def test_criar_romancista(client, user, token):
    response = client.post(
        "/romancistas/",
        headers={"Authorization": f"Bearer {token}"},
        json={"nome": "Machado de Assis"},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"nome": "Machado de Assis", "id": 1}


def test_criar_romancista_ja_existente(client, token, romancista):
    response = client.post(
        "/romancistas/",
        headers={"Authorization": f"Bearer {token}"},
        json={"nome": romancista.nome},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_listar_romancistas(client, romancista, user, token):
    response = client.get(
        "/romancistas/", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "romancistas": [{"nome": romancista.nome, "id": 1}]
    }


def test_excluir_romancista(client, romancista, user, token):
    response = client.delete(
        f"/romancistas/{romancista.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"mensagem": "Romancista excluído com sucesso."}


def test_excluir_romancista_que_nao_existe(client, user, token):
    response = client.delete(
        "/romancistas/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Romancista não encontrado"}


def test_editar_romancista(client, romancista, user, token):
    response = client.patch(
        f"/romancistas/{romancista.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"nome": "Machado de Assis"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"nome": "Machado de Assis", "id": 1}


def test_editar_romancista_que_nao_existe(client, user, token):
    response = client.patch(
        "/romancistas/1",
        headers={"Authorization": f"Bearer {token}"},
        json={"nome": "Machado de Assis"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Romancista não encontrado."}
