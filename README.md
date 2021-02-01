# shifu
The Tao Governance dApp

## This is currently in beta. Use at your own risk.

Uses python, Django, and Postgres

## Sample .env
`
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=<postgres password>
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
PGDATA=/var/lib/postgresql/data
POSTGRES_DB=shifu
RPC_ENDPOINT=ws://some_tao_node:8546
RESTFUL_ENDPOINT=http://some_tao_node:8545
SECRET_KEY='<your secret django key'
`
## Install
`docker network create shifunet`
`docker-compose build shifu_web shifu_crawler`
`docker-compose up`
Don't forget to set `DEBUG=False` in settings.py
