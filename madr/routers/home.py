from fastapi import APIRouter
from starlette.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Minha Apresentação</title>
        <style>
            body {
                font-family: sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                color: #333;
            }
            .container {
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #fff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 5px;
            }
            h1 {
                text-align: center;
                color: #333;
            }
            p {
                line-height: 1.6;
            }
            .link {
                display: block;
                text-align: center;
                margin-top: 20px;
            }
            a {
                color: #007bff;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Olá! Eu sou Rafael Santos de Araujo</h1>
            <p>Sou um desenvolvedor apaixonado por criar soluções web eficientes e inovadoras. 
            Tenho experiência em Python e FastAPI, e estou sempre buscando aprender novas tecnologias 
            e aprimorar minhas habilidades.</p>

            <p>O MADR é uma API desenvolvida com FastAPI para gerenciar um acervo digital de romances. Ela permite operações de CRUD (criar, ler, atualizar e deletar) para livros e romancistas, além de incluir o registro de contas e autenticação para operações específicas. No projeto cada usuário possui uma conta (protegida pro e-mail/senha). Depois que está "dentro" da conta (ou seja, authenticado com um JWT), o usuário pode criar/ler/atualizar/excluir romancistas e livros que queira guardar no acervo.</p>

            <div class="link">
                <a href="/docs">Acesse a documentação da API</a>
            </div>
            
             <div class="link">
                <a href="https://github.com/rafaelmgbh" target="_blank">Meu GitHub</a> 
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
