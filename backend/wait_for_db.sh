#!/bin/sh

until pg_isready -h db -U bruno-valsecchi -d pruebasscoutgine_db; do
  echo "Waiting for PostgreSQL to become available..."
  sleep 2
done
echo "PostgreSQL is ready!"