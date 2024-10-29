from rest_framework_simplejwt.authentication import JWTAuthentication

class AccessJWTAuthentication(JWTAuthentication):
    def get_header(self, request):
        token = request.COOKIES.get('access')
        """本ver"""
        # request.META['HTTP_AUTHORIZATION'] = '{header_type}{access_token}'.format(
        #     header_type="Bearer",access_token=token)
        # return super().get_header(request)
        """chatGPTver"""
        if token is None:
            return None  # トークンが存在しない場合、Noneを返す
        
        # ヘッダー形式を設定
        return f"Bearer {token}".encode("utf-8")


class RefreshJWTAuthentication(JWTAuthentication):
    def get_header(self, request):
        refresh = request.COOKIES.get('refresh')
        request.META['HTTP_REFRESH_TOKEN'] = refresh
        return super().get_header(request)

        