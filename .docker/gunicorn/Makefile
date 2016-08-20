NAMESPACE=brandsocial
APP=base
TAG=python3.5

build:
	docker build --no-cache=true -t ${NAMESPACE}/${APP}:${TAG} .
run:
	docker run --name=${APP} --detach=true ${NAMESPACE}/${APP}:${TAG}
clean:
	docker stop ${APP} && docker rm ${APP}
reset: clean
	docker rmi ${NAMESPACE}/${APP}:${TAG}
ssh:
	docker run --rm --interactive --tty --name=${APP} ${NAMESPACE}/${APP} zsh

push:
	docker push ${NAMESPACE}/${APP}:${TAG}
