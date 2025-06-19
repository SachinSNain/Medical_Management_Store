import ttkbootstrap as ttk
from ttkbootstrap import Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from db import with_cursor


@with_cursor
def get_sales_data(conn, cur):
    cur.execute("""
        SELECT createdOn, SUM(Amount) AS total_sales
        FROM billing_tran
        WHERE createdOn >= CURDATE() - INTERVAL 7 DAY
        GROUP BY createdOn;
    """)
    data = cur.fetchall()
    data.sort(key=lambda x: x[0])
    return data


@with_cursor
def get_mostly_sold_item(conn, cur):
    cur.execute("""
        SELECT MedicineName, SUM(Qty) AS total_qty
        FROM billing_tran
        WHERE createdOn >= CURDATE() - INTERVAL 7 DAY
        GROUP BY MedicineName
        ORDER BY total_qty DESC;
    """)
    return cur.fetchall()


@with_cursor
def get_items_near_expiry(conn, cur):
    cur.execute("""
        SELECT MedicineName, DATEDIFF(ExpiryDate, CURDATE()) AS days_to_expire
        FROM medicine_m
        WHERE ExpiryDate BETWEEN CURDATE() AND CURDATE() + INTERVAL 1 MONTH
        ORDER BY days_to_expire DESC;
    """)
    return cur.fetchall()


def open_report_section(app):
    reports_window = Toplevel(app)
    reports_window.title("Reports")
    reports_window.minsize(1050, 530)

    sales_data = get_sales_data()

    ttk.Label(
        reports_window,
        text="Welcome To MedPay Medical Store Reports",
        font=("Arial", 18)
    ).pack(pady=10)

    def generate_reports():
        dates = [x[0].strftime('%Y-%m-%d') for x in sales_data]
        total_sales = [x[1] for x in sales_data]

        mostly_sold = get_mostly_sold_item()
        near_expiry = get_items_near_expiry()

        medicine_names = [x[0] for x in mostly_sold[:2]]
        quantities = [x[1] for x in mostly_sold[:2]]

        fig = Figure(figsize=(10, 8))
        axes = fig.subplots(3, 1)

        # Sales Bar Chart
        axes[0].bar(dates, total_sales)
        axes[0].set_title("Billing Sales Bar Chart (Last 7 Days)")
        axes[0].set_xlabel("Date")
        axes[0].set_ylabel("Total Sales")

        # Top Sold Items Pie Chart
        axes[1].pie(quantities, labels=medicine_names, autopct="%1.1f%%")
        axes[1].set_title("Top 2 Sold Item Pie Chart")

        # Near Expiry Bar Chart
        med_names = [item[0] for item in near_expiry]
        days_left = [item[1] for item in near_expiry]
        axes[2].bar(med_names, days_left, color='red')
        axes[2].set_title("Items Near Expiry in a Month")
        axes[2].set_xlabel("Medicine Name")
        axes[2].set_ylabel("Days to Expiry")
        axes[2].tick_params(axis='x', rotation=45)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=reports_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=ttk.TOP, fill=ttk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, reports_window)
        toolbar.update()
        toolbar.pack(side=ttk.BOTTOM, fill=ttk.X)

    ttk.Button(
        reports_window,
        text="Generate MedPay Medical Store Reports",
        command=generate_reports,
        bootstyle="primary"
    ).pack(pady=10)

    ttk.Label(reports_window, text="Total Sales Today: 0", bootstyle="info")\
        .pack(pady=5)
    ttk.Label(reports_window, text="Out of Stock Items: 0", bootstyle="info")\
        .pack(pady=5)
