import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from PIL import Image

from datetime import datetime
import random
import string
import os

# ---------------- GLOBAL ----------------
selected_dates = []
PAGE_W, PAGE_H = A4
RECEIPT_W = PAGE_W * 0.70
RECEIPT_X = (PAGE_W - RECEIPT_W) / 2
RECEIPT_BG = HexColor("#EDEDED")  # light receipt gray

pdfmetrics.registerFont(
    TTFont("Thermal", "assets/MerchantCopy.ttf")
)

# ---------------- GST ----------------
def generate_gstin():
    #return "33ABCDE1234F1Z" + str(random.randint(1, 9))
    return "33ABCDE1234F1Z8"
    
# -----------------RANDOM TIME-------------------    
def random_time(start_hour=6, end_hour=22):
    hour = random.randint(start_hour, end_hour)
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}"

# ---------------- IMAGE UTILS ----------------
def grayscale_image(path):
    img = Image.open(path).convert("L")
    temp = path.replace(".png", "_gray.png")
    img.save(temp)
    return temp

def draw_center_logo(c, path, cx, y, max_width_mm):
    if not os.path.exists(path):
        return y

    gray = grayscale_image(path)
    img = Image.open(gray)
    iw, ih = img.size

    scale = (max_width_mm * mm) / iw
    w = iw * scale
    h = ih * scale

    c.drawImage(ImageReader(img), cx - w/2, y - h, width=w, height=h, mask="auto")
    return y - h - 8

def draw_hdfc_vertical(c, path):
    if not os.path.exists(path):
        return

    img = Image.open(path).convert("L").rotate(90, expand=True)
    iw, ih = img.size

    x = RECEIPT_X + RECEIPT_W - iw - 75
    y = PAGE_H / 2 - ih / 2

    c.drawImage(ImageReader(img), x, y, mask="auto")

def generate_consolidated_report(dates):
    os.makedirs("bills", exist_ok=True)

    today = datetime.now().strftime("%Y%m%d")
    report_file = f"bills/report_consolidated_{today}.pdf"
    receipt_no = random.randint(10000, 99999)
    gstin = generate_gstin()
    rate = round(random.uniform(100.50, 102.90), 2)
    amount = random.randint(4000, 5000)
    volume = round(amount / rate, 2)

    WIDTH, HEIGHT = A4
    RECEIPT_W = WIDTH * 0.45
    RECEIPT_H = HEIGHT * 0.70

    rx = (WIDTH - RECEIPT_W) / 2
    ry = (HEIGHT - RECEIPT_H) / 2
    
    c = canvas.Canvas(report_file, pagesize=A4)
    

    for bill_date in dates:
         # ----- Gray receipt background -----
         c.setFillColor(HexColor("#eeeeee"))
         c.roundRect(rx, ry, RECEIPT_W, RECEIPT_H, 8, fill=1, stroke=0)
         c.setFillColor(HexColor("#000000"))
    
         y = ry + RECEIPT_H - 18
    
         # ----- Logos -----
         logo = "assets/bp.png" if company_var.get() == "Bharat Petroleum" else "assets/iocl.jpg"
         y = draw_center_logo(c, logo, rx + RECEIPT_W/2, y, 35)
         draw_hdfc_vertical(c, "assets/hdfc.png")
    
         # ----- Text writer -----
         def line(txt, bold=True, center=False, gap=14):
             nonlocal y
             #c.setFont("Courier-Bold" if bold else "Courier", 9.5)
             c.setFont("Thermal", 20)
             if center:
                 c.drawCentredString(rx + RECEIPT_W/2, y, txt)
             else:
                 c.drawString(rx + 10, y, txt)
             y -= gap
    
         # ----- Content -----
         line("")
         line(company_var.get().upper(), center=True)
         line("WELCOME !!!", center=True)
         line("")
         line("")
         line(f"GST NO : {gstin}")
         for l in address_entry.get("1.0", tk.END).strip().upper().split("\n"):
             line(l, bold=False, gap=12)
    
         line("")
         line(f"RECEIPT NO : {receipt_no}")
         line(f"DATE : {bill_date.strftime('%d %b %Y')}   TIME : {random_time()}")
    
         line("")
         line("PRODUCT : PETROL")
         line(f"RATE/LTR : {rate}")
         line(f"AMOUNT   : {amount}")
         line(f"VOLUME   : {volume} LT")
    
         line("")
         line(f"VEH NO   : {vehicle_entry.get().upper()}")
         line("MODE     : CASH")
    
         line("")
         line("")
         line("")
         line("")
         line("")
         line("")
         line("")
         line("SAVE FUEL YAANI SAVE MONEY", center=True)    
         line("THANK YOU – VISIT AGAIN", center=True)

         c.showPage()

    c.save()

# ---------------- RECEIPT ----------------
def generate_single_receipt(bill_date):
    os.makedirs("bills", exist_ok=True)

    receipt_no = random.randint(10000, 99999)
    gstin = generate_gstin()
    rate = round(random.uniform(100.50, 102.90), 2)
    amount = random.randint(4000, 5000)
    volume = round(amount / rate, 2)

    WIDTH, HEIGHT = A4
    RECEIPT_W = WIDTH * 0.45
    RECEIPT_H = HEIGHT * 0.70

    rx = (WIDTH - RECEIPT_W) / 2
    ry = (HEIGHT - RECEIPT_H) / 2

    file = f"bills/RECEIPT_{receipt_no}_{bill_date.strftime('%d%m%Y')}.pdf"

    #file = f"bills/RECEIPT_Consolidated.pdf"
    c = canvas.Canvas(file, pagesize=A4)
    
    # ----- Gray receipt background -----
    c.setFillColor(HexColor("#eeeeee"))
    c.roundRect(rx, ry, RECEIPT_W, RECEIPT_H, 8, fill=1, stroke=0)
    c.setFillColor(HexColor("#000000"))

    y = ry + RECEIPT_H - 18

    # ----- Logos -----
    logo = "assets/bp.png" if company_var.get() == "Bharat Petroleum" else "assets/iocl.jpg"
    y = draw_center_logo(c, logo, rx + RECEIPT_W/2, y, 35)
    draw_hdfc_vertical(c, "assets/hdfc.png")

    # ----- Text writer -----
    def line(txt, bold=True, center=False, gap=14):
        nonlocal y
        #c.setFont("Courier-Bold" if bold else "Courier", 9.5)
        c.setFont("Thermal", 20)
        if center:
            c.drawCentredString(rx + RECEIPT_W/2, y, txt)
        else:
            c.drawString(rx + 10, y, txt)
        y -= gap

    # ----- Content -----
    line("")
    line(company_var.get().upper(), center=True)
    line("WELCOME !!!", center=True)
    line("")
    line("")
    line(f"GST NO : {gstin}")
    for l in address_entry.get("1.0", tk.END).strip().upper().split("\n"):
        line(l, bold=False, gap=12)

    line("")
    line(f"RECEIPT NO : {receipt_no}")
    line(f"DATE : {bill_date.strftime('%d %b %Y')}   TIME : {random_time()}")

    line("")
    line("PRODUCT : PETROL")
    line(f"RATE/LTR : {rate}")
    line(f"AMOUNT   : {amount}")
    line(f"VOLUME   : {volume} LT")

    line("")
    line(f"VEH NO   : {vehicle_entry.get().upper()}")
    line("MODE     : CASH")

    line("")
    line("")
    line("")
    line("")
    line("")
    line("")
    line("")
    line("SAVE FUEL YAANI SAVE MONEY", center=True)    
    line("THANK YOU – VISIT AGAIN", center=True)

    c.showPage()
    c.save()

# ---------------- BULK ----------------
def generate_receipts():
    if not selected_dates:
        messagebox.showerror("Error", "Select dates")
        return

    if not vehicle_entry.get().strip() or not address_entry.get("1.0", tk.END).strip():
        messagebox.showerror("Error", "Vehicle & address required")
        return

    for d in selected_dates:
        generate_single_receipt(d)
        
    generate_consolidated_report(selected_dates)

    messagebox.showinfo("Done", f"{len(selected_dates)} receipts generated")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Petrol Receipt Generator")
root.geometry("520x680")

tk.Label(root, text="Petrol Receipt Generator", font=("Arial", 16, "bold")).pack(pady=10)

company_var = tk.StringVar(value="Bharat Petroleum")
ttk.Combobox(
    root,
    textvariable=company_var,
    values=["Bharat Petroleum", "Indian Oil"],
    state="readonly",
    width=25
).pack(pady=5)

tk.Label(root, text="Select Date").pack()
date_entry = DateEntry(root, date_pattern="dd-mm-yyyy")
date_entry.pack()

def add_date():
    d = date_entry.get_date()
    if d not in selected_dates:
        selected_dates.append(d)
        dates_list.insert(tk.END, d.strftime("%d-%m-%Y"))

tk.Button(root, text="Add Date", command=add_date).pack(pady=5)

dates_list = tk.Listbox(root, height=6)
dates_list.pack()

tk.Label(root, text="Vehicle Number").pack()
vehicle_entry = tk.Entry(root, width=30)
vehicle_entry.pack()
vehicle_entry.insert(0, "TN04 BT1234")

tk.Label(root, text="Outlet Address").pack()
address_entry = tk.Text(root, height=4, width=45)
address_entry.pack()
address_entry.insert("1.0", "BP SRI RAMACHANDRA AGENCIES\nPERAMBUR, CHENNAI 600011")
#address_entry.insert("2.0", "PERAMBUR CHENNAI 600011")

tk.Button(
    root,
    text="Generate Receipts",
    bg="black",
    fg="white",
    font=("Arial", 11, "bold"),
    command=generate_receipts
).pack(pady=20)

root.mainloop()
