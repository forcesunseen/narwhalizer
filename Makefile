build:
	docker build . -t narwhalizer

run: 
	docker run -it -v ${PWD}/data:/app/data --env-file $(env) narwhalizer

dev:
	docker run -it -v ${PWD}/data:/app/data -v ${PWD}/generate:/app/generate --env-file $(env) narwhalizer
