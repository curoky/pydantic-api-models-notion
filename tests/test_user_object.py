import uuid
from pydantic_api.notion.models.objects.properties.page_property import CreatedByProperty, PeopleProperty
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


def test_people_property_accepts_deleted_users():
    """Test that PeopleProperty can contain DeletedUserObject items when users are deleted."""
    deleted_user_id = uuid.uuid4()
    active_user_id = uuid.uuid4()
    
    data = {
        "type": "people",
        "people": [
            {
                "object": "user",
                "id": deleted_user_id,
            },
            {
                "object": "user", 
                "id": active_user_id,
                "type": "person",
                "person": {
                    "email": "active@example.com"
                },
                "name": "Active User",
                "avatar_url": None
            }
        ]
    }
    
    people_property = PeopleProperty.model_validate(data)
    assert len(people_property.people) == 2
    
    # First user should be parsed as DeletedUserObject (no type/person data)
    assert isinstance(people_property.people[0], DeletedUserObject)
    assert people_property.people[0].object == "user"
    assert people_property.people[0].id == deleted_user_id
    
    # Second user should be parsed as PersonUserObject (has type/person data)
    from pydantic_api.notion.models.objects.user import PersonUserObject
    assert isinstance(people_property.people[1], PersonUserObject)
    assert people_property.people[1].object == "user"
    assert people_property.people[1].id == active_user_id
    assert people_property.people[1].person.email == "active@example.com"
