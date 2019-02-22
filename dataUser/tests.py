from django.test import TestCase

# Create your tests here.
def a(param1):
    def b(param):
         return param1+param
    return b
p1=a(5)
p2=a(4)
print(p1(10))
print(p2(10))