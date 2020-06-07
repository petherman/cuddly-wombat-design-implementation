from app import app
from collections import Counter
from app.models import MenuItem

class Report():
    
    def __init__(self,orders,reservations):
        self.orders = orders
        self.total = 0
        self.num_orders = len(self.orders)
        self.num_guests = 0
        self.reservations = reservations
        self.most_popular_item = None
        self.get_num_guests()
        self.get_most_popular_item()
        self.total_revenue()
        
    def total_revenue(self):
        self.total = 0
        for order in self.orders:
            self.total += order.total
        #return(self.total)
    
    def num_orders(self):
        return(self.num_orders)
    
    def get_num_guests(self):
        self.num_guests = 0
        for reservation in self.reservations:
            self.num_guests += reservation.party_size
        return(self.num_guests)    
    
    def get_most_popular_item(self):
        list_of_items = []
        for order in self.orders:
            for order_item in order.order_items:
                list_of_items.append(order_item.ordered_item_id)
        most_common = Counter(list_of_items).most_common(1)
        for item_id, item_amount in most_common:
            app.logger.info('%s %s', item_id, item_amount)
            self.most_popular_item = MenuItem.query.filter_by(id=item_id).first()
            item_counter = item_amount
        app.logger.info('Most common item: %s', self.most_popular_item.name)
        
        
        

                        