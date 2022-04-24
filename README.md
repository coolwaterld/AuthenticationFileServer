# AuthenticationFileServer
Fastapi Based Authentication File Server
# Run on native PC
pip install -r requirements.txt

python3 main.py
# Run on docker
docker build -t fsimage .

sudo docker run -d --name fscontainer -p 8001:8001 fsimage
