# AuthenticationFileServer
Fastapi Based Authentication File Server
# Run on native PC
pip install -r requirements.txt

python3 main.py
# Run on docker
docker build -t fsimage .

sudo docker run -d --name fscontainer -p 8001:8001 fsimage
# Use  it
0. See all API on http://0.0.0.0:8001/docs#/ 
1. register an account using 'http://0.0.0.0:8001/auth/register'
2. Login 'http://0.0.0.0:8001/auth/jwt/login'
3. List your files  'http://0.0.0.0:8001/list' 
4. Upload/Modify a file 'http://0.0.0.0:8001/file_upload' 
5. Download a file 'http://0.0.0.0:8001/file_download/{filename}' 
6. Delete a file 'http://0.0.0.0:8001/file_delete/{filename}' 
