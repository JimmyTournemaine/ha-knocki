#!/bin/bash

cd /workspaces/ha-core

echo -e "Ruff...\r\c"
ruff --output-format=github homeassistant/components/knocki tests/components/knocki \
    && echo -e "\rRuff...OK" \
    || echo -e "\rRuff...KO"

echo -e "Codespell...\r\c"
codespell --ignore-words-list 'hass' homeassistant/components/knocki tests/components/knocki\
    && echo -e "\rCodespell...OK" \
    || echo -e "\rCodespell...KO"

echo -e "Mypy...\r\c"
mypy --no-error-summary homeassistant/components/knocki tests/components/knocki\
    && echo -e "\rMypy...OK" \
    || echo -e "\rMypy...KO"

echo -e "Pylint...\r\c"
pylint --ignore-missing-annotations=y --ignore-wrong-coordinator-module=y homeassistant/components/knocki tests/components/knocki\
    && echo -e "\rPylint...OK" \
    || echo -e "\rPylint...KO"

echo -e "Hassfest...\r\c"
python -m script.hassfest --integration-path homeassistant/components/knocki --action validate \
    && echo -e "\rHassfest...OK" \
    || echo -e "\rHassfest...KO"

echo -e "Pytest...\r\c"
pytest tests/components/knocki --doctest-modules \
    --cov=./homeassistant/components/knocki --cov-report=xml --cov-report=term \
    && echo -e "\rPytest...OK" \
    || echo -e "\rPytest...KO"
sed -i 's|<source>/workspaces/ha-knocki/knocki|<source>/workspaces/ha-core/homeassistant/components/knocki|g' coverage.xml
