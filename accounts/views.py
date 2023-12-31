# 데이터 처리
from .serializer import *

# APIView 사용 관련
from rest_framework.views import APIView

# Response 관련
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# 인증 관련
import jwt
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from BloomMate_backend.settings import SECRET_KEY
from rest_framework_simplejwt.tokens import AccessToken


# 회원가입 view
@permission_classes([AllowAny])
class SignupAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
            res = Response(
                {
                    "user": serializer.data,
                    "message": "Register success",
                },
                status=status.HTTP_200_OK
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
     
# 로그인 view   
@permission_classes([AllowAny])
class LoginAPIView(APIView):
    def post(self, request):
        user = authenticate(
            account_id=request.data.get("account_id"),
            password=request.data.get("password"),
        )
        
        if user is not None:
            serializer = UserSerializer(user)
            # 토큰 발급
            token = TokenObtainPairSerializer.get_token(user)
            access_token = str(token.access_token)
            res = Response(
                {
                    "account_id": serializer.data['account_id'],
                    "user_name": serializer.data['user_name'],
                    "tiiun_number": serializer.data['tiiun_number'],
                    "garden_size": serializer.data['garden_size'],
                    "address": serializer.data['address'],
                    "token": {
                        "access": access_token
                    },
                },
                status=status.HTTP_200_OK
            )
            
            # 토큰 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            return res
        else:
            return Response(
                {
                    "message": "User with given account id and password does not exists"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    

# 회원 정보 확인 및 수정하기, 로그아웃 view
class UserInfoAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 회원 정보 가져오기
    def get(self, request):
        user = request.user # 현재 인증된 사용자 가져오기
        serializer = UserSerializer(user)
        return Response(
            {
                "account_id": serializer.data['account_id'],
                "user_name": serializer.data['user_name'],
                "tiiun_number": serializer.data['tiiun_number'],
                "garden_size": serializer.data['garden_size'],
                "address": serializer.data['address'],
            },                
            status=status.HTTP_200_OK
        )
    
    # 회원 정보 수정하기
    def patch(self, request):
        user = request.user # 현재 인증된 사용자 가져오기
        data = request.data # 수정할 정보가 들어있는 요청 데이터 가져오기
        
        # 수정하고자 하는 정보가 빈칸인지 확인하는 함수
        def is_blank(data):
            return data.strip() == ''
        
        # 확인하려는 데이터 필드 리스트를 만듭니다.
        fields_to_check = [data['user_name'], data['tiiun_number'], data['garden_size'], data['address']]

        # account_id를 변경하려고 할 때 에러 응답 반환
        # 나머지 정보는 변경이 가능하기 때문에 총 8개의 정보 중 7개까지만 변경이 가능하다.
        if 'account_id' in data or len(data) > 7:
            return Response(
                {
                    "message": "해당 정보는 변경할 수 없습니다."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # 아이디를 제외한 각 정보를 빈칸으로 설정할 때 에러 응답 반환
        # 이 경우, 정보를 수정할 때, 수정하고자 하는 부분은 새로 작성 및 수정하지 않을 부분은 기존 정보를 그대로 전송하는 방법으로 해야함
        # 아래의 예시는 user_name만 변경하려 할 때, 실제로 backend에 보내는 코드는 user_name뿐만 아니라 나머지 부분은 기존의 정보를 그대로 작성한 것
        # {
        #     "user_name": "snow",
        #     "tiiun_number": "test_tiiun_number",
        #     "garden_size": "0",
        #     "address": "test_address"
        # }
        elif any(is_blank(field) for field in fields_to_check):
            return Response(
                {
                    "message": "빈칸으로 설정할 수 없습니다."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            # 유효성 검사를 통해 user_name 필드만 변경 가능하도록 함
            serializer = UserSerializer(user, data=data, partial=True)
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {
                        "account_id": serializer.data['account_id'],
                        "user_name": serializer.data['user_name'],
                        "tiiun_number": serializer.data['tiiun_number'],
                        "garden_size": serializer.data['garden_size'],
                        "address": serializer.data['address'],
                        "date_joined": serializer.data['date_joined'],
                        "date_updated": serializer.data['date_updated'],
                    },                
                    status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=400)
            
    # 로그아웃
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response(
            {
                "message": "Logout success"
            },
            status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access")
        return response
    
    
# 토큰 확인
class JWTtokenVerifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        token = request.COOKIES.get("access")

        if not token :
            return Response(
                {
                    "message": "토큰이 쿠키에 존재하지 않습니다."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try :
            # 토큰 디코드 검증
            decoded_token = AccessToken(token)
            return Response(
                {
                    "message": "토큰이 유효합니다.",
                    "token_data": decoded_token.payload
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            # 토큰 검증 에러 처리
            return Response(
                {
                    "message": "토큰이 유효하지 않습니다.",
                    "error": str(0)
                },
                status=status.HTTP_401_UNAUTHORIZED
            )