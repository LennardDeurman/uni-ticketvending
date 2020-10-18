import tkinter as tk
from datetime import datetime
from ui_info import UIPayment, UIInfo, UIWay
from stations.station_register import StationRegister
from orders.order_register import OrderRegister
from orders.lineitem import LineItem, TicketSpecification
from orders.enums import ClassType, DiscountRate
from payments.payment_operation import PaymentOperation, PaymentResponse


class UI(tk.Frame):

	station_register : StationRegister = StationRegister()

	order_register : OrderRegister = OrderRegister()

	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.widgets()

	def widgets(self):
		self.master.title("Ticket machine")
		menubar = tk.Menu(self.master)
		self.master.config(menu=menubar)

		fileMenu = tk.Menu(menubar)
		fileMenu.add_command(label="Exit", command=self.on_exit)
		menubar.add_cascade(label="File", menu=fileMenu)

		all_stations = self.station_register.find_all()
		station_names = list(map(lambda x: x.name, all_stations))

		stations_frame = tk.Frame(self.master, highlightbackground="#cccccc", highlightthickness=1)
		stations_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)
		# From station
		tk.Label(stations_frame, text = "From station:").grid(row=0, padx=5, sticky=tk.W)
		self.from_station = tk.StringVar(value=station_names[0])
		tk.OptionMenu(stations_frame, self.from_station, *station_names).grid(row=1, padx=5, sticky=tk.W)

		# To station
		tk.Label(stations_frame, text = "To station:").grid(row=0, column=1, sticky=tk.W)
		self.to_station = tk.StringVar(value=station_names[0])
		tk.OptionMenu(stations_frame, self.to_station, *station_names).grid(row=1, column=1, sticky=tk.W)

		ticket_options_frame = tk.Frame(self.master, highlightbackground="#cccccc", highlightthickness=1)
		ticket_options_frame.pack(fill=tk.BOTH, expand=1, padx=10)

		# Class
		tk.Label(ticket_options_frame, text = "Travel class:").grid(row=1, sticky=tk.W)
		self.travel_class = tk.IntVar(value=ClassType.SecondClass.value)
		tk.Radiobutton(ticket_options_frame, text="First class", variable=self.travel_class, value=ClassType.FirstClass.value).grid(row=5, sticky=tk.W)
		tk.Radiobutton(ticket_options_frame, text="Second class", variable=self.travel_class, value=ClassType.SecondClass.value).grid(row=6, sticky=tk.W)

		# Way
		tk.Label(ticket_options_frame, text = "Way:").grid(row=7, sticky=tk.W)
		self.way = tk.IntVar(value=UIWay.OneWay.value)
		tk.Radiobutton(ticket_options_frame, text="One-way", variable=self.way, value=UIWay.OneWay.value).grid(row=8, sticky=tk.W)
		tk.Radiobutton(ticket_options_frame, text="Return", variable=self.way, value=UIWay.Return.value).grid(row=9, sticky=tk.W)

		# Discount
		tk.Label(ticket_options_frame, text = "Discount:").grid(row=10, sticky=tk.W)
		self.discount = tk.IntVar(value=DiscountRate.NoDiscount.value)
		tk.Radiobutton(ticket_options_frame, text="No discount", variable=self.discount, value=DiscountRate.NoDiscount.value).grid(row=11, sticky=tk.W)
		tk.Radiobutton(ticket_options_frame, text="20% discount", variable=self.discount, value=DiscountRate.TwentyDiscount.value).grid(row=12, sticky=tk.W)
		tk.Radiobutton(ticket_options_frame, text="40% discount", variable=self.discount, value=DiscountRate.FortyDiscount.value).grid(row=13, sticky=tk.W)

		payment_frame = tk.Frame(self.master, highlightbackground="#cccccc", highlightthickness=1)
		payment_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

		# Payment
		tk.Label(payment_frame, text = "Payment:").grid(row=14, sticky=tk.W) 
		self.payment = tk.IntVar(value=UIPayment.Cash.value)
		tk.Radiobutton(payment_frame, text="Cash", variable=self.payment, value=UIPayment.Cash.value).grid(row=15, sticky=tk.W)
		tk.Radiobutton(payment_frame, text="Credit Card", variable=self.payment, value=UIPayment.CreditCard.value).grid(row=16, sticky=tk.W)
		tk.Radiobutton(payment_frame, text="Debit Card", variable=self.payment, value=UIPayment.DebitCard.value).grid(row=17, sticky=tk.W)

		# Pay button
		tk.Button(self.master, text="Pay", command=self.on_click_pay).pack(side=tk.RIGHT, ipadx=10, padx=10, pady=10)

		self.pack(fill=tk.BOTH, expand=1)


	def handle_payment(self, order_price, payment) -> PaymentResponse:
		payment_operation = PaymentOperation(order_price)
		if payment == UIPayment.CreditCard:
			return payment_operation.pay_with_creditcard()
		elif payment == UIPayment.DebitCard:
			return payment_operation.pay_with_debitcard()
		elif payment == UIPayment.Cash:
			return payment_operation.pay_by_cash()
		return None

	def on_click_pay(self):
		ui_info = self.get_ui_info()
		arrival = self.station_register.find_by_name(ui_info.to_station)
		departure = self.station_register.find_by_name(ui_info.from_station)
		
		line_items = [
			LineItem(
				specification=TicketSpecification(
					validity_date=datetime.now(),
					arrival=arrival,
					departure=departure,
					is_retour=ui_info.is_retour,
					discount=ui_info.discount,
					class_type=ui_info.travel_class
				),
				quantity=1,
			)
		]

		
		new_order = self.order_register.create_new(
			line_items=line_items
		)

		order_price = new_order.calculate_price()
		payment_response = self.handle_payment(order_price, ui_info.payment)
		
		self.order_register.finish(new_order, payment_response=payment_response)		

		
	
		


		

	def get_ui_info(self) -> UIInfo:
		return UIInfo(from_station=self.from_station.get(),
			to_station=self.to_station.get(),
			travel_class=self.travel_class.get(),
			way=self.way.get(),
			discount=self.discount.get(),
			payment=self.payment.get())

	def on_exit(self):
		self.quit()

#endregion


def main():
 
	root = tk.Tk()
	UI(root)

	root.mainloop() 


if __name__ == '__main__':
	main()
