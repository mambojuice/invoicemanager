from django.contrib import admin

# Register your models here.
from .models import Customer
from .models import Invoice
from .models import InvoiceAttachment
from .models import ExpenseAttachment
from .models import Expense

admin.site.register(Customer)
admin.site.register(Invoice)
admin.site.register(Expense)