#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

echo "DEBUG: Argumentos recibidos: host=$host, cmd=$cmd"
echo "DEBUG: Variables de entorno:"
echo "  PGDATABASE=$PGDATABASE"
echo "  PGUSER=$PGUSER"
echo "  PGHOST=$PGHOST"

echo "DEBUG: Comando psql que se va a ejecutar:"
echo "PGPASSWORD=brunovalse psql --host=$host --username=bruno-valsecchi --dbname=scoutgine --command=\\q"

until PGPASSWORD=brunovalse psql --host="$host" --username=bruno-valsecchi --dbname=scoutgine --command='\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command: $cmd"
exec $cmd