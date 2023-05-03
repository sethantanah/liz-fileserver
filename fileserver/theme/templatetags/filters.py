from django import template

register = template.Library()


@register.filter(name='extensions')
def audio_extension(extension):
    audio_extensions = ['mp3', 'wav', 'aac', 'flac', 'wma', 'ogg', 'alac', 'aiff', 'dsd', 'dsf', 'dff']
    video_extensions = ['avi', 'mp4', 'wmv', 'mov', 'flv', 'mkv', 'webm']
    image_extensions = ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'webp', 'tiff']

    if extension in audio_extensions:
        return 'audio'
    elif extension in video_extensions:
        return 'video'
    elif extension in image_extensions:
        return 'image'
    else:
        return 'pdf'
