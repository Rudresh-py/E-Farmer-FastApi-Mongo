from pydantic import BaseModel, EmailStr
from fastapi import UploadFile
from typing import Optional
from datetime import datetime


class UserRegisterModel(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    username: Optional[str]
    password: str
    email: EmailStr = None
    address: Optional[str] = None
    pincode: Optional[str] = None
    farmerid: Optional[str] = None
    aggreid: Optional[str] = None
    photo: Optional[bytes] = None
    is_farmer: Optional[bool] = None
    is_aggregator: Optional[bool] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]



class UserLogin(BaseModel):
    email: EmailStr
    password: str

#     class Meta:
#         verbose_name_plural = "Customer_vendor_table"
#         verbose_name = "Customer_vendor_table"
# class fertilizersmodel(models.Model):
#     user = models.ForeignKey(registertable, on_delete=models.CASCADE, null=True, blank=True)
#     name = models.CharField(max_length=300, null=True, blank=True)
#     descr = models.TextField(null=True, blank=True)
#     image = models.FileField(upload_to="fertilizers", null=True, blank=True)
#     farmer = models.BooleanField(default=False)
#     aggregator = models.BooleanField(default=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name_plural = "Fertilizers"


class FertilizersModel(BaseModel):
    user: str
    name: str
    desc: str
    image: Optional[bytes] = None
    is_farmer: Optional[bool] = None
    is_aggregator: Optional[bool] = None
    price: Optional[float] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class ProductModel(BaseModel):
    name: str
    desc: str
    image: Optional[bytes] = None
    is_aggregator: Optional[bool] = None
    price: Optional[float] = None
    # category: str
    # user_id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

# class machinarymodel(models.Model):
#     user = models.ForeignKey(registertable, on_delete=models.CASCADE, null=True, blank=True)
#
#     name = models.CharField(max_length=300, null=True, blank=True)
#     descr = models.TextField(null=True, blank=True)
#     image = models.FileField(upload_to="machinary", null=True, blank=True)
#     farmer = models.BooleanField(default=False)
#     aggregator = models.BooleanField(default=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     leaseprice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name_plural = "Machinaries"
#
#
# class pesticidesmodel(models.Model):
#     user = models.ForeignKey(registertable, on_delete=models.CASCADE, null=True, blank=True)
#
#     name = models.CharField(max_length=300, null=True, blank=True)
#     descr = models.TextField(null=True, blank=True)
#     image = models.FileField(upload_to="machinary", null=True, blank=True)
#     farmer = models.BooleanField(default=False)
#     aggregator = models.BooleanField(default=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name_plural = "Pesticides"
#
#
# STATUS_CHOICES = (
#     ("Pending", "Pending"),
#     ("Shipped", "Shipped"),
#     ("Delivered", "Delivered")
# )
#
#
# class orderstable(models.Model):
#     user = models.ForeignKey(registertable, on_delete=models.CASCADE, null=True, blank=True)
#     orderid = models.CharField(max_length=100, null=True, blank=True)
#     paymentid = models.CharField(max_length=100, null=True, blank=True)
#     productname = models.CharField(max_length=300, null=True, blank=True)
#     price = models.CharField(max_length=20, null=True, blank=True)
#     status = models.CharField(
#         choices=STATUS_CHOICES,
#         max_length=20,
#         default="Pending", null=True, blank=True
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.orderid
#
#     class Meta:
#         verbose_name_plural = "Orders"
#
#
# class querymodels(models.Model):
#     name = models.CharField(max_length=256, null=True, blank=True)
#     email = models.EmailField(max_length=256, null=True, blank=True)
#     phone = models.CharField(max_length=20, null=True, blank=True)
#     subject = models.CharField(max_length=256, null=True, blank=True)
#     query = models.TextField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.subject
#
#     class Meta:
#         verbose_name_plural = "User Queries"
