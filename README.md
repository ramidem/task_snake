# task_snake

This whole REST API was created using ChatGPT as my way of learning Python

---

## API Docs with flasgger

Run the app locally, and go to [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

## TODOs

These were provided by ChatGPT and I decided to turn them into a to do list to be implemented in this app.

- [x] **Implement resource-based routing**: Map each resource to a specific endpoint, such as "/tasks" for a list of tasks.
- [x] **Implement HTTP methods**: Implement different HTTP methods, such as GET for retrieving a resource, POST for creating a resource, PUT for updating a resource, and DELETE for deleting a resource.
- [x] **Implement JSON format for requests and responses**: Make sure requests and responses are in JSON format and use the Flask `jsonify` function for returning JSON responses.
- [ ] **Implement error handling**:
    - [x] Return proper HTTP status codes for different types of errors (e.g. 404 for not found, 400 for bad request, 500 for internal server error)
    - [ ] Return descriptive error messages to help the client understand what went wrong
    - [ ] Handle exceptions properly and log errors for debugging purposes
    - [ ] Provide appropriate error handling for common errors, such as invalid input, resource not found, and unauthorized access
- [x] **Integrate with a database**: Use a database to store the API data and integrate it using SQLAlchemy.
- [ ] **Implement authentication and authorization**: Implement OAuth, JWT, or session-based authentication to secure the API.
- [x] **Implement API versioning**: Implement API versioning to maintain backward compatibility when making changes to the API. The API version can be included in the endpoint URL, such as "/v1/tasks".
- [x] **Document the API**: Document the API using Swagger or OpenAPI to make it easy for clients to understand how to use the API.

