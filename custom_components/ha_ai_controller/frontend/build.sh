#!/bin/bash

# Install dependencies
npm install

# Build the React app
npm run build

# Create the static directory if it doesn't exist
mkdir -p build/static/js

# Copy only the JS files since we're not generating CSS
cp build/static/js/main.*.js build/static/js/main.js
