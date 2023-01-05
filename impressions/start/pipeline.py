from .models import Profile


def get_avatar(backend, strategy, details, response,
               user=None, *args, **kwargs):
    url = None
    if backend.name == 'vk-oauth2':
        url = response.get('photo', '')
    if url:
        try:
            profile = Profile.objects.get(user=user)
            profile.avatar = url
        except:
            profile = Profile.objects.create(user=user, avatar=url)
        profile.save()
