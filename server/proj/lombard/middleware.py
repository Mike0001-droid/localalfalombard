import json
import logging
import typing as typ

from django.http import HttpRequest, HttpResponse

from utils.transport.rest import TicketResponseValidator


logger = logging.getLogger('debug')


class ValidateExternalApiResponse:
    def __init__(self, get_response: typ.Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        requested_uri = request.build_absolute_uri()
        response: HttpResponse = self.get_response(request)
        if requested_uri.endswith('/get_tickets/') or requested_uri.endswith('/get_ticket_info/'):
            response_data: dict = json.loads(response.content)
            validate_service = TicketResponseValidator(response_data)
            validate_service.validate()
            response.content = json.dumps(response_data)
        return response
