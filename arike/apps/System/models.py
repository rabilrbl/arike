from uuid import uuid4

from django.db import models

# CHOICES
# Reference https://github.com/coronasafe/care/blob/master/care/users/models.py#L61
LOCAL_BODY_CHOICES = (
    (1, "Grama Panchayath"),
    (2, "Block Panchayath"),
    (3, "District Panchayath"),
    (4, "Nagar Panchayath"),
    (5, "Municipality"),
    (6, "Corporation"),
    (7, "Others"),
)


class BaseManager(models.Manager):
    """
    Base manager for models.
    """

    def get_queryset(self):
        return super(BaseManager, self).get_queryset().filter(deleted=False)

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


# Add Common fields to share accross all models
class BaseModel(models.Model):
    """
    Base model for all models.
    """
    # Common fields
    external_id = models.UUIDField(default=uuid4, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

    objects = BaseManager()

    def hard_delete(self, *args, **kwargs):
        super(BaseModel, self).delete(*args, **kwargs)

    def get_last_updated_date(self):
        return self.updated_at.strftime("%d-%m-%Y %H:%M:%S")

    def get_created_date(self):
        return self.created_at.strftime("%d-%m-%Y %H:%M:%S")

    class Meta:
        abstract = True

# Models


class State(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class District(BaseModel):
    state = models.ForeignKey(State, on_delete=models.PROTECT)

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class LocalBody(BaseModel):
    district = models.ForeignKey(District, on_delete=models.PROTECT)

    name = models.CharField(max_length=255)
    kind = models.IntegerField(choices=LOCAL_BODY_CHOICES, default=7)
    local_body_code = models.CharField(max_length=20, blank=True, null=True)

    def get_kind(self):
        return LOCAL_BODY_CHOICES[self.kind][1]

    def __str__(self):
        return f"{self.name} ({self.kind})"


class Ward(BaseModel):
    local_body = models.ForeignKey(LocalBody, on_delete=models.PROTECT)

    name = models.CharField(max_length=255)
    number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.number})"
