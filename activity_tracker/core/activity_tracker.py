import logging
import time
from typing import List, Type

from django.db.models.base import Model
from django.db.models.signals import post_save
from events_library.utils import emit
from rest_framework.serializers import ModelSerializer


class ActivityTracker:
    @classmethod
    def track_changes(
        cls,
        event_name: str,
        model_class: Type[Model],
        tracked_fields: List[str],
        additional_fields: List[str],
    ):
        """Attaches to the model_class post_save signal,
        which emits the appropiate activity event to the activities service"""

        class GenericSerializer(ModelSerializer):
            """Serializer that extends ModelSerializer"""

            class Meta:
                model = model_class
                fields = "__all__"

        def handle_upsert(instance, created, **kwargs):

            if not hasattr(instance, "tracker"):
                raise AttributeError("Model is missing the tracker field")

            # Returns dictionary which contains previous state of changed fields
            # On create returns all fields that are not None
            changed_fields = instance.tracker.changed()

            tracked_fields_set = set(tracked_fields)
            changed_fields_set = set(changed_fields)

            if tracked_fields_set.intersection(changed_fields_set):
                changed_fields_payload = {}
                data = GenericSerializer(instance).data

                for field in tracked_fields:
                    if field in changed_fields:
                        changed_fields_payload[field] = {
                            "from": changed_fields[field],
                            "to": data[field],
                        }

                data_payload = {
                    key: data[key] for key in additional_fields if key in data
                }

                payload = {
                    "instance_id": instance.id,
                    "profile_id": instance.get_owner_profile_id(),
                    "timestamp": time.time(),
                    "properties": {
                        "changed": changed_fields_payload,
                        "data": data_payload,
                    },
                }
                logging.info(f"Emit {event_name}: " + str(payload))

                emit(event_name, payload)

        post_save.connect(handle_upsert, sender=model_class, weak=False)
