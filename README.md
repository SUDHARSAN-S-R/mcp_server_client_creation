# mcp_server_client_creation

The server side provides the interaction layer that defines how the MCP tools should work and what operations can be performed.

On the client side, the system uses the Groq API to provide intelligence to the application. The client sends the request to the Groq model, and the model decides which tool should be used.

After that, the Python program on the server side executes the actual logic of the code and returns the result back to the client.
