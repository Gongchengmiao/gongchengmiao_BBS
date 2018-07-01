import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class BbsUsernameValidator(validators.RegexValidator):
    # regex = r'^[\w.@+-]+$'
    regex = r'^[a-zA-Z\_][\w.@+-]+$'  # 首字母必须是字母或者下划线
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and @/./+/-/_ characters.'
        'And the first letter is required to be letter or underline.'
    )
    flags = 0
