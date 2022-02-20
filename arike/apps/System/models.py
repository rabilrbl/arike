from django.db import models
from uuid import uuid4

# CHOICES
# Reference https://github.com/coronasafe/care/blob/master/care/users/models.py#L61
LOCAL_BODY_CHOICES = (
    # Panchayath levels
    (1, "Grama Panchayath"),
    (2, "Block Panchayath"),
    (3, "District Panchayath"),
    (4, "Nagar Panchayath"),
    # Municipality levels
    (10, "Municipality"),
    # Corporation levels
    (20, "Corporation"),
    # Unknown
    (50, "Others"),
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

    objects = BaseManager()

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

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
    district  = models.ForeignKey(District, on_delete=models.PROTECT)

    name = models.CharField(max_length=255)
    kind = models.IntegerField(choices=LOCAL_BODY_CHOICES)
    local_body_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.kind})"

class Ward(BaseModel):
    local_body = models.ForeignKey(LocalBody, on_delete=models.PROTECT)

    name = models.CharField(max_length=255)
    number = models.CharField()

    def __str__(self):
        return f"{self.name} ({self.number})"
