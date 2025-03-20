#! /bin/bash

GR='\033[0;32m'
NC='\033[0m'
source .env >/dev/null

echo -n "What is the structure's name: "
read -r struc_name
echo -n "Output file's name: "
read -r output
echo "Is it a SAS BS ?"
echo -n "y/n: "
read -r sas
echo "Do you want to generate a docx file ?"
echo -n "y/n: "
read -r docx

if [ "$sas" == "y" ]; then
    sas="--sas"
else
    sas=""
fi

if [ "$docx" == "y" ]; then
    docx="--docx"
else
    docx=""
fi

echo -e "${GR}Check if a new docker image is available${NC}"
docker pull ghcr.io/extauren/bs_generator:latest
echo -e "${GR}PDF is generating, please wait...${NC}"
docker run --env-file .env --name bs_generator ghcr.io/extauren/bs_generator:latest python bs_generator.py -s "$struc_name" -n "$output" $docx $sas
docker cp bs_generator:/app/$output.pdf "$FOLDER_OUTPUT"
if [ -n "$docx" ]; then
    docker cp bs_generator:/app/$output.docx "$FOLDER_OUTPUT"
fi
docker rm bs_generator