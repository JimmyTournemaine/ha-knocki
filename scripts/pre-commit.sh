#!/bin/bash

cd /workspaces/ha-core

# Définir la liste des éléments titre=>commande
declare -A liste
liste["Ruff"]="ruff --output-format=github homeassistant/components/knocki tests/components/knocki"
liste["Codespell"]="codespell --ignore-words-list 'hass' homeassistant/components/knocki tests/components/knocki"
liste["Hassfest"]="python -m script.hassfest --integration-path homeassistant/components/knocki --action validate"
liste["Mypy"]="mypy --no-error-summary homeassistant/components/knocki tests/components/knocki"
liste["Pylint"]="pylint --ignore-missing-annotations=y --ignore-wrong-coordinator-module=y homeassistant/components/knocki tests/components/knocki"
liste["Pytest"]="pytest tests/components/knocki --doctest-modules --cov=./homeassistant/components/knocki --cov-report=xml --cov-report=term"

# Parcourir la liste et exécuter les commandes
for titre in "${!liste[@]}"; do
    echo -n "$titre ... "
    output=$(eval "${liste[$titre]}" 2>&1)
    exit_status=$?

    if [ $exit_status -eq 0 ]; then
        echo -e "\033[32mOK\033[0m"
    else
        echo "$output"
        echo -e "$titre \033[31mKO\033[0m"
    fi
done
