from pydantic import BaseModel

class MyBase(BaseModel):
    a: int = 1
    b: int = a + 1
    
    @classmethod
    def from_base(cls):
        return cls()

class MyClass1(MyBase):
    def foo(self):
        self.b = 10

class MyClass2(MyBase):
    pass

c1 = MyClass1.from_base()
print(c1)

c2 = MyClass2.from_base()
print(c2)

c1.foo()

print(c1)
print(c2)