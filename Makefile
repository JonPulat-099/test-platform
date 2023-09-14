run:
	sudo docker-compose up -d --build
down:
	sudo docker-compose down
build: 
	make build-back;
	make build-front;

build-back:
	docker-compose run --rm web bash -c "echo 'test'"

build-front: 
	docker-compose run --rm front node --version