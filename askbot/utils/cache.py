"""Utilities for working with Django Models."""
import itertools

from django.contrib.contenttypes.models import ContentType

from askbot.utils.lists import flatten

from django.utils.decorators import decorator_from_middleware_with_args
from django.middleware.cache import CacheMiddleware
from django.conf import settings as django_settings

def flexi_cache_page(*args, **kwargs):
    """
    *** BASED ON @cache_page ***
    ===========================================================
    Decorator for views that tries getting the page from the cache and
    populates the cache if the page isn't in the cache yet.

    The cache is keyed by the URL and some data from the headers.
    Additionally there is the key prefix that is used to distinguish different
    cache areas in a multi-site setup. You could use the
    sites.get_current().domain, for example, as that is unique across a Django
    project.

    Additionally, all headers from the response's Vary header will be taken
    into account on caching -- just like the middleware does.
    """

    # Do nothing if FLEXI_CACHE is swiched off
    if not django_settings.FLEXI_CACHE:
        return lambda x: x
    else:
        # We also add some asserts to give better error messages in case people are
        # using other ways to call cache_page that no longer work.
        cache_alias = kwargs.pop('cache', None)
        key_prefix = kwargs.pop('key_prefix', None)
        assert not kwargs, "The only keyword arguments are cache and key_prefix"
        def warn():
            import warnings
            warnings.warn('The cache_page decorator must be called like: '
                      'cache_page(timeout, [cache=cache name], [key_prefix=key prefix]). '
                      'All other ways are deprecated.',
                      PendingDeprecationWarning,
                      stacklevel=3)

        if len(args) > 1:
            assert len(args) == 2, "cache_page accepts at most 2 arguments"
            warn()
            if callable(args[0]):
                return decorator_from_middleware_with_args(CacheMiddleware)(cache_timeout=args[1], cache_alias=cache_alias, key_prefix=key_prefix)(args[0])
            elif callable(args[1]):
                return decorator_from_middleware_with_args(CacheMiddleware)(cache_timeout=args[0], cache_alias=cache_alias, key_prefix=key_prefix)(args[1])
            else:
                assert False, "cache_page must be passed a view function if called with two arguments"
        elif len(args) == 1:
            if callable(args[0]):
                warn()
                return decorator_from_middleware_with_args(CacheMiddleware)(cache_alias=cache_alias, key_prefix=key_prefix)(args[0])
            else:
                # The One True Way
                return decorator_from_middleware_with_args(CacheMiddleware)(cache_timeout=args[0], cache_alias=cache_alias, key_prefix=key_prefix)
        else:
            warn()
            return decorator_from_middleware_with_args(CacheMiddleware)(cache_alias=cache_alias, key_prefix=key_prefix)

def fetch_model_dict(model, ids, fields=None):
    """
    Fetches a dict of model details for model instances with the given
    ids, keyed by their id.

    If a fields list is given, a dict of details will be retrieved for
    each model, otherwise complete model instances will be retrieved.

    Any fields list given shouldn't contain the primary key attribute for
    the model, as this can be determined from its Options.
    """
    if fields is None:
        return model._default_manager.in_bulk(ids)
    else:
        id_attr = model._meta.pk.attname
        return dict((obj[id_attr], obj) for obj
            in model._default_manager.filter(id__in=ids).values(
                *itertools.chain((id_attr,), fields)))

def populate_foreign_key_caches(model, objects_to_populate, fields=None):
    """
    Populates caches for the given related Model in instances of objects
    which have a ForeignKey relationship to it, specified as a list of
    (object list, related attribute name list) two-tuples.

    If a list of field names is given, only the given fields will be
    looked up and related object caches will be populated with a dict of
    the specified fields. Otherwise, complete model instances will be
    retrieved.
    """
    # Get all related object ids for the appropriate fields
    related_object_ids = []
    for objects, attrs in objects_to_populate:
        related_object_ids.append(tuple(tuple(getattr(obj, '%s_id' % attr)
                                              for attr in attrs)
                                  for obj in objects))
    unique_ids = tuple(set(pk for pk in flatten(related_object_ids) if pk))
    related_objects = fetch_model_dict(model, unique_ids, fields)

    # Fill related object caches
    for (objects, attrs), related_ids in itertools.izip(objects_to_populate,
                                                        related_object_ids):
        for obj, related_ids_for_obj in itertools.izip(objects,
                                                       related_ids):
            for attr, related_object in itertools.izip(attrs, (related_objects.get(pk, None)
                                                               for pk in related_ids_for_obj)):
                setattr(obj, '_%s_cache' % attr, related_object)

def populate_content_object_caches(generic_related_objects, model_fields=None):
    """
    Retrieves ``ContentType`` and content objects for the given list of
    items which use a generic relation, grouping the retrieval of content
    objects by model to reduce the number of queries executed.

    This results in ``number_of_content_types + 1`` queries rather than
    the ``number_of_generic_reL_objects * 2`` queries you'd get by
    iterating over the list and accessing each item's object attribute.

    If a dict mapping model classes to field names is given, only the
    given fields will be looked up for each model specified and the
    object cache will be populated with a dict of the specified fields.
    Otherwise, complete model instances will be retrieved.
    """
    if model_fields is None:
        model_fields = {}

    # Group content object ids by their content type ids
    ids_by_content_type = {}
    for obj in generic_related_objects:
        ids_by_content_type.setdefault(obj.content_type_id,
                                       []).append(obj.object_id)

    # Retrieve content types and content objects in bulk
    content_types = ContentType.objects.in_bulk(ids_by_content_type.keys())
    for content_type_id, ids in ids_by_content_type.iteritems():
        model = content_types[content_type_id].model_class()
        objects[content_type_id] = fetch_model_dict(
            model, tuple(set(ids)), model_fields.get(model, None))

    # Set content types and content objects in the appropriate cache
    # attributes, so accessing the 'content_type' and 'object' attributes
    # on each object won't result in further database hits.
    for obj in generic_related_objects:
        obj._object_cache = objects[obj.content_type_id][obj.object_id]
        obj._content_type_cache = content_types[obj.content_type_id]
