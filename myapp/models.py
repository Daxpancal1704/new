from django.db import models

# Create your models here.

class user(models.Model):
    u_name=models.CharField(max_length=30)
    l_name=models.CharField(max_length=30)
    email=models.EmailField()
    password=models.CharField(max_length=30)
    c_password=models.CharField(max_length=30)
    contact=models.IntegerField()
    otp=models.IntegerField(default=1234)


    def __str__(self):
        return self.email
    

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
class sub_category(models.Model):
    m_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
ch=(("XL","XL"),("M","M"),("L","L"),("S","S"),("free size","free size"))
class Add_product(models.Model):
    user_id = models.ForeignKey(user,on_delete=models.CASCADE)
    m_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    s_id = models.ForeignKey(sub_category,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    qty = models.IntegerField(default=1)
    offer = models.IntegerField()
    descriptions = models.TextField(max_length=1000)
    pic = models.ImageField(upload_to="IMG")
    size=models.CharField(choices=ch,max_length=30,default="")
    
    def __str__(self):
        return self.name
  
class Add_to_cart(models.Model):
    
    user_id = models.ForeignKey(user,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Add_product,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    pic = models.ImageField(upload_to="IMG")
    total_price = models.IntegerField()
    qty = models.IntegerField(default=1) 
    offer = models.IntegerField()
    size=models.CharField(max_length=30,default="")


    def __str__(self):
        return self.name


class Address(models.Model):
    user_id=models.ForeignKey(user,on_delete=models.CASCADE)
    f_name=models.CharField(max_length=30)
    l_name=models.CharField(max_length=30)
    email=models.EmailField(max_length=30)
    contact_no=models.CharField(max_length=30)
    address_1=models.CharField(max_length=30)
    address_2=models.CharField(max_length=30)
    country=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    state=models.CharField(max_length=30)
    zip_code=models.CharField(max_length=30)
    list=models.TextField()



class Contact(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    message=models.CharField(max_length=300)


class Add_to_wishlist(models.Model):

    user_id = models.ForeignKey(user,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Add_product,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    pic = models.ImageField(upload_to="IMG")
    offer=models.IntegerField()

    
    def __str__(self):
        return self.name
    

class Order(models.Model):
        user_id = models.ForeignKey(user,on_delete=models.CASCADE)
        product_id = models.ForeignKey(Add_product,on_delete=models.CASCADE)
        name = models.CharField(max_length=30)
        qty = models.IntegerField(default=1) 
        price=models.IntegerField()
        pic = models.ImageField(upload_to="IMG")
        size=models.CharField(max_length=30,default="")











# class feedback(models.Model):
#     user_id = models.ForeignKey(user,on_delete=models.CASCADE)
#     product_id = models.ForeignKey(Add_product,on_delete=models.CASCADE)  
#     message=models.CharField(max_length=200)
        

        