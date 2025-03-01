from rest_framework.authentication import TokenAuthentication as BaseTokenAuth
from rest_framework.authtoken.models import Token

class TokenAuthentication(BaseTokenAuth): #basically overwriting TokenAuthentication
    keyword = 'Bearer'  
    #Esta es la palabra que va antes del token.
    #por default es "Token" pero la cambio a "Bearer"
