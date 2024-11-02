from flask import Response, jsonify, make_response


class APIResponse:
    @staticmethod
    def respond(data=None, message="Success", status_code=200):
        response = {
            "message": message,
            "data": data
        }
        return response, status_code

    @staticmethod
    def respond_error(message="Error", status_code=400):
        response = {
            "message": message
        }
        return response, status_code
