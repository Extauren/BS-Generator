#! /bin/bash

struc_name=$1
output=$2
docx=$3
source .env >/dev/null


docker pull ghcr.io/extauren/bs_generator:latest
docker run -v "./pappers.json:/app/pappers.json:ro" --env-file .env --name bs_generator ghcr.io/extauren/bs_generator:latest python bs_generator.py -s "$struc_name" -n "$output" $docx
docker cp bs_generator:/app/$output.pdf "$FOLDER_OUTPUT"
if [ -n "$docx" ]; then
    docker cp bs_generator:/app/$output.docx "$FOLDER_OUTPUT"
fi
docker rm bs_generator >/dev/null