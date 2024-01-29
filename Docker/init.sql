DROP ROLE IF EXISTS nipohc_user;
CREATE ROLE nipohc_user WITH LOGIN ENCRYPTED PASSWORD 'password';;

CREATE DATABASE nipohc;
GRANT ALL PRIVILEGES ON DATABASE nipohc TO nipohc_user;
ALTER DATABASE nipohc OWNER TO nipohc_user;

DROP ROLE IF EXISTS nipohc_test_user;
CREATE ROLE nipohc_test_user WITH LOGIN ENCRYPTED PASSWORD 'password';

CREATE DATABASE nipohc_test;
GRANT ALL PRIVILEGES ON DATABASE nipohc_test TO nipohc_test_user;
ALTER DATABASE nipohc_test OWNER TO nipohc_test_user;
