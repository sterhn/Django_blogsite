from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_image_file_extension(value):
    ext = value.name.split('.')[-1].lower()
    if ext not in ['jpg', 'jpeg', 'png', 'gif']:
        raise ValidationError(_('Unsupported file extension.'))

def validate_image_file_size(value):
    if value.size > 1048576:  # 1MB
        raise ValidationError(_('Image file too large.'))