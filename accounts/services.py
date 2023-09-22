from django.core.exceptions import ValidationError


def get_path_upload_avatar(instance, image):
    return f'avatar/{instance.username}/{image}'


def validate_size_image(image_obj):
    megabyte_limit = 3
    if image_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError("Maximum file size {megabyte_limit}MB")