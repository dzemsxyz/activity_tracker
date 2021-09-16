from typing import List, Type

from django.db.models.base import Model
from events_library.utils import Service, declare_event

from .core import ActivityTracker


def declare_activity_event(
    event_name: str,
    model_class: Type[Model],
    tracked_fields: List[str],
    additional_fields: List[str],
) -> None:
    """Tracks field changes of the given model on every update or create
    and sends them to the activities service

    Arguments:
        event_name: str
            The name of the event that will be emitted
        model_class: dict
            Model to be tracked
        tracked_fields: dict
            Any changes on this set of fields will trigger the event and send the changes
        additional_fields: dict
            Additional fields to be sent needed for the activity log message
    """

    declare_event(event_name, (Service.ACTIVITIES,))

    ActivityTracker.track_changes(
        event_name, model_class, tracked_fields, additional_fields
    )
