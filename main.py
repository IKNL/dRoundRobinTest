""" Main.py

This is the main entry-point when the docker-container is initialized.
It executes the following steps:

1) read the input.txt
    This should contain the name of the method that should be executed.
    Optionally it contains some args and kwargs
2) The token is read from token.txt This is a JWT token that can be 
    used to interact with the server and used by my_turn to identify
    the node it is running on
3) The method is executed
4) The output it written to output.txt

If the docker container is terminated. output.txt will be send to the 
server by the node.
"""
import json
import os
import sys

from roundrobintest import master, my_turn, info, warn

# read input from the mounted inputfile
info("Reading input")
with open("app/input.txt") as fp:
    input_ = json.loads(fp.read())

# determine function from input, summarize is used by default.
# and get the args and kwargs input for this function
method_name = input_.get("method", "my_turn")
method = {
    "my_turn": my_turn,
    "master": master
}.get(method_name)
if not method:
    warn(f"method name={method_name} not found!\n")
    exit()

# both the master (central) and node algorithm require a token
info("Reading token")
with open("app/token.txt") as fp:
    token = fp.read().strip()
    
# call the actual function
output = method(token)

# write output to mounted output file
info("Writing output")
with open("app/output.txt", 'w') as fp:
    fp.write(json.dumps(output))
