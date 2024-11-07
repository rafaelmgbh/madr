from http import HTTPStatus


def test_criar_livro(client, user, token, romancista):
    response = client.post(
        "/livros/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "titulo": "Dom Casmurro",
            "romancista_id": romancista.id,
            "ano": 1899,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "titulo": "Dom Casmurro",
        "romancista_id": romancista.id,
        "ano": 1899,
        "id": 1,
    }


def test_criar_romancista_inexistente(client, token):
    response = client.post(
        "/livros/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "titulo": "Dom Casmurro",
            "romancista_id": 1,
            "ano": 1899,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Romancista não encontrado"}


def test_listar_livros(client, user, token, romancista):
    client.post(
        "/livros/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "titulo": "Dom Casmurro",
            "romancista_id": romancista.id,
            "ano": 1899,
        },
    )
    response = client.get(
        "/livros/", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "livros": [
            {
                "titulo": "Dom Casmurro",
                "romancista_id": romancista.id,
                "ano": 1899,
                "id": 1,
            }
        ]
    }


def test_excluir_livro(client, user, token, romancista):
    response = client.post(
        "/livros/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "titulo": "Dom Casmurro",
            "romancista_id": romancista.id,
            "ano": 1899,
        },
    )
    response = client.delete(
        "/livros/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"mensagem": "Livro deletado com sucesso"}


def test_exluir_livro_nao_existe(client, user, token):
    response = client.delete(
        "/livros/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Livro não encontrado"}
