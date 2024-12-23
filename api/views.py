from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from .serializers import ProjectSerializers
from projects.models import Project,Review,Tag

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},

        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'},

    ]

    return Response(routes)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def  getProjects(request):
    print('USER:',request.user)

    projects = Project.objects.all()
    serializer = ProjectSerializers(projects,many = True)


    return Response(serializer.data)


@api_view(['GET'])
def  getProject(request,pk):

    projects = Project.objects.get(id=pk)
    serializer = ProjectSerializers(projects,many = False)


    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request,pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data # this is only possible because of django rest framework and we can access the body of the data

    review,created = Review.objects.get_or_create(  # get or create will first check whether that review is there in the db or not 
        owner = user,
        project=project,
   )
    
    review.value = data['value']
    review.save()
    project.getVoteCount  # because of @propert decortor it does not need to triggered as a regular fucntion

    serializer = ProjectSerializers(project,many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def removeTag(request):
    tagId = request.data['tag']
    projectId = request.data['project']
    project = Project.objects.get(id=projectId)
    tag = Tag.objects.get(id = tagId)

    project.tags.remove(tag)

    return Response('Tag was deleted!')

