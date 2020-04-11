# Py-restfull
Um micro web framework feito em python, para utilizar alguns conhecimentos. 


## Dependências

* Python 3.8.x
* Pipenv - Gerenciador de pacotes python - https://docs.pipenv.org

### Como usar?
Você pode usar com pipenv or docker. 
 

#### Pipenv

1 - Crie seu ambiente

```bash
pipenv --python 3.8
```
2 -  Instale os pré-requisitos
```bash
pipenv install
```
3 - Na raiz do projeto crie um arquivo .env e adicione os dados abaixo 
```code
DATABASE_NAME=<name do seu banco>
DATABASE_USERNAME=<user do seu banconame>
DATABASE_PASSWORD=<your datababse password>
DATABASE_HOST=<host do seu banco>
DATABASE_PORT=<host do seu banco>
```
[P.S.: Necessário mongodb instalado e configurado para rodar o projeto.]

4 - Utilize o comando abaixo para rodar a API: 
```bash
pipenv shell
python app.py
```

#### Docker 
**warning**: não implementado ainda

1 - Ter instalado docker e docker-compose


2 - Na raiz do projeto crie um arquivo .env e adicione os dados abaixo 
```code
DATABASE_NAME=local_db
DATABASE_USERNAME=local_db
DATABASE_PASSWORD=local_db
DATABASE_HOST=db
DATABASE_PORT=port
```