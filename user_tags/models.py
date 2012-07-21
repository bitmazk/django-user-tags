"""Models for the ``user_tags`` app."""
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TaggedItem(models.Model):
    """
    This actually maps tags to real items.

    For example there might be a "WeatherEntry" object in the database, which
    has a tag group called "description" and tags called "sunny" and "rainy".

    The ``TaggedItem`` is the missing piece to link the user tag "sunny" to the
    "WeatherEntry" object in the database.

    :content_object: Can be any Django model object that should be tagged.
    :user_tag: One or many ``UserTag`` instances.

    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    user_tags = models.ManyToManyField(
        'user_tags.UserTag',
        verbose_name=_('User tag'),
    )


class UserTag(models.Model):
    """
    Belongs to a ``UserTagGroup`` and resembles a tag in that group.

    Each user tag inside a tag group must be unique in that group. This allows
    a user to rename a tag (i.e. to correct a typo) and have all of these tags
    updated immediately.

    :user_tag_group: A ``UserTagGroup`` instance.
    :text: The text of this tag, i.e. "sunny"

    """
    class Meta:
        unique_together = ('user_tag_group', 'text')

    user_tag_group = models.ForeignKey(
        'user_tags.UserTagGroup',
        verbose_name=_('User tag group'),
    )

    text = models.CharField(
        max_length=256,
        verbose_name=_('Text'),
    )


class UserTagGroup(models.Model):
    """
    Belongs to a ``User`` and resembles a group of tags.

    For example "weather" might be a group of tags with lot's of ``UserTag``
    objects like "sunny", "rainy" etc..

    :user: A ``User`` instance.
    :name: The name of this tag group.

    """
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
    )

    name = models.CharField(
        max_length=256,
        verbose_name=_('Name'),
    )
