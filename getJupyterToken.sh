#!/bin/bash
## This script returns the Token value to be inserted in the Jupyter server

urlToken=$(docker logs biospytial_client_1 | grep -m 1 token );

Token=$(echo $urlToken | awk -F "=" '{print $2 }');

echo "Use this token: "$Token
