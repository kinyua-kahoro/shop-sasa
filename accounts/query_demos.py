from unicodedata import category

from accounts.models import Customer, Order, Product

# returns all customers from customer table
customers = Customer.objects.all()

# returns first customer from table
firstCustomer = Customer.objects.first()

# returns last customer from table
lastCustomer = Customer.objects.last()

# returns single customer by name
customerByName = Customer.objects.get(name="Kinyua Kahoro")
customerById = Customer.objects.get(id=1)

# returns all orders related to customer(firstCustomer variable above)
firstCustomer.order_set.all()

# returns orders customer name(Query parent model names)
order = Order.objects.first()
parentName = order.customer.name

# returns products from products table with value of "Outdoor" in category attribute
products = Product.objects.filter(category="Outdoor")

# Order/Sort objects by id
leastToGreatest = Product.objects.all().order_by("id")
greatestToLeast = Product.objects.all().order_by("-id")

# returns all products with tag of "Sports"
productsFiltered = Product.objects.filter(tags__name="Sports")

# returns the total count for number of time a "Ball was ordered by the first customer
ballOrders = firstCustomer.order_set.filter(product_name="Ball").count()

# returns total count for each product ordered
allOrders = {}
for order in firstCustomer.order_set.all():
     if order.product_name in allOrders:
         allOrders[order.product_name] += 1
     else:
         allOrders[order.product_name] = 1

# returns: allOrders: {'Ball':2, 'BBQ Grill':1}