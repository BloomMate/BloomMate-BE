from .models import Community
from .serializer import QuestionSerializer, CommentSerializer
from .pagination import CustomResultsSetPagination

from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from rest_framework.views import APIView

from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication


# Community에 올라온 질문 목록 보여주기
class QuestionList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = CustomResultsSetPagination
    
    # 질의응답 리스트 보여줄 때
    def get(self, request):
        questions = Community.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        dataList=serializer.data

        for element in dataList:
            del element['comments'] # comments 부분은 안 보여주기
        return Response(dataList,status=status.HTTP_200_OK)
    

# 새로운 질문 등록
class QuestionCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request):
        # request.data 는 사용자의 입력 데이터
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True): # 유효성 검사
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# 새로운 댓글 등록 - 백엔드에서 직접 넣어줄 예정
class CommentCreate(APIView):
    permission_classes = [permissions.AllowAny] # 토큰 없이 누구나 댓글 등록 가능
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, pk, format=None):
        question = Community.objects.get(pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(question=question)
            question.answer_or_not = True # 댓글 유무 업데이트
            question.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# 질문 세부사항 관련
class QuestionDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    
    # 객체 가져오기
    def get_object(self, pk):
        try:
            return Community.objects.get(pk=pk)
        except Community.DoesNotExist:
            raise Http404
        
    # 질문 상세히 보기
    def get(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    
    # 질문 수정하기
    def patch(self, request, pk, format=None):
        question = self.get_object(pk)
        
        # 질문자와 수정자가 동일한지 확인
        if not request.user == question.user:
            return Response({
                "detail": "직접 작성한 질문이 아닙니다. 질문 수정이 허가되지 않았습니다."
            },
            status=status.HTTP_403_FORBIDDEN                    
        )
        
        serializer = QuestionSerializer(instance=question, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 질문 삭제하기
    def delete(self, request, pk, format=None):
        question = self.get_object(pk)
        
        # 질문자와 수정자가 동일한지 확인
        if not request.user == question.user:
            return Response({
                "detail": "직접 작성한 질문이 아닙니다. 질문 삭제가 허가되지 않았습니다."
            },
            status=status.HTTP_403_FORBIDDEN
        )
            
        question.delete()
        return Response({
                "message": "질문이 삭제되었습니다."
            },
            status=status.HTTP_204_NO_CONTENT
        )