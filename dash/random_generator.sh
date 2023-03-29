#!/bin/bash

# Remove the output directory
rm -fr /usr/share/staging/fhir/*

# Run the synthea command
java -jar /synthea/synthea-with-dependencies.jar Massachusetts -a 18-65 -c /synthea/src/main/resources/synthea.properties

# Print and OK message
echo "OK, random data generated"

# Run the Pathling command
python /dash/upload.py

# Print and OK message
echo "OK, data uploaded to Pathling"