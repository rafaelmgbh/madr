from http import HTTPStatus


def test_criar_romancista(client):
    response = client.post(
        "/romancistas/",
        json={"nome": "Machado de Assis"},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"nome": "Machado de Assis", "id": 1}


def test_criar_romancista_ja_existente(client, romancista):
    response = client.post(
        "/romancistas/",
        json={"nome": romancista.nome},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_listar_romancistas(client, romancista):
    response = client.get("/romancistas/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "romancistas": [{"nome": romancista.nome, "id": 1}]
    }


def test_excluir_romancista(client, romancista):
    response = client.delete(f"/romancistas/{romancista.id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"mensagem": "Romancista excluído com sucesso."}


def test_excluir_romancista_que_nao_existe(client):
    response = client.delete("/romancistas/1")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Romancista não encontrado"}
