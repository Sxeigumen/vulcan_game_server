FROM postgres:15.3-bookworm

ADD ./SQL_server/init.sql /docker-entrypoint-initdb.d/