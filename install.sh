#!/bin/bash

# Clone the repository
git clone https://github.com/coqui-ai/TTS .

# Move into the repository directory
cd TTS

# Run pip install
pip install -e .[all]

# Go back to the root directory
cd ..

# Install app
pip install -e .[development]