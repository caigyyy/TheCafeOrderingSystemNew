import tkinter as tk
from tkinter import ttk, messagebox
from uuid import uuid4

from menu import Menu
from menu_item_factory import MenuItemFactory
from customer import Customer
from order_system import OrderSystem
from bill import Bill
from payment_service import PaymentService
from gui_order_observer import GuiOrderObserver

MIN_PHONE_LEN = 8  
MAX_PHONE_LEN = 15  


class CafeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cafe Ordering System (Tkinter)")
        self.geometry("980x650")

        self.menu = Menu(menu_id="M1", title="Local Café Menu")
        self.system = None
        self.customer = None
        self.order = None

        self.tax_rate_var = tk.DoubleVar(value=0.15)

        self._seed_demo_data()
        self._build_ui()
        self._refresh_menu_list()
        self._set_order_controls_enabled(False)
        self._validate_customer_fields()

    # Menu data 
    def _seed_demo_data(self):
        drinks = [
            ("D1", "Espresso", "Single espresso shot.", 2.50, "S", True),
            ("D2", "Americano", "Espresso topped with hot water.", 3.00, "M", True),
            ("D3", "Cappuccino", "Espresso with steamed milk and foam.", 3.50, "M", True),
            ("D4", "Latte", "Espresso with steamed milk (light foam).", 3.80, "L", True),
            ("D5", "Flat white", "Stronger coffee with velvety microfoam.", 3.70, "M", True),
            ("D6", "Mocha", "Latte with chocolate.", 4.10, "L", True),
            ("D7", "Matcha", "Matcha latte (green tea).", 4.20, "L", True),
            ("D8", "Hot chocolate", "Rich chocolate drink.", 3.90, "L", True),
        ]
        for (item_id, name, desc, price, size, is_hot) in drinks:
            self.menu.add_item(
                MenuItemFactory.create_menu_item(
                    "drink",
                    id=item_id,
                    name=name,
                    description=desc,
                    price=price,
                    available=True,
                    size=size,
                    is_hot=is_hot,
                )
            )

        foods = [
            ("F1", "Sandwiches",
             "Selection of sandwiches (ask for today's options).",
             6.50, "Contains gluten"),
            ("F2", "Paninis",
             "Pressed panini (ask for fillings).",
             7.00, "Contains gluten"),
            ("F3", "Wraps",
             "Fresh wraps (ask for fillings).",
             6.80, "Contains gluten"),
            ("F4", "Salads",
             "Fresh salad bowl (ask for today's options).",
             6.20, "Vegetarian options available"),
            ("F5", "Soup of the day",
             "Ask staff for today's soup.",
             4.80, "May contain allergens"),
            ("F6", "Craigoll the Bagel Special",
             "Toasted bagel special (ask for today's filling).",
             7.20, "Contains gluten"),
        ]
        for (item_id, name, desc, price, dietary_info) in foods:
            self.menu.add_item(
                MenuItemFactory.create_menu_item(
                    "food",
                    id=item_id,
                    name=name,
                    description=desc,
                    price=price,
                    available=True,
                    dietary_info=dietary_info,
                )
            )

    # UI layout 
    def _build_ui(self):
        root = ttk.Frame(self, padding=10)
        root.pack(fill="both", expand=True)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=2)
        root.rowconfigure(1, weight=1)

        # Customer details
        customer = ttk.LabelFrame(root, text="Customer details (required)")
        customer.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        for i in range(6):
            customer.columnconfigure(i, weight=1)

        ttk.Label(customer, text="Full name").grid(
            row=0, column=0, sticky="w", padx=8, pady=8
        )
        self.user_name_var = tk.StringVar()
        self.user_name_var.trace_add("write", lambda *_: self._validate_customer_fields())
        ttk.Entry(customer, textvariable=self.user_name_var).grid(
            row=0, column=1, sticky="ew", padx=(0, 8), pady=8
        )

        ttk.Label(customer, text="Phone").grid(
            row=0, column=2, sticky="w", padx=8, pady=8
        )
        self.user_phone_var = tk.StringVar()
        self.user_phone_var.trace_add("write", lambda *_: self._validate_customer_fields())
        ttk.Entry(customer, textvariable=self.user_phone_var).grid(
            row=0, column=3, sticky="ew", padx=(0, 8), pady=8
        )

        self.start_order_btn = ttk.Button(
            customer, text="Start Order", command=self.on_start_order
        )
        self.start_order_btn.grid(row=0, column=4, sticky="ew", padx=8, pady=8)

        self.customer_status_lbl = ttk.Label(customer, text="Status: Not started")
        self.customer_status_lbl.grid(row=0, column=5, sticky="w", padx=8, pady=8)

        # Left: Menu
        left = ttk.LabelFrame(root, text="Menu")
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        left.columnconfigure(0, weight=1)
        left.rowconfigure(2, weight=1)

        form = ttk.Frame(left)
        form.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        for i in range(4):
            form.columnconfigure(i, weight=1)

        ttk.Label(form, text="Type").grid(row=0, column=0, sticky="w")
        self.item_type = ttk.Combobox(form, values=["food", "drink"], state="readonly")
        self.item_type.set("drink")
        self.item_type.grid(row=1, column=0, sticky="ew", padx=(0, 6))

        ttk.Label(form, text="ID").grid(row=0, column=1, sticky="w")
        self.item_id = ttk.Entry(form)
        self.item_id.grid(row=1, column=1, sticky="ew", padx=(0, 6))

        ttk.Label(form, text="Name").grid(row=0, column=2, sticky="w")
        self.item_name = ttk.Entry(form)
        self.item_name.grid(row=1, column=2, sticky="ew", padx=(0, 6))

        ttk.Label(form, text="Price").grid(row=0, column=3, sticky="w")
        self.item_price = ttk.Entry(form)
        self.item_price.grid(row=1, column=3, sticky="ew")

        menu_btns = ttk.Frame(left)
        menu_btns.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        menu_btns.columnconfigure(0, weight=1)
        menu_btns.columnconfigure(1, weight=1)
        menu_btns.columnconfigure(2, weight=1)

        self.add_menu_btn = ttk.Button(
            menu_btns, text="Add Menu Item", command=self.on_add_menu_item
        )
        self.add_menu_btn.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.remove_menu_btn = ttk.Button(
            menu_btns, text="Remove Selected", command=self.on_remove_menu_item
        )
        self.remove_menu_btn.grid(row=0, column=1, sticky="ew", padx=(0, 6))

        self.toggle_menu_btn = ttk.Button(
            menu_btns, text="Toggle Availability", command=self.on_toggle_availability
        )
        self.toggle_menu_btn.grid(row=0, column=2, sticky="ew")

        self.menu_list = tk.Listbox(left, height=18)
        self.menu_list.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))

        order_add = ttk.Frame(left)
        order_add.grid(row=3, column=0, sticky="ew", padx=8, pady=(0, 10))
        order_add.columnconfigure(1, weight=1)

        ttk.Label(order_add, text="Qty").grid(row=0, column=0, sticky="w")
        self.qty_var = tk.IntVar(value=1)
        self.qty_spin = ttk.Spinbox(
            order_add, from_=1, to=99, textvariable=self.qty_var, width=6
        )
        self.qty_spin.grid(row=0, column=1, sticky="w")

        self.add_to_order_btn = ttk.Button(
            order_add, text="Add Selected to Order", command=self.on_add_to_order
        )
        self.add_to_order_btn.grid(row=0, column=2, sticky="e")

        # Right: Order + Bill
        right = ttk.Frame(root)
        right.grid(row=1, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

        top = ttk.LabelFrame(right, text="Current Order")
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(0, weight=1)

        self.order_table = ttk.Treeview(
            top,
            columns=("id", "name", "qty", "unit", "total"),
            show="headings",
            height=10,
        )
        for c, w in [("id", 90), ("name", 220), ("qty", 60), ("unit", 80), ("total", 90)]:
            self.order_table.heading(c, text=c.upper())
            self.order_table.column(c, width=w, anchor="w")
        self.order_table.grid(row=0, column=0, sticky="ew", padx=8, pady=8)

        order_actions = ttk.Frame(top)
        order_actions.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        for i in range(5):
            order_actions.columnconfigure(i, weight=1)

        self.remove_line_btn = ttk.Button(
            order_actions, text="Remove Selected Line", command=self.on_remove_order_line
        )
        self.remove_line_btn.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.clear_order_btn = ttk.Button(
            order_actions, text="Clear Order", command=self.on_clear_order
        )
        self.clear_order_btn.grid(row=0, column=1, sticky="ew", padx=(0, 6))

        ttk.Label(order_actions, text="Tax rate").grid(
            row=0, column=2, sticky="e", padx=(0, 6)
        )
        self.tax_entry = ttk.Entry(
            order_actions, textvariable=self.tax_rate_var, width=8
        )
        self.tax_entry.grid(row=0, column=3, sticky="w")

        self.refresh_totals_btn = ttk.Button(
            order_actions, text="Refresh totals", command=self._refresh_totals
        )
        self.refresh_totals_btn.grid(row=0, column=4, sticky="ew")

        bottom = ttk.LabelFrame(right, text="Bill")
        bottom.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
        bottom.columnconfigure(0, weight=1)
        bottom.rowconfigure(1, weight=1)

        totals = ttk.Frame(bottom)
        totals.grid(row=0, column=0, sticky="ew", padx=8, pady=8)

        self.subtotal_lbl = ttk.Label(totals, text="Subtotal: 0.00")
        self.subtotal_lbl.grid(row=0, column=0, sticky="w", padx=(0, 12))

        self.tax_lbl = ttk.Label(totals, text="Tax: 0.00")
        self.tax_lbl.grid(row=0, column=1, sticky="w", padx=(0, 12))

        self.total_lbl = ttk.Label(totals, text="Total: 0.00")
        self.total_lbl.grid(row=0, column=2, sticky="w")

        bill_btns = ttk.Frame(bottom)
        bill_btns.grid(row=2, column=0, sticky="ew", padx=8, pady=8)
        bill_btns.columnconfigure(0, weight=1)
        bill_btns.columnconfigure(1, weight=1)

        self.generate_bill_btn = ttk.Button(
            bill_btns, text="Generate Bill", command=self.on_generate_bill
        )
        self.generate_bill_btn.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.pay_btn = ttk.Button(
            bill_btns, text="Pay (Simulate)", command=self.on_pay
        )
        self.pay_btn.grid(row=0, column=1, sticky="ew")

        self.bill_text = tk.Text(bottom, height=14, wrap="word")
        self.bill_text.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))

    # Validation helpers 
    def _is_valid_phone(self, phone: str) -> bool:
        phone = phone.strip()
        if not phone.isdigit():
            return False
        return MIN_PHONE_LEN <= len(phone) <= MAX_PHONE_LEN

    def _validate_customer_fields(self):
        name = self.user_name_var.get().strip()
        phone = self.user_phone_var.get().strip()
        ok = bool(name) and self._is_valid_phone(phone)
        self.start_order_btn.configure(state="normal" if ok else "disabled")

    def _set_order_controls_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.menu_list.configure(state=state)
        self.qty_spin.configure(state=state)
        self.add_to_order_btn.configure(state=state)
        self.remove_line_btn.configure(state=state)
        self.clear_order_btn.configure(state=state)
        self.tax_entry.configure(state=state)
        self.refresh_totals_btn.configure(state=state)
        self.generate_bill_btn.configure(state=state)
        self.pay_btn.configure(state=state)
        self.bill_text.configure(state=state)

    # Customer / Order start 
    def on_start_order(self):
        name = self.user_name_var.get().strip()
        phone = self.user_phone_var.get().strip()

        if not name:
            messagebox.showwarning("Customer", "Please enter your full name.")
            return
        if not self._is_valid_phone(phone):
            messagebox.showwarning(
                "Customer",
                f"Phone must be digits only and {MIN_PHONE_LEN}-{MAX_PHONE_LEN} digits long.",
            )
            return

        self.customer = Customer(customer_id=str(uuid4()), full_name=name, phone=phone)
        self.system = OrderSystem()
        self.order = self.system.create_order(self.customer)

        # Attach GUI observer so any order change refreshes the UI
        self.order.add_observer(GuiOrderObserver(self))

        self.customer_status_lbl.configure(text=f"Status: Active ({name})")
        self._set_order_controls_enabled(True)
        self._refresh_order_table()
        self._refresh_totals()

    # Menu handlers 
    def on_add_menu_item(self):
        try:
            t = self.item_type.get().strip()
            item_id = self.item_id.get().strip()
            name = self.item_name.get().strip()
            price = float(self.item_price.get().strip())
            if not item_id or not name:
                raise ValueError("ID and Name are required.")
            item = MenuItemFactory.create_menu_item(
                t, id=item_id, name=name, description="", price=price, available=True
            )
            self.menu.add_item(item)
            self._refresh_menu_list()
            messagebox.showinfo("Menu", f"Added menu item: {item_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_remove_menu_item(self):
        item_id = self._selected_menu_item_id()
        if not item_id:
            messagebox.showwarning("Menu", "Select a menu item first.")
            return
        try:
            self.menu.remove_item(item_id)
            self._refresh_menu_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_toggle_availability(self):
        item_id = self._selected_menu_item_id()
        if not item_id:
            messagebox.showwarning("Menu", "Select a menu item first.")
            return
        try:
            item = self.menu.get_item(item_id)
            self.menu.set_availability(item_id, not item.available)
            self._refresh_menu_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Order handlers 
    def on_add_to_order(self):
        if self.order is None:
            return
        try:
            qty = int(self.qty_var.get())
            if qty < 1:
                raise ValueError
        except Exception:
            messagebox.showwarning(
                "Order", "Quantity must be a whole number (1 or more)."
            )
            return

        item_id = self._selected_menu_item_id()
        if not item_id:
            messagebox.showwarning("Order", "Select a menu item first.")
            return
        try:
            item = self.menu.get_item(item_id)
            self.order.add_item(item, qty)
            # UI also refreshed by observer, but keep these for safety
            self._refresh_order_table()
            self._refresh_totals()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_remove_order_line(self):
        if self.order is None:
            return
        selected = self.order_table.selection()
        if not selected:
            messagebox.showwarning("Order", "Select an order line first.")
            return
        item_id = self.order_table.item(selected[0], "values")[0]
        try:
            self.order.remove_item(item_id)
            self._refresh_order_table()
            self._refresh_totals()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_clear_order(self):
        if self.order is None:
            return
        for line in list(self.order.get_lines()):
            try:
                self.order.remove_item(line.item.id)
            except Exception:
                pass
        self._refresh_order_table()
        self._refresh_totals()
        self.bill_text.configure(state="normal")
        self.bill_text.delete("1.0", "end")
        self.bill_text.configure(state="normal")

    # Billing/Payment 
    def on_generate_bill(self):
        if self.order is None:
            return
        try:
            tax_rate = float(self.tax_rate_var.get())
            bill = Bill.generate_from(order=self.order, bill_id="BILL-UI", tax_rate=tax_rate)
            text = bill.to_text(self.order, cafe_name="Local Café")
            self.bill_text.configure(state="normal")
            self.bill_text.delete("1.0", "end")
            self.bill_text.insert("end", text)
            self.bill_text.configure(state="normal")
            self._refresh_totals()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_pay(self):
        if self.order is None:
            return
        try:
            tax_rate = float(self.tax_rate_var.get())
            bill = Bill.generate_from(order=self.order, bill_id="BILL-PAY", tax_rate=tax_rate)
            p = PaymentService().process_payment(bill.total)
            messagebox.showinfo(
                "Payment",
                f"Payment {p.status.value}\nAmount: {p.amount:.2f}\nID: {p.payment_id}",
            )

            # Immediately mark as PREPARING and update UI via observer
            from enums import OrderStatus
            self.order.set_status(OrderStatus.PREPARING)

            # After 1 minute (8000 ms), mark as READY.
            self.after(8000, self._mark_order_ready)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _mark_order_ready(self):
        """Called by Tkinter after delay to mark order as ready."""
        if self.order is None:
            return
        from enums import OrderStatus
        self.order.set_status(OrderStatus.READY)

    # Refresh helpers 
    def _refresh_menu_list(self):
        self.menu_list.delete(0, "end")
        for item in self.menu.list_items(only_available=False):
            flag = "Available" if item.available else "Unavailable"
            self.menu_list.insert(
                "end", f"{item.id} | {item.name} | {item.price:.2f} | {flag}"
            )

    def _refresh_order_table(self):
        for r in self.order_table.get_children():
            self.order_table.delete(r)
        if self.order is None:
            return
        for line in self.order.get_lines():
            self.order_table.insert(
                "",
                "end",
                values=(
                    line.item.id,
                    line.item.name,
                    line.qty,
                    f"{line.unit_price:.2f}",
                    f"{line.line_total():.2f}",
                ),
            )

    def _refresh_totals(self):
        if self.order is None:
            self.subtotal_lbl.config(text="Subtotal: 0.00")
            self.tax_lbl.config(text="Tax: 0.00")
            self.total_lbl.config(text="Total: 0.00")
            return
        try:
            sub = float(self.order.calculate_total())
            tax_rate = float(self.tax_rate_var.get())
            tax = round(sub * tax_rate, 2)
            total = round(sub + tax, 2)
            self.subtotal_lbl.config(text=f"Subtotal: {sub:.2f}")
            self.tax_lbl.config(text=f"Tax: {tax:.2f}")
            self.total_lbl.config(text=f"Total: {total:.2f}")
        except Exception:
            self.subtotal_lbl.config(
                text=f"Subtotal: {self.order.calculate_total():.2f}"
            )
            self.tax_lbl.config(text="Tax: (invalid rate)")
            self.total_lbl.config(text="Total: (invalid rate)")

    def _selected_menu_item_id(self):
        sel = self.menu_list.curselection()
        if not sel:
            return None
        row = self.menu_list.get(sel[0])
        return row.split("|")[0].strip()


if __name__ == "__main__":
    app = CafeApp()
    app.mainloop()
