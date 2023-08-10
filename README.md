## Config File 

This script compares the prices on mousehunt discord and offical marketplace to determine potential profits

A secret file (secret.txt) containing discord Authorization is required 

A cookie file (cookie.txt) containing mousehunt cookie is required 

A tele file (tele.txt) containing telegram token

## Docker

To run on discord, the following command are required \

docker build -t mousehunt . 

docker run --restart always mousehunt
