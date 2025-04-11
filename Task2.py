import csv
import os
from datetime import datetime
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        # Logo - only try to add if file exists
        if os.path.exists('logo.png'):
            self.image('logo.png', 10, 8, 25)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Sales Data Analysis Report', 0, 0, 'C')
        # Line break
        self.ln(20)
    
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def read_data(filename):
    """Read data from CSV file"""
    data = []
    try:
        with open(filename, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        print("Please make sure the file exists in the same directory as the script.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")
        return None

def analyze_data(data):
    """Perform basic analysis on the data"""
    if not data:
        return None
        
    analysis = {}
    
    # Basic statistics
    total_sales = sum(float(item['Amount']) for item in data)
    average_sale = total_sales / len(data)
    regions = set(item['Region'] for item in data)
    products = set(item['Product'] for item in data)
    
    # Sales by region
    sales_by_region = {}
    for region in regions:
        sales_by_region[region] = sum(float(item['Amount']) for item in data if item['Region'] == region)
    
    # Sales by product
    sales_by_product = {}
    for product in products:
        sales_by_product[product] = sum(float(item['Amount']) for item in data if item['Product'] == product)
    
    analysis['total_sales'] = total_sales
    analysis['average_sale'] = average_sale
    analysis['sales_by_region'] = sales_by_region
    analysis['sales_by_product'] = sales_by_product
    analysis['record_count'] = len(data)
    
    return analysis

def generate_report(data, analysis, output_filename):
    """Generate PDF report"""
    if not data or not analysis:
        print("Cannot generate report without valid data and analysis.")
        return False
    
    pdf = PDFReport()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    # Report metadata
    pdf.cell(0, 10, f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
    pdf.ln(10)
    
    # Summary statistics
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Summary Statistics', 0, 1)
    pdf.set_font('Arial', '', 12)
    
    pdf.cell(0, 10, f"Total records analyzed: {analysis['record_count']}", 0, 1)
    pdf.cell(0, 10, f"Total sales: ${analysis['total_sales']:,.2f}", 0, 1)
    pdf.cell(0, 10, f"Average sale amount: ${analysis['average_sale']:,.2f}", 0, 1)
    pdf.ln(10)
    
    # Sales by region
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Sales by Region', 0, 1)
    pdf.set_font('Arial', '', 12)
    
    for region, sales in analysis['sales_by_region'].items():
        pdf.cell(0, 10, f"{region}: ${sales:,.2f}", 0, 1)
    pdf.ln(10)
    
    # Sales by product
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Sales by Product', 0, 1)
    pdf.set_font('Arial', '', 12)
    
    for product, sales in analysis['sales_by_product'].items():
        pdf.cell(0, 10, f"{product}: ${sales:,.2f}", 0, 1)
    pdf.ln(10)
    
    # Sample data table
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Sample Data (First 10 Records)', 0, 1)
    pdf.set_font('Arial', 'B', 10)
    
    # Table header
    pdf.cell(40, 10, 'Date', 1)
    pdf.cell(40, 10, 'Region', 1)
    pdf.cell(40, 10, 'Product', 1)
    pdf.cell(40, 10, 'Amount', 1)
    pdf.ln()
    
    # Table rows
    pdf.set_font('Arial', '', 10)
    for row in data[:10]:
        pdf.cell(40, 10, row['Date'], 1)
        pdf.cell(40, 10, row['Region'], 1)
        pdf.cell(40, 10, row['Product'], 1)
        pdf.cell(40, 10, f"${float(row['Amount']):,.2f}", 1)
        pdf.ln()
    
    # Save the PDF
    pdf.output(output_filename)
    return True

def main():
    # Configuration
    input_file = 'sales_data.csv'
    output_file = 'sales_report.pdf'
    
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, input_file)
    
    # Process data
    print("Reading data...")
    data = read_data(input_path)
    
    if not data:
        return
    
    print("Analyzing data...")
    analysis = analyze_data(data)
    
    if not analysis:
        print("Error in data analysis.")
        return
    
    print("Generating report...")
    if generate_report(data, analysis, output_file):
        print(f"Report generated successfully: {output_file}")
    else:
        print("Failed to generate report.")

if __name__ == "__main__":
    main()