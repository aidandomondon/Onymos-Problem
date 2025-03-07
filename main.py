# Order class to represent each buy or sell order
class Order:
    def __init__(self, order_type, ticker, quantity, price):
        self.order_type = order_type  # Either 'Buy' or 'Sell'
        self.ticker = ticker
        self.quantity = quantity
        self.price = price
        self.next = None

# StockOrderBook class that stores buy and sell orders for each ticker
class StockOrderBook:
    def __init__(self):
        # Using a linked list
        self.buy_head = None
        self.sell_head = None

    # Adds an order to the book
    def addOrder(self, order_type, ticker, quantity, price):
        new_order = Order(order_type, ticker, quantity, price)

        # Inserts the order in the correct position 
        if order_type == 'Buy':
            # Insert buy orders in descending price order (highest first)
            if not self.buy_head or self.buy_head.price <= price:
                new_order.next = self.buy_head
                self.buy_head = new_order
            else:
                current = self.buy_head
                while current.next and current.next.price > price:
                    current = current.next
                new_order.next = current.next
                current.next = new_order
        elif order_type == 'Sell':
            # Insert sell orders in ascending price order (lowest first)
            if not self.sell_head or self.sell_head.price >= price:
                new_order.next = self.sell_head
                self.sell_head = new_order
            else:
                current = self.sell_head
                while current.next and current.next.price < price:
                    current = current.next
                new_order.next = current.next
                current.next = new_order

    # Function to match orders in the order book
    def matchOrder(self):
        matched_orders = []
        
        buy_order = self.buy_head
        sell_order = self.sell_head
        while buy_order and sell_order:
            if buy_order.price >= sell_order.price:
                matched_quantity = min(buy_order.quantity, sell_order.quantity)
                matched_orders.append({
                    'buy_price': buy_order.price,
                    'sell_price': sell_order.price,
                    'quantity': matched_quantity,
                    'ticker': buy_order.ticker
                })
                buy_order.quantity -= matched_quantity
                sell_order.quantity -= matched_quantity
                
                if buy_order.quantity == 0:
                    self.buy_head = buy_order.next
                if sell_order.quantity == 0:
                    self.sell_head = sell_order.next
                
                # Move to the next orders
                if buy_order.quantity > 0:
                    buy_order = buy_order.next
                if sell_order.quantity > 0:
                    sell_order = sell_order.next
            else:
                break  # No more possible matches
        
        return matched_orders

# A wrapper function that randomly executes orders
def simulate_order_activity(stock_order_book):
    tickers = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA']
    
    while True:
        order_type = ['Buy', 'Sell'][int(random(0, 2))]  # Simulate random choice of order type
        ticker = tickers[int(random(0, 5))]  # Randomly pick a ticker
        quantity = int(random(1, 100))  # Random quantity between 1 and 100
        price = int(random(100, 1500))  # Random price between 100 and 1500
        
        stock_order_book.addOrder(order_type, ticker, quantity, price)
        
        # Simulate random delay between orders
        time_sleep(random(0.1, 1.0))  # Simulate random delay

# Main execution function
def main():
    stock_order_book = StockOrderBook()
    
    # Simulate stock transactions in parallel using basic function calls
    while True:
        # Simulate matching orders in the order book every 2 seconds
        matched_orders = stock_order_book.matchOrder()
        if matched_orders:
            for order in matched_orders:
                print(f"Matched {order['quantity']} units of {order['ticker']} at Buy Price: {order['buy_price']}, Sell Price: {order['sell_price']}")
        
        time_sleep(2)  # Match orders every 2 seconds

# Helper function to simulate random number generation
def random(min_val, max_val):
    # simple rng
    return min_val + (max_val - min_val) * 0.5

# Helper function to simulate sleep (delay)
def time_sleep(seconds):
    start_time = 0  # Simulate the current time by a variable
    end_time = seconds  # Set end time as the specified sleep duration
    
    while start_time < end_time:
        start_time += 0.001  # Simulate passage of time by incrementing small steps
        # In a real environment, this would be tied to a system clock or timer
        pass  # Busy-wait loop

if __name__ == "__main__":
    main()
