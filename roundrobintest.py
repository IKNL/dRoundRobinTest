import os
import sys
import time
import json
import jwt
import requests

from pytaskmanager.node.server_io import ClientContainerProtocol

# loggers
info = lambda msg: sys.stdout.write("info > "+msg+"\n")
warn = lambda msg: sys.stdout.write("warn > "+msg+"\n")

def master(token):
    """Master algoritm.
    
    The master algorithm is the chair of the Round Robin, which makes 
    sure everyone waits for their turn to identify themselfs.

    Keyword arguments:
    token -- JWT token to access the central server
    """

    # post task to all nodes in collaboration, the environment variables
    # are set by the node instance
    info("Setup (proxy)server communication client")

    client = ClientContainerProtocol(
        token=token, 
        host=os.environ["HOST"],
        port=os.environ["PORT"], 
        path=os.environ["API_PATH"]
    )

    # get all organizations (ids) that are within the collaboration
    # FlaskIO knows the collaboration to which the container belongs
    # as this is encoded in the JWT (Bearer token)
    organizations = client.get_organizations_in_my_collaboration()
    ids = [organization.get("id") for organization in organizations]

    # The input fot the algorithm is the same for all organizations
    # in this case  
    info("Defining input paramaeters")
    input_ = {
        "method": "my_turn",
    }

    # send the task subsequently to all organizations
    messages = []
    for id_ in ids:

        info(f"Giving the turn to organization_id={id_}")

        # collaboration and image is stored in the key, so we do not need
        # to specify these (this is handled by FlaskIO)
        info("Creating node task")
        task = client.create_new_task(
            input_=input_, 
            organization_ids=[id_]
        )


        # wait for node to return results. Instead of polling it is also
        # possible to subscribe to a websocket channel to get status
        # updates
        task_id = task.get("id")
        task = client.request(f"task/{task_id}")
        while not task.get("complete"):
            task = client.request(f"task/{task_id}")
            info("Waiting for results")
            time.sleep(1)

        info("Obtaining results")
        results = client.get_results(task_id=task.get("id"))
        results = [json.loads(result.get("result")) for result in results]
        messages.append(results.pop())

        info("master algorithm complete")

    # return all the messages from the nodes
    return messages

def my_turn(token):
    """Node algorithm.
    
    Uses the token to identify the node to the server.

    Keyword arguments:
    token -- JWT token to access the central server
    """
    
    # decode public part of the JWT (we do not have or need the secret)
    claims = jwt.decode(token, verify=False)
    return claims.get("identity")
