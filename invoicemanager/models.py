from __future__ import unicode_literals

from django.core.files.storage import FileSystemStorage
from django.db import models

# Create your models here.
class Customer(models.Model):
	name = models.CharField(max_length=256)
	address1 = models.CharField(max_length=256, blank=True)
	address2 = models.CharField(max_length=256, blank=True)
	city = models.CharField(max_length=128, blank=True)
	state = models.CharField(max_length=2, blank=True)
	zip = models.CharField(max_length=12, blank=True)
	email = models.CharField(max_length=256, blank=True)

	def __str__(self):
		return self.name
	
	def invoices(self):
		return Invoice.objects.filter(customer=self).count()

class Invoice(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	date = models.DateField()
	status = models.CharField(max_length=10)

	def __str__(self):
	    return str(self.id)

	def total_items(self):
		total = 0
		items = self.invoiceitem_set.all()

		for item in items:
			total += item.cost * item.qty

		return total

	def total_expenses(self):
		total = 0
		expenses = self.expense_set.all()

		for expense in expenses:
			total += expense.cost * expense.qty

		return total

	def total(self):
		items = self.total_items()
		expenses = self.total_expenses()

		return items - expenses
		
	def paid(self):
		return self.status == 'Paid'
		
	def unpaid(self):
		return self.status == 'Unpaid'
		
	def draft(self):
		return self.status == 'Draft'

class InvoiceItem(models.Model):
	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
	name = models.CharField(max_length=128)
	description = models.TextField()
	cost = models.DecimalField(decimal_places=2, max_digits=10)
	qty = models.IntegerField()

	def total(self):
		return self.cost * self.qty

class Expense(models.Model):
	description = models.TextField()
	cost = models.DecimalField(decimal_places=2, max_digits=10)
	qty = models.IntegerField()
	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, null=True)
	date = models.DateField(blank=True, null=True)
		
	def total(self):
		return self.cost * self.qty

	def is_business_expense(self):
		return self.invoice is None

class InvoiceAttachment(models.Model):
	file = models.FileField(upload_to='invoice/')
	displayname = models.CharField(max_length=128)
	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

class ExpenseAttachment(models.Model):
	file = models.FileField(upload_to='expense/')
	displayname = models.CharField(max_length=128)
	expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
