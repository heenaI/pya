CREATE DATABASE Liebkreis;
CREATE USER scheduler_user WITH ENCRYPTED PASSWORD 'MeraPassword880677!';


postgresql://hina:MeraPassword880677!@localhost/Liebkreis
docker exec -it liebkreis_db psql -U hina -d Liebkreis