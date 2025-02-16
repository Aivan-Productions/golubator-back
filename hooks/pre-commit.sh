#!/bin/bash

if ! command -v poetry &> /dev/null; then
	echo "No poetry in \$PATH, dont't edit pyproject.toml file, or install poetry"
	echo "(BTW this git hook auto-generates requirements.txt for pip in docker)"
	exit 1
fi

if ! poetry self show plugins | grep -q 'poetry-plugin-export'; then
    echo "No poetry-plugin-export plugin, install it to auto-generate requirements.txt file"
    echo "poetry self add poetry-plugin-export"
    exit 1
fi

if ! git diff --quiet HEAD^ HEAD -- pyproject.toml requirements.txt; then
	echo "Generating requirements.txt..."
	poetry export -f requirements.txt --output requirements.txt &> /dev/null
	git add .
fi
