# ComunicationLTD

To set up the virtual environment:
C:\Users\Eden\Desktop\securityProject>  
1) python -m venv env  
2) env\Scripts\activate  

To install packages in requirements.txt:   
1) pip install -r requirements.txt   
2) OR do it manually :)  


SQL:  
1) docker-compose up -d  

Commands for shell:   
2) docker exec -it 45c63302dbbe bash -l  
3) mysql -h 127.0.0.1 -u root -p communication  
4) password: Qazqazwsx1  

use communication;  
SHOW TABLES;  
SELECT * FROM users_users;  

If the 3306 port is already allocated by Docker Compose, open an administrator shell and run the following commands:  
1) netstat -ano | findstr :3306  
2) taskkill /PID 3306 /F  

To run the server with tls:  
```python 
python manage.py runsslserver --certificate .\RootCA.pem --key .\RootCA.key
```
DJANGO admin panel:  
1) username: admin@gmail.com  
2) password: 5Q6O0Lot*8Da  
