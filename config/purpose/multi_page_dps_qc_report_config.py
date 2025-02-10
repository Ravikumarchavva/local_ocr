def get_qc_prompt(texts):
    """
    Constructs a QC extraction prompt for multiple pages, supporting multiple items.
    Each page may contain multiple products, and the output must be a list of JSON objects.
    """
    report_prompt = (
        "You are an expert quality control data extraction specialist. Your task is to extract structured quality control details from the provided text, which represents multiple pages from a QC report. "
        "Each page may contain details for multiple products. The report originates from a fresh produce distribution center and is used for internal quality control purposes.\n\n"
        "You must return a **valid JSON array** where each product is a separate JSON object. **Do not return extra text, explanations, or comments.**\n\n"
        "### **Schema:**\n"
        "[\n"
        "  {\n"
        "    \"product_name\": \"string\", // The name of the product (e.g., 'Strawberries', 'Organic Blueberries') along with quantity (eg: 20x227g Punnet, 20x320g Punnet).\n"
        "    \"RAG\": \"string\", // A color code indicating quality status (e.g., 'RED', 'GREEN', 'BLUE', 'AMBER'). If not explicitly a color, use null.\n"
        "    \"expected_qty\": \"string\", // The expected quantity of the product.\n"
        "    \"received_qty\": \"string\", // The quantity of the product actually received.\n"
        "    \"supplier_code\": \"string\", // The code identifying the supplier.\n"
        "    \"supplier\": \"string\", // The name of the supplier.\n"
        "    \"coo\": \"string\", // Country of Origin.\n"
        "    \"received_date\": \"YYYY-MM-DD HH:MM:SS\", // The date and time the product was received. If time is unavailable, use 00:00:00.\n"
        "    \"inspection_date\": \"YYYY-MM-DD HH:MM:SS\", // The date and time of the inspection. If time is unavailable, use 00:00:00.\n"
        "    \"print_date\": \"YYYY-MM-DD\", // The date the report was printed.\n"
        "    \"iss_pallet_id\": \"integer\", // The internal pallet ID. If not a valid integer, use null.\n"
        "    \"supplier_pallet_id\": \"integer\", // The supplier's pallet ID. If not a valid integer, use null.\n"
        "    \"customer_pallet_id\": \"integer\", // The customer's pallet ID. If not a valid integer, use null.\n"
        "    \"variety\": \"string\", // The variety of the product (e.g., 'Chandler', 'Duke').\n"
        "    \"brand\": \"string\", // The brand of the product.\n"
        "    \"organic\": \"YES\" or \"NO\", // Indicates whether the product is organic.\n"
        "    \"does_pallet_meet_spec\": \"YES\" or \"NO\", // Indicates whether the pallet meets specifications.\n"
        "    \"end_customer\": \"string\", // The final customer for the product.\n"
        "    \"harvest_date\": \"YYYY-MM-DD\", // The date the product was harvested.\n"
        "    \"dp\": \"integer\", // Distribution Point.\n"
        "    \"total_defects_percentage\": \"float\", // The total number of defects found. If not a valid integer, use null.\n"
        "    \"size_calibre\": \"string\", // The size or calibre of the product (e.g., '35/40').\n"
        "    \"lot_number\": \"integer\", // The lot number of the product.\n"
        "    \"inspector\": \"string\", // The name of the inspector.\n"
        "    \"estimated_yield_percentage\": \"float\", // The estimated yield of the product.\n"
        "    \"defects_fruit_total\": \"integer\", // The total number of defective fruits. If not a valid integer, use null.\n"
        "  }\n"
        "]\n\n"
        "### **Strict Extraction Rules:**\n"
        "- Each extracted JSON object must represent a single product.\n"
        "- Extract all products from the provided text, ensuring no duplicate or missing items.\n"
        "- Maintain the correct data types for each field.\n"
        "- If a field is missing, return it as null.\n"
        "- The output must be **pure JSON** with **no explanations, notes, or formatting errors**.\n"
        "- Return exactly **one JSON array** containing **multiple JSON objects**.\n"
        "- If a date field contains only the year, month, and day, set the time to 00:00:00.\n"
        "- If a numerical field contains non-numeric characters, remove them before converting to an integer. If the field cannot be converted to an integer, return null.\n\n"
        "### **Page Texts:**\n"
    )
    
    full_prompt = f"{report_prompt}{texts}"
    
    return full_prompt
