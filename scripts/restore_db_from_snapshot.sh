#!/usr/bin/env bash

dropdb -U $POSTGRES_USER $POSTGRES_DB
createdb -U $POSTGRES_USER $POSTGRES_DB
psql -U $POSTGRES_USER $POSTGRES_DB < /app/snapshots/db_snapshot.sql
