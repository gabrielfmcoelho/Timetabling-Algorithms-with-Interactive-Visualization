echo ">>---------------------<<"
echo "Setting up $1 project"
echo "Environment in $2 mode"
echo "---------------------"
echo "API Project Info"
echo "> PORT: $3"
echo "> VERSION: $5"
echo "---------------------"
echo "FRONTEND Project Info"
echo "> PORT: $4"
echo "> VERSION: $6"
echo "---------------------"
echo "CORS Configurations"
echo "> ORIGINS: ${7}"
echo "> CREDENTIALS: ${8}"
echo "> METHODS: ${9}"
echo "> HEADERS: ${10}"
echo ">>---------------------<<"

cp config/templates/.env.tpl .env
sed -i "s/(PROJECT_NAME)/$1/g" .env
sed -i "s/(MODE)/$2/g" .env
sed -i "s/(API_PORT)/$3/g" .env
sed -i "s/(FRONTEND_PORT)/$4/g" .env
sed -i "s/(API_VERSION)/$5/g" .env
sed -i "s/(FRONTEND_VERSION)/$6/g" .env
sed -i "s/(CORS_ALLOW_ORIGINS)/${7}/g" .env
sed -i "s/(CORS_ALLOW_CREDENTIALS)/${8}/g" .env
sed -i "s/(CORS_ALLOW_METHODS)/${9}/g" .env
sed -i "s/(CORS_ALLOW_HEADERS)/${10}/g" .env

cp config/templates/Dockerfile.api.tpl Dockerfile.api
sed -i "s/(API_PORT)/$3/g" Dockerfile.api

cp config/templates/Dockerfile.frontend.tpl Dockerfile.frontend
sed -i "s/(FRONTEND_PORT)/$4/g" Dockerfile.frontend

cp config/templates/docker-compose.yml.tpl docker-compose.yml
sed -i "s/(PROJECT_NAME)/$1/g" docker-compose.yml
sed -i "s/(API_PORT)/$3/g" docker-compose.yml
sed -i "s/(FRONTEND_PORT)/$4/g" docker-compose.yml