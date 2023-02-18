# data-engineering-sandbox
This repo contains the full stack environment based on docker for a modern data engineering project and useful for technical interviews too.

- [Setup](#local-setup)
- [Development](#development)

## Local Setup
Please be sure that you have already installed docker and docker-compose on your linux enviroment. You can run this comand:

```bash
sudo docker version && docker-compose version
```
Modifique the .env file with your own enviroment variables:

```bash
mv .env_example .env
```

## development
This sandbox contaim the follows elements:

-   Airflow, as a pipeline orchestactor.
-   Minio, as a S3 bucket.
-   Mysql, as a relational database.

The airflow folder has the filesystem and a example pipeline for test all the enviroment called `test_conections.py`. Also has the dumdata folder with a test dataset.

You will need to create all the conections using the airlow webserver, for that acess this url  `http://127.0.0.1:8080/`consider this instructions:

Conect with the Mysql database on container, you can acess the container `sudo docker exec -it data-engineering-sandbox-db-1 bash`  and acess the mysql `mysql -u root -p` for create you database and then create the connection:

```bash
host: 172.17.0.1
schema: your-database
login: root
port: 3306
```
You can access minio with this url `http://localhost:9001/`, to create a connection on airflow use this variables:
```bash
extra: {"aws_access_key_id": "minio_access_key", "aws_secret_access_key": "minio_secret_key", "host": "http://127.0.0.1:9000"}
```