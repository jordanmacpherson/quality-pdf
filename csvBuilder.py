import fitz
import re
import csv

def find_acronyms_with_pages(pdf_path, pattern):
    """
    Extracts text from a PDF and finds all unique acronyms and the pages they appear on.
    """
    try:
        document = fitz.open(pdf_path)
        acronym_pages = {}
        
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text = page.get_text()
            
            # Find all matches on the page
            matches = re.findall(pattern, text)
            
            # Store the page number for each unique acronym
            for acronym in set(matches):
                if acronym not in acronym_pages:
                    acronym_pages[acronym] = []
                acronym_pages[acronym].append(page_num + 1)
        
        document.close()
        return acronym_pages
    except FileNotFoundError:
        print("Error: File not found.")
        return None

def write_to_csv(data, filename="acronym_results.csv"):
    """
    Writes the acronym data to a CSV file.
    """
    if not data:
        print("No data to write to CSV.")
        return
        
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header row
        writer.writerow(['Unique Acronym', 'Pages Found On'])
        
        # Write data rows
        for acronym, pages in sorted(data.items()):
            writer.writerow([acronym] + pages)

# Example usage: Find all unique acronyms and save to CSV
pdf_file = "whirlpool.pdf"
acronym_pattern = r'\b[A-Z&_./\\]{2,6}\b'

acronym_data = find_acronyms_with_pages(pdf_file, acronym_pattern)
if acronym_data:
    write_to_csv(acronym_data)
    print("Results have been saved to 'acronym_results.csv'")