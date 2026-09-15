# Criar container

    docker run --name pg-docker -e POSTGRES_PASSWORD=escolhaumasenha -d -p 5432:5432 -v ${HOME}/docker/volumes/postgres:/var/lib/postgresql postgres