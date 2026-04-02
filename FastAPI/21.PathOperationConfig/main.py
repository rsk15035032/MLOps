'''
FastAPI allows you to customize path operations directly in the decorator using several parameters:

status_code: Defines the HTTP response code (e.g., 201 CREATED). You can use fastapi.status constants for readability.
tags: Organize endpoints into groups for better API documentation. Can also be managed using Enum for consistency.
summary & description: Provide brief and detailed explanations of the endpoint.
Descriptions can also be written using docstrings with Markdown support.
response_description: Describes the response returned by the API (default: "Successful response").
deprecated: Marks an endpoint as deprecated without removing it.
'''

## refernce : https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#deprecate-a-path-operation