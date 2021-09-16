# Activity Tracker

Activity Tracker is used for tracking field changes and sending activity events via `events_library` to the `activities` service.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install git+git://github.com/dzemsxyz/activity_tracker.git@master#egg=activity_tracker
```

## Usage

```python
# apps.py
def ready(self) -> None:

    from activity_tracker.utils import declare_activity_event
    from orders.models import Order

    # event name, model class, fields to track, additional fields
    declare_activity_event("order-status", Order, ("status",), ("name",))
```

## Requirements
Model must have: 
- [Field Tracker](https://django-model-utils.readthedocs.io/en/latest/utilities.html#field-tracker) field named `tracker`.
- Method for retrieving the owner profile_id called `get_owner_profile_id()`

Example:
```python
# models.py
from model_utils import FieldTracker

class Order(PolymorphicModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    """
    Other fields...
    """
    tracker = FieldTracker()
    
    def get_owner_profile_id(self) -> uuid.UUID:
        return profile.id
```


## License
[MIT](https://choosealicense.com/licenses/mit/)