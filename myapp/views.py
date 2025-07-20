from django.shortcuts import render,redirect
from .models import*
from django.core.mail import send_mail
import random
import razorpay


def index(request):

    if "email" in request.session:
            uid=user.objects.get(email=request.session['email'])
            pid=Add_product.objects.all()
            mid=Category.objects.all()
            lid=Add_to_cart.objects.filter(user_id=uid).count()
            lid_w=Add_to_wishlist.objects.filter(user_id=uid).count()
            wid=Add_to_wishlist.objects.filter(user_id=uid)
            wis_id=[item.product_id.id for item in wid ]


            con={
                'uid':uid,
                'pid':pid,
                'mid':mid,
                'lid':lid,
                'lid_w':lid_w,
                "wis_id":wis_id
               
            }
            return render(request,"index.html",con)
    else:
            pid=Add_product.objects.all()
            cid=Category.objects.all()
            mid=Category.objects.all()

            con={
                'pid':pid,
                'cid':cid,
                'mid':mid
               
            }

            return render(request,"index.html",con)


def shop(request):
    
    try:
        uid=user.objects.get(email=request.session['email'])
        pid=Add_product.objects.all()
        cid =Category.objects.all()
        mid=Category.objects.all()   
        lid=Add_to_cart.objects.filter(user_id=uid).count()
        lid_w=Add_to_wishlist.objects.filter(user_id=uid).count()
        wid=Add_to_wishlist.objects.filter(user_id=uid)
        
        high_to_low=request.GET.get('high_to_low')
        low_to_high=request.GET.get('low_to_high')
        A_to_Z=request.GET.get('A_to_Z')
        Z_to_A=request.GET.get('Z_to_A')
        wis_id=[item.product_id.id for item in wid ]
        c_id=request.GET.get("c_id")


        if high_to_low:
            pid=Add_product.objects.order_by("-price")
        elif low_to_high:
            pid=Add_product.objects.order_by("price")
        elif A_to_Z:
            pid=Add_product.objects.order_by("name")
        elif Z_to_A:
            pid=Add_product.objects.order_by("-name")
        elif c_id:
            pid=Add_product.objects.filter(s_id=c_id)         
        else:
            pid=Add_product.objects.all()

        con={
            'pid':pid,
            'cid':cid,
            # 'size':size,
            'mid':mid,
            'lid':lid,
            'lid_w':lid_w,
            'wis_id':wis_id,
            'high_to_low':high_to_low,
            'low_to_high':low_to_high,
            'A_to_Z':A_to_Z,
            'Z_to_A':Z_to_A,
            
        }

        return render(request,"shop.html",con)
    except:
        pid=Add_product.objects.all()
        cid =Category.objects.all()
        mid=Category.objects.all()  
        

        con={
            'pid':pid,
            'cid':cid,
            'mid':mid
        } 
        return render(request,"shop.html",con)


def detail(request,id):

    uid = user.objects.get(email=request.session['email'])
    mid=Category.objects.all() 
    vid=Add_product.objects.get(id=id)
    lid=Add_to_cart.objects.filter(user_id=uid).count()
    lid_w=Add_to_wishlist.objects.filter(user_id=uid).count()


    con={
        'uid':uid,
        'mid':mid,
        'vid':vid,
        'lid':lid,
        'lid_w':lid_w
    }

    return render(request,"detail.html",con)

def contact(request):

    if request.POST:
            name=request.POST['name']
            email=request.POST['email']
            message=request.POST['message']
            lid=Add_to_cart.objects.filter(user_id=uid).count()
            lid_w=Add_to_wishlist.objects.filter(user_id=uid).count()


            uid=Contact.objects.create(name=name,
                                   email=email,
                                   message=message,
                                   )
            
            
         
            return render(request,"contact.html")

    else:   

            return render(request,"contact.html")

def checkout(request):
    uid=user.objects.get(email=request.session['email'])
    prod=Add_to_cart.objects.filter(user_id=uid)
    # lid=Add_to_cart.objects.all().count()
    pid=Add_product.objects.all()
    # lid_w=Add_to_wishlist.objects.all().count()
    

    l1=[]
    sub_total=0
    total=0


    for i in prod:

        a = i.offer * i.qty
        l1.append(a)
        sub_total = sum(l1)
        total = sub_total + 50
        print("____________________________",total,sub_total,l1)


    amount = total*100 
    client = razorpay.Client(auth=('rzp_test_bilBagOBVTi4lE','77yKq3N9Wul97JVQcjtIVB5z'))
    response = client.order.create({
                        'amount':amount,
                        'currency':'INR',
                        'payment_capture':1
    })

    for i in prod:
        oid=Order.objects.create(user_id=uid,
                                 product_id=i.product_id,
                                 name=i.name,
                                 price=i.price,
                                 size=i.size,
                                 pic=i.pic,
                                 qty=i.qty,
                                #  contact_no=i.contact_no
                                                 )


    con={

        'prod':prod,
        'sub_total':sub_total,
        'total':total,
        'response':response,
        # 'lid':lid,
        # 'lid_w':lid_w,
        'pid':pid

    }

    return render(request,"checkout.html",con)

def cart(request):

    if "email" in request.session:
        uid=user.objects.get(email=request.session['email'])
        pid=Add_to_cart.objects.filter(user_id=uid)
        lid=Add_to_cart.objects.filter(user_id=uid).count()
        lid_w=Add_to_wishlist.objects.filter(user_id=uid).count()

        
        
        con={
            'pid':pid,
            'lid':lid,
            'lid_w':lid_w
        }
        return render(request,"cart.html",con)
    else:

        return render(request,"login.html")
    

def address(request):
    
    try:

        uid=user.objects.get(email=request.session['email'])
        cid=Address.objects.filter(user_id=uid).exists()
        aid=Address.objects.get(user_id=uid)

        if cid:
            l1=[]

            c_id=Add_to_cart.objects.all()

            for i in c_id:
                l1.append(f"_New Product_:-    user_id :- {i.user_id}, name :- {i.name},  price :- {i.price},  qty :- {i.qty} ")

                aid.list=l1
                aid.save()

                return redirect('checkout')
        
    except:
        if request.POST:
            f_name=request.POST['f_name']
            l_name=request.POST['l_name']
            email=request.POST['email']
            contact_no=request.POST['contact_no']
            address_1=request.POST['address_1']
            address_2=request.POST['address_2']
            country=request.POST['country']
            city=request.POST['city']
            state=request.POST['state']
            zip_code=request.POST['zip_code']

            uid=Address.objects.create(user_id=uid,
                                    f_name=f_name,
                                    l_name=l_name,
                                    email=email,
                                    contact_no=contact_no,
                                    address_1=address_1,
                                    address_2=address_2,
                                    country=country,
                                    city=city,
                                    state=state,
                                    zip_code=zip_code,
                                    )
            
            l1=[]

            cid=Add_to_cart.objects.all()

            for i in cid:
                l1.append(f"_New Product_:-    user_id :- {i.user_id}, name :- {i.name},  price :- {i.price},  qty :- {i.qty} ")


            uid.list=l1
            uid.save()


            return redirect("checkout")
        else:

            return render(request,"address.html")    

def delete_Address(request):
    uid=user.objects.get(email=request.session['email'])
    did=Address.objects.filter(user_id=uid).delete()


    return redirect('address')

def plus(request,id):
    
    pid=Add_to_cart.objects.get(id=id)
    
    
    if pid:
        
        pid.qty =pid.qty + 1
        pid.total_price=pid.offer * pid.qty
        pid.save()
        
        
        return redirect('cart')
    
    else:
        
        return redirect('cart')

def minus(request,id):
    
    pid=Add_to_cart.objects.get(id=id)
    
    if pid:
        
        if pid.qty == 1:
            pid.delete()
            return redirect('cart')
        
        pid.qty =pid.qty  - 1 
        pid.total_price=pid.offer * pid.qty
        
        pid.save()
        
        return redirect('cart')
    
    else:
        
        return redirect('cart')
    
def deletes(request,id):
    
    pid=Add_to_cart.objects.get(id=id)
    
    pid.delete()
    
    return redirect('cart')

  
def login(request):
    
    if "email" in request.session:
        uid = user.objects.get(email=request.session['email'])
        pid=Add_product.objects.all()
        mid=Category.objects.all()
        
        con={
            'pid':pid,
            'mid':mid
        }
        
        return render(request,"index.html",con)
    else:
        try:
            if request.POST:
                email = request.POST['email']
                password = request.POST['password']
               
                uid = user.objects.get(email = email)
               
                request.session['email']=uid.email
                
                if uid.email==email:
                 if uid.password == password:
                    pid = Add_product.objects.all() 
                    mid=Category.objects.all()
            
                    con = {
                            
                            'pid' : pid,
                            'mid':mid
                    }                
                    return render(request,"index.html",con)
                 else:
                    con = {
                        'pid' : "invalid password..."
                    }
                    return render(request,"login.html",con)
                else:
                    con={
                        'eid':"invalid email.........."
                    }
                    return render(request,"login.html",con)
            else:
                return render(request,"login.html")
        except:
            con = {
                        'eid' : "invalid email..."
                    }
            return render(request,"login.html",con)

def register(request):

    if request.POST:

        u_name = request.POST['u_name']
        l_name=request.POST['l_name']
        email=request.POST['email']
        password=request.POST['password']
        c_password=request.POST['c_password']
        contact=request.POST['contact']


        uid=user.objects.create(u_name=u_name,
                                l_name=l_name,
                                email = email,
                                password=password,
                                c_password = c_password,
                                contact=contact,
                                )
        
        return render(request,"login.html")
    else:
        return render(request,"register.html")
    

def confirm_password(request):
    
    if request.POST:
        email=request.POST['email']
        otp=request.POST['otp']
        password=request.POST['password']
        c_password=request.POST['c_password']
        
        uid=user.objects.get(email=email)
        
        if str(uid.otp) == otp:
            
            if password == c_password:
                uid.password = password
                uid.save()
                
                
                con={
                    
                    'email' : email,
                    'uid' : uid
                }
                return render(request,"login.html",con)
            else:
                con={
                    
                    'eid':"invalid password.......",
                    'email': email,
                    'uid': uid
                }
                return render(request,"confirm_password.html",con)
        else:
            con={
                
                'email':email,
                'oid':"invalid otp..",
                'uid':uid
            }
            return render(request,"confirm_password.html",con)
    return render(request,"confirm_password.html")


def forget_password(request):

    if request.POST:
        email = request.POST['email']
        
        otp = random.randint(1111,9999)
        
        try:
            uid = user.objects.get(email=email)
            uid.otp = otp
            uid.save()
            
            send_mail("forget_password","your otp is ..."+str(otp),"gohiljayb10@gmail.com",[email])
            
            con = {
                'email' : email
            }
            return render(request,"confirm_password.html",con)
        except:
            con={
                'eid':"invalide email..."
            }
            return render(request,"forget_password.html",con)
        
    return render(request,"forget_password.html")

def add_to_cart(request,id):
    
    if "email" in request.session:
        uid=user.objects.get(email=request.session['email'])
        pid=Add_product.objects.get(id=id)
        aid=Add_to_cart.objects.filter(product_id=pid,user_id=uid).exists()
       
        if aid:
            
            aid=Add_to_cart.objects.get(product_id=pid)
            
            aid.qty=aid.qty + 1
            aid.total_price=aid.offer * aid.qty
            aid.save()
            
            return redirect('cart')
            
        else:
            
            Add_to_cart.objects.create(user_id=uid,
                                        product_id=pid,
                                        name=pid.name,
                                        price=pid.price,
                                        pic=pid.pic,
                                        offer=pid.offer,
                                        total_price=pid.qty * pid.offer,
                                        size=pid.size
                                        )
            return redirect('cart')
    else:
        return render(request,"login.html")
  

def logout(request):

    if "email" in request.session:

        del request.session['email']

        return render(request,"login.html")
    else:
        return render(request,"login.html")
    
def search(request):

    name = request.GET['name']

    if name:

        pid = Add_product.objects.filter(name__contains=name)
        con = {
            'pid' : pid
        }

        return render(request,"shop.html",con)
    else:
        return redirect('index')

def category(request,id):
    uid=user.objects.get(email=request.session['email'])
    mid=Category.objects.all()
    pid=Add_product.objects.filter(m_id=id)
    cid=Category.objects.all()
    lid=Add_to_cart.objects.filter(user_id=uid).count()
    lid_w=Add_to_wishlist.objects.filter(user_id=uid).count()
    
    con={
        'mid':mid,
        'pid': pid,
        'cid':cid,
        'lid':lid,
        'lid_w':lid_w
    }
    return render(request,"shop.html",con)

def wishlist(request):
    if "email" in request.session:
        email=request.session['email']
        uid=user.objects.get(email=email)
        wid=Add_to_wishlist.objects.all()
        lid_w=Add_to_wishlist.objects.filter(user_id=uid).count()
        lid=Add_to_cart.objects.filter(user_id=uid).count()
        wid=Add_to_wishlist.objects.filter(user_id=uid)
        wis_id=[item.product_id.id for item in wid ]


        con={
            'uid':uid,
            'wid':wid,
            'lid_w':lid_w,
            'lid':lid,
            'wis_id':wis_id
        }     

        return render(request,"wishlist.html",con)
    else:
        return redirect ('login')
    
def delete_w(request,id):
    try:
       pid=Add_product.objects.get(id=id) 
       wid=Add_to_wishlist.objects.get(product_id=id)
       wid.delete()
    except:
        wid=Add_to_wishlist.objects.get(id=id)
        wid.delete()
    return redirect(request.META['HTTP_REFERER'])

def add_to_wishlist(request,id):

    if "email" in request.session:
        
        uid = user.objects.get(email=request.session['email'])
        pid = Add_product.objects.get(id=id)
        

        wid = Add_to_wishlist.objects.create(
                                    user_id=uid,
                                    product_id=pid,
                                    name=pid.name,
                                    price=pid.price,
                                    pic=pid.pic,
                                    offer=pid.offer,
                                    )
        
        return redirect('wishlist')
    else:
        return render(request,"login.html")


def order(request):


    uid=user.objects.get(email=request.session['email'])
    
    oid=Order.objects.filter(user_id=uid)
    aid=Address.objects.filter(user_id=uid)
    did=Add_to_cart.objects.filter(user_id=uid).delete()
    con={
         
         'oid':oid,
         'aid':aid,
         'did':did
     }
    return render(request,"order.html",con)


def price_filter1(request):
    c1=request.GET.get("size-1")
    c2=request.GET.get("size-2")
    c3=request.GET.get("size-3")
    c4=request.GET.get("size-4")
    c5=request.GET.get("free size")
    mid=Category.objects.all()
    

    pid=[]
    if c1:
        print("XL")
        p=Add_product.objects.filter(size="XL")
        pid.extend(p)
    if c2:
        print("M")
        p=Add_product.objects.filter(size="M")
        pid.extend(p)
    if c3:
        print("L")
        p=Add_product.objects.filter(size="L")
        pid.extend(p) 
    if c4:
        print("S")  
        p=Add_product.objects.filter(size="S")
        pid.extend(p) 
    if c5:
        print("free size")  
        p=Add_product.objects.filter(size="free size")
        pid.extend(p) 
   
    if len(pid) == 0:
        print("ok")      
    contaxt={
        "pid":pid,
        "p_count":len(pid),
        "mid":mid,
        
    }
    return render(request, 'shop.html',contaxt)

