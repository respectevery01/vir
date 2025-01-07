#!/bin/bash

# Create necessary directories
mkdir -p public/assets

# Copy static files
cp -r assets/* public/assets/
cp app.js public/
cp styles.css public/
cp index.html public/ 