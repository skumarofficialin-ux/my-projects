# Fuel Bill Generator

A Python application for generating petrol receipt PDFs with a graphical user interface.

## Description

This application allows users to generate realistic-looking petrol station receipts in PDF format. It supports multiple dates, different fuel companies (Bharat Petroleum and Indian Oil), and generates both individual receipts and a consolidated report.

## Features

- GUI interface for easy receipt generation
- Support for multiple dates
- Company selection (Bharat Petroleum or Indian Oil)
- Customizable vehicle number and outlet address
- Generates PDF receipts with thermal printer-style formatting
- Includes logos and branding elements
- Random receipt numbers and transaction details
- Consolidated report generation

## Installation

1. Ensure you have Python 3.x installed
2. Install required dependencies:
   ```
   pip install tkcalendar reportlab pillow
   ```
3. Run the application:
   ```
   python main.py
   ```

## Dependencies

- tkinter (built-in with Python)
- tkcalendar
- reportlab
- pillow (PIL)

## Usage

1. Launch the application by running `main.py`
2. Select the fuel company from the dropdown
3. Choose a date using the date picker
4. Click "Add Date" to add multiple dates if needed
5. Enter the vehicle number
6. Enter the outlet address in the text box
7. Click "Generate Receipts" to create PDFs

Generated receipts will be saved in the `bills/` directory.

## Assets

The `assets/` folder should contain:
- `bp.png` - Bharat Petroleum logo
- `iocl.jpg` - Indian Oil logo
- `hdfc.png` - HDFC bank logo
- `MerchantCopy.ttf` - Thermal receipt font

## Output

- Individual receipt PDFs: `bills/RECEIPT_{receipt_no}_{date}.pdf`
- Consolidated report: `bills/report_consolidated_{today}.pdf`

## Notes

- Receipt details like GST number, rates, amounts, and volumes are randomly generated for demonstration purposes
- The application uses a thermal-style font to mimic receipt printers</content>
<parameter name="filePath">e:\Projects\Fuel-Bill-Generator\README.md