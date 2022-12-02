import logging
import requests
from typing import Callable

from django.conf import settings
from rest_framework import status
from chats.apps.api.v1.internal.internal_authorization import InternalAuthentication

LOGGER = logging.getLogger(__name__)


def retry_request_and_refresh_flows_auth_token(
    project,
    request_method: Callable,
    headers: dict,
    url: str,
    params: dict = None,
    json=None,
    user_email: str = "",
    retries: int = settings.FLOWS_AUTH_TOKEN_RETRIES,
):
    for _ in range(0, retries):
        response = request_method(url=url, params=params, json=json, headers=headers)
        if response.status_code in [401, 403]:
            headers["Authorization"] = project.set_flows_project_auth_token(
                user_email=user_email
            )
        else:
            break
    return response


class FlowsContactsAndGroupsMixin:
    def project_headers(self, token):
        headers = {
            "Content-Type": "application/json; charset: utf-8",
            "Authorization": f"Token {token}",
        }
        return headers

    def list_contacts(self, project):
        response = retry_request_and_refresh_flows_auth_token(
            project=project,
            request_method=requests.get,
            headers=self.project_headers(project.flows_authorization),
            url=f"{self.base_url}/api/v2/contacts.json",
            user_email=project.random_admin.user.email,
        )
        return response.json()

    def create_contact(self, project, data: dict):
        response = retry_request_and_refresh_flows_auth_token(
            project=project,
            user_email=project.permissions.random_admin.user.email,
            request_method=requests.post,
            url=f"{self.base_url}/api/v2/contacts.json",
            json=data,
            headers=self.project_headers(project.flows_authorization),
        )
        return response.json()

    def list_contact_groups(self, project):
        response = retry_request_and_refresh_flows_auth_token(
            project=project,
            request_method=requests.get,
            headers=self.project_headers(project.flows_authorization),
            url=f"{self.base_url}/api/v2/groups.json",
            user_email=project.permissions.random_admin.user.email,
        )
        return response.json()


class FlowRESTClient(InternalAuthentication, FlowsContactsAndGroupsMixin):
    def __init__(self, *args, **kwargs):
        self.base_url = settings.FLOWS_API_URL

    def create_queue(self, uuid: str, name: str, sector_uuid: str):
        response = requests.post(
            url=f"{self.base_url}/api/v2/internals/ticketers/{sector_uuid}/queues/",
            headers=self.headers,
            json={"uuid": uuid, "name": name},
        )
        if response.status_code not in [
            status.HTTP_200_OK,
            status.HTTP_201_CREATED,
            status.HTTP_204_NO_CONTENT,
        ]:
            LOGGER.debug(
                f"[{response.status_code}] Failed to create the queue.  response: {response.content}"
            )
        return response

    def update_queue(self, uuid: str, name: str, sector_uuid: str):
        response = requests.patch(
            url=f"{self.base_url}/api/v2/internals/ticketers/{sector_uuid}/queues/{uuid}/",
            headers=self.headers,
            json={"name": name},
        )
        if response.status_code not in [
            status.HTTP_200_OK,
            status.HTTP_201_CREATED,
            status.HTTP_204_NO_CONTENT,
        ]:
            LOGGER.debug(
                f"[{response.status_code}] Failed to update the queue. response: {response.content}"
            )
        return response

    def destroy_queue(self, uuid: str, sector_uuid: str):
        response = requests.delete(
            url=f"{self.base_url}/api/v2/internals/ticketers/{sector_uuid}/queues/{uuid}/",
            headers=self.headers,
        )

        if response.status_code not in [
            status.HTTP_200_OK,
            status.HTTP_201_CREATED,
            status.HTTP_204_NO_CONTENT,
        ]:
            LOGGER.debug(
                f"[{response.status_code}] Failed to delete the queue. response: {response.content}"
            )
        return response
