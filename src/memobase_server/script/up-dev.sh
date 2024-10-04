set -e
docker-compose up memobase-server-db memobase-server-redis
rm -rf ./db/data
rm -rf ./db/redis