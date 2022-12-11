from django.http import HttpResponse

from Model.models import Test

def testdb(request):
    # case1: insert
    # test1 = Test(name='wuxinbei')
    # test1.save()
    # return HttpResponse("<p>insert succ!</p>")

    # case2: get
    response = ""
    response1 = ""
    list = Test.objects.all()
    response2 = Test.objects.filter(id=1)
    response3 = Test.objects.get(name='wuxinbei')

    for item in list:
        response1 += item.name + ' '
    response = response1
    return HttpResponse("<p>" + response + "</p>")

