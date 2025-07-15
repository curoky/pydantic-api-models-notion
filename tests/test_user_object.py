import uuid
from pydantic_api.notion.models.objects.properties.page_property import CreatedByProperty
from pydantic_api.notion.models.objects.user import UserObject, DeletedUserObject


def test_userobject_accepts_deleteduser():
    user_id = uuid.uuid4()
    data = {
        "type": "created_by",
        "created_by": {
            "object": "user",
            "id": user_id,
        }
    }
    created_by = CreatedByProperty.model_validate(data)
    assert isinstance(created_by.created_by, DeletedUserObject)
    assert created_by.created_by.object == "user"
    assert created_by.created_by.id == user_id
