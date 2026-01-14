import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="HelloWorld")
def HelloWorld(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP trigger function that returns a personalized greeting.

    Query Parameters:
        name (optional): Name to include in greeting

    Request Body (JSON):
        name (optional): Name to include in greeting

    Returns:
        200 OK with greeting message
    """
    logging.info('Python HTTP trigger function processed a request.')

    # Try to get name from query string first
    name = req.params.get('name')

    # If not in query string, try request body
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    # Return personalized greeting or default message
    if name:
        return func.HttpResponse(
            f"Hello, {name}! This HTTP triggered function executed successfully.",
            status_code=200
        )
    else:
        return func.HttpResponse(
            "Hello! This HTTP triggered function executed successfully. "
            "Pass a name in the query string (e.g., ?name=Azure) or in the request body for a personalized response.",
            status_code=200
        )
