#! /bin/bash

struc_name=$1
output=$2
docx=$3
GR='\033[0;32m'
NC='\033[0m'
source .env >/dev/null

echo -e "${GR}Check if a new docker image is available${NC}"
docker pull ghcr.io/extauren/bs_generator:latest
echo -e "${GR}PDF is generating, please wait...${NC}"
docker run  -v "./pappers.json:/app/pappers.json:ro" --env-file .env --name bs_generator ghcr.io/extauren/bs_generator:latest python bs_generator.py -s "$struc_name" -n "$output" $docx
docker cp bs_generator:/app/$output.pdf "$FOLDER_OUTPUT"
if [ -n "$docx" ]; then
    docker cp bs_generator:/app/$output.docx "$FOLDER_OUTPUT"
fi
docker rm bs_generator