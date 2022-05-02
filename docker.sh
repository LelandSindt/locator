docker image build . -t locator:local
docker container rm -f locator
docker container run --detach --restart always --name locator --env-file settings.env --volume ${PWD}/cookies-google-com.txt:/usr/src/app/cookies-google-com.txt locator:local
