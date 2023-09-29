run:
	docker-compose up -d

down:
	docker-compose down

build: 
	make build-back;
	make build-front;

build-back:
	docker-compose run --rm web bash -c "pip install -r requirements.txt"

build-front: 
	docker-compose run --rm front node --version

local-dev:
	docker-compose run --rm web bash -c "cd docker/bash && run_web.sh"