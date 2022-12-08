import logging

from .micloudexception import MiCloudException
from .miutils import get_session

# A dictionary consisting of miot standard types and their singular form
MIOT_STANDARD_TYPES = {
    "devices": "device",
    "services": "service",
    "properties": "property",
    "actions": "action",
    "events": "event",
}

_LOGGER = logging.getLogger(__name__)


class MiotSpec:
    """Simple wrapper for accessing miot-spec.org web service.

    You can pass an existing requests.Session object using *session* to each class method,
    otherwise a new session is created using :meth:`micloud.miutils.get_session`.

    :meth:`get_specs` returns a list of all available specs with their version and urn information.
    The latter can be used with :meth:`get_spec_for_urn` to obtain a full miotspec schema.
    """

    BASE_URL = "https://miot-spec.org/miot-spec-v2"

    @classmethod
    def get_specs(cls, status="released", session=None):
        """Return information about all available miotspec implementations.

        Note that every model may appear multiple times using different version in the response.

        Use :meth:`miot_get_schema_for_urn` to download the miotspec schema file based on the urn.

        :param status: filter by status, "released", "debug", "preview", "all", defaults to "released"
        """
        if session is None:
            session = get_session()

        url = f"{cls.BASE_URL}/instances?status={status}"

        AVAILABLE_STATUSES = ["released", "debug", "preview", "all"]
        if status not in AVAILABLE_STATUSES:
            raise MiCloudException("Unknown release status %s" % status)

        _LOGGER.debug("Going to download specs listing with status %s" % status)

        response = session.get(url)
        return response.json()

    @classmethod
    def get_spec_for_urn(cls, device_urn: str, session=None):
        """Return miotspec device schema for the given device URN.

        The returned dict contains information about all services, properties, actions, events etc.
        the device has been reported to support.

        :meth:`miot_get_available_schemas` can be used to return a list of all available URNs.
        """
        if session is None:
            session = get_session()

        _LOGGER.debug("Going to download a spec for %s" % device_urn)

        url = f"{cls.BASE_URL}/instance?type={device_urn}"

        response = session.get(url)
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_standard_types(cls, type_: str, session=None):
        """Return standardized URNs for a given type.

        The type can be either devices, services, properties, actions, or events.
        """
        if type_ not in MIOT_STANDARD_TYPES:
            raise MiCloudException("Invalid schema type requested: %s" % type_)

        if session is None:
            session = get_session()

        url = f"{cls.BASE_URL}/spec/{type_}"

        _LOGGER.debug("Going to download definition for type %s" % type_)

        response = session.get(url)
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_standard_type_spec(cls, type_urn: str, session=None):
        """Return a schema for a standard type URN.

        The response depends on the requested type and contains metadata about
        the elements the given standard type must and can implement.
        """
        splitted_urn = type_urn.split(":")
        spec_type = splitted_urn[2]
        namespace = splitted_urn[1]
        if namespace != "miot-spec-v2":
            raise MiCloudException(
                "Tried to fetch spec for non-standard namespace %s" % namespace
            )

        if session is None:
            session = get_session()

        url = f"{cls.BASE_URL}/spec/{spec_type}?type={type_urn}"

        response = session.get(url)
        response.raise_for_status()
        return response.json()
