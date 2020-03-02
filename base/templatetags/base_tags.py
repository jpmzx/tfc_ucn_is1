import datetime
import json
import random
import base64
from django import template
from django.conf import settings
from django.core.cache import cache
from django.urls import reverse
from django.utils.safestring import mark_safe
from decimal import Decimal
from django.utils.encoding import force_text
from hashlib import md5

register = template.Library()

@register.simple_tag()
def get_name_from_path(path):
    return path.split('/')[-1]

@register.simple_tag()
def project_url(path):
    '''Returns url from url's where namespace is the project name'''
    project_name = getattr(settings, 'PROJECT_NAME_CODE', None)

    if project_name:
        return reverse('{}:{}'.format(project_name, path))
    else:
        return reverse(path)


@register.simple_tag()
def git_version():
    '''Returns git version from base project'''
    exec_env = getattr(settings, 'EXEC_ENV', None)
    git_version = getattr(settings, 'GIT_VERSION', None)
    if git_version:
        if exec_env != 'PRODUCTION':
            return git_version + ' ({})'.format(exec_env)
        else:
            return git_version
    else:
        return ""


@register.simple_tag
def get_attribute(model, attribute):
    '''Returns verbose_name for a model.'''
    return getattr(model, attribute)

@register.simple_tag
def JSON_get_attribute(obj, attribute, int_key = False):
    '''Returns value for a key from a JSON or python dictionary.'''
    try:
        return obj[int(attribute) if int_key else attribute]
    except KeyError:
        return None
    except ValueError:
        return None
    except TypeError:
        return None

@register.simple_tag
def model_get_help_text(instance, field_name):
    return model_get_field(instance.__class__, field_name).help_text

@register.simple_tag
def model_get_field_verbose_name(instance, field_name):
    return model_get_field(instance.__class__, field_name).verbose_name

@register.simple_tag
def get_field(form, field):
    '''Returns a list with the fields name of a django form.'''
    # Note: Only work to django model forms and django model forms with exclude fields.
    # Code functionality to other attributes of the django forms
    #return list(set([obj.name for obj in form._meta.model._meta.get_fields()]) - set(form._meta.exclude))
    return form[field]

@register.simple_tag
def get_model_verbose_name(instance):
    '''Returns verbose_name for a model.'''
    return instance._meta.verbose_name

@register.simple_tag()
def logout_url():
    return getattr(settings, 'LOGOUT_URL', '/logout/')



@register.simple_tag(takes_context=True)
def avatar_url(context, size=None, email="-1", user=None, identification="-1"):
    # TODO: Make behaviour configurable
    type_ = 'user'
    hash_ = None
    if not user:
        user = context['request'].user.username
    to_encode = user
    if identification != "-1":
        type_ = 'id'
        to_encode = str(identification)
    if email != "-1":
        type_ = 'email'
        to_encode = email.lower()
        
    try:
        hash_ = str(base64.urlsafe_b64encode(to_encode.encode("utf-8")),"utf-8")
    except:
        url = get_app_url("url_ecore")
        if settings.DEBUG == True:
            base_root = url + settings.BASE_DIR + '/person_ext/static/'
        else:
            base_root = url + settings.STATIC_ROOT
        return base_root + "person_ext/images/avatar-clear.png?m={}".format(month=datetime.date.today().month)        
        
    url = '{url}/person/avatar/?hash={hash}&d={month}&type={type}{size}'.format(
        url=get_app_url("url_ecore"),
        hash=hash_,
        type=type_,
        size="&size=true" if size else '',
        month=datetime.date.today().month
    )
    return url
    

@register.simple_tag(takes_context=True)
def avatar_register(context):
    # TODO: Make behaviour configurable
    user = context['request'].user
    return 'https://www.gravatar.com/{hash}'.format(
        hash=md5(user.username.encode('utf-8')).hexdigest()
    )

@register.simple_tag(takes_context=True)
def add_active(context, url_name, *args, **kwargs):
    '''Sidebar menu tag (returns active class)'''
    exact_match = kwargs.pop('exact_match', False)

    path = reverse(url_name, args=args, kwargs=kwargs)
    if not exact_match and context.request.path.startswith(path):
        return ' active '
    elif exact_match and context.request.path == path:
        return ' active '
    else:
        return ''

@register.simple_tag
def random_int(a, b=None):
    if b is None:
        a, b = 0, a
    return random.randint(a, b)

@register.filter(name='field_type')
def field_type(field):
    '''Get the type of field in django template'''
    return field.__class__.__name__

@register.filter(is_safe=True)
def valdateformat(value):
    """
    Converts an integer to a string containing dots every three digits.
    For example, 3000 becomes '3.000' and 45000 becomes '45.000'.
    """
    if isinstance(value, datetime.date):
        return value.strftime('%d/%m/%Y')
    if isinstance(value, bool):
        if value == False:
            return 'No'
        elif value == True:
            return 'Si'
    return value



@register.simple_tag
def get_url_or_none(django_url_name):
    try:
        return reverse(django_url_name)
    except:
        return None

@register.filter
def index(List, i):
    """
        get item by index
    """
    try:
        return List[i]
    except:
        try:
            return List[str(i)]
        except:
            return ""



@register.filter
def code_clean(value):
    return value.replace("REQ# ","")


@register.filter
def str_to_datetime(value, format = '%Y/%m/%d'):
    if value:
        return datetime.datetime.strptime(value, format)
    else:
        return ""

@register.filter
def is_past_due(value):
    """
    Para saber si una fecha es menor a hoy (si está vencida)
    """
    today = datetime.date.today()
    return value < today



class SumNode(template.Node):
    def __init__(self, sequence, loopvar, loopitem):
        self.sequence = template.Variable(sequence)
        self.loopvar = loopvar
        self.loopitem = template.Variable(loopitem)

    def render(self, context):
        sequence = self.sequence.resolve(context)
        if sequence:
            return sum(self.loopitem.resolve({self.loopvar: x}) for x in sequence)
        else:
            return 0


@register.tag('sum')
def do_sum(parser, token):
    """{% sum <foo.bar> for <foo> in <sequence> %}"""
    bits = token.split_contents()[1:]
    try:
        loopitem, _for, loopvar, _in, sequence = bits
    except ValueError:
        raise template.TemplateSyntaxError("Invalid tag syntax expected"
                                           " '{% sum <foo.bar> for <foo> in <sequence> %}'")

    return SumNode(sequence, loopvar, loopitem)

@register.filter
def validate_messageis_table(value):
    if value.find('table') != -1:
        return True
    return False

@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(dict(zip([value for value in obj._fields],obj))))


@register.simple_tag
def update_variable(value):
    """Allows to update existing variable in template"""
    return value