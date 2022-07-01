from users.api.v1.serializers import ProfileSerializer
from users.models.user import User


def SocialAuthRes(self,request):
    self.request = request
    self.serializer = self.get_serializer(data=self.request.data,
                                          context={'request': request})
    self.serializer.is_valid(raise_exception=True)
    self.login()
    res = self.get_response().data
    username = res['user']['username']

    user = User.objects.get(username=username)
    user.name = user.first_name
    user.save()

    serializer_response = {
        'profile': ProfileSerializer(
            instance=user).data,
        'token': res['token']}
    return serializer_response