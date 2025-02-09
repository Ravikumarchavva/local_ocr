MAX_MODEL_TOKENS = 2056  # new constant for maximum model tokens

def get_qc_prompt(text):
    """
    Constructs a QC extraction prompt by appending the provided page text.
    Returns a string ready for LLM processing.
    """
    report_prompt = (
        "You are an expert quality control data extraction specialist. Your task is to extract structured quality control details from the provided text, which represents a page from a QC report. "
        "The report originates from a fresh produce distribution center and is used for internal quality control purposes.\n"
        "You must return a **valid JSON object** that strictly follows this schema. **Do not return extra text, explanations, or comments.**\n\n"
        "### **Schema:**\n"
        "{\n"
        "  \"product_name\": \"string\", // The name of the product (e.g., 'Strawberries', 'Organic Blueberries') along with quantity (eg: 20x227g Punnet, 20x320g Punnet).\n"
        "  \"RAG\": \"string\", // A color code indicating quality status (e.g., 'RED', 'GREEN', 'BLUE', 'AMBER'). If not explicitly a color, use null.\n"
        "  \"expected_qty\": \"string\", // The expected quantity of the product.\n"
        "  \"received_qty\": \"string\", // The quantity of the product actually received.\n"
        "  \"supplier_code\": \"string\", // The code identifying the supplier.\n"
        "  \"supplier\": \"string\", // The name of the supplier.\n"
        "  \"coo\": \"string\", // Country of Origin.\n"
        "  \"received_date\": \"YYYY-MM-DD HH:MM:SS\", // The date and time the product was received. If time is unavailable, use 00:00:00.\n"
        "  \"inspection_date\": \"YYYY-MM-DD HH:MM:SS\", // The date and time of the inspection. If time is unavailable, use 00:00:00.\n"
        "  \"print_date\": \"YYYY-MM-DD\", // The date the report was printed.\n"
        "  \"iss_pallet_id\": \"integer\", // The internal pallet ID. If not a valid integer, use null.\n"
        "  \"supplier_pallet_id\": \"integer\", // The supplier's pallet ID. If not a valid integer, use null.\n"
        "  \"customer_pallet_id\": \"integer\", // The customer's pallet ID. If not a valid integer, use null.\n"
        "  \"variety\": \"string\", // The variety of the product (e.g., 'Chandler', 'Duke').\n"
        "  \"brand\": \"string\", // The brand of the product.\n"
        "  \"organic\": \"YES\" or \"NO\", // Indicates whether the product is organic.\n"
        "  \"does_pallet_meet_spec\": \"YES\" or \"NO\", // Indicates whether the pallet meets specifications.\n"
        "  \"end_customer\": \"string\", // The final customer for the product.\n"
        "  \"harvest_date\": \"YYYY-MM-DD\", // The date the product was harvested.\n"
        "  \"dp\": \"integer\", // Distribution Point.\n"
        "  \"total_defects_percentage\": \"float\", // The total number of defects found. If not a valid integer, use null.\n"
        "  \"size_calibre\": \"string\", // The size or calibre of the product (e.g., '35/40').\n"
        "  \"lot_number\": \"integer\", // The lot number of the product.\n"
        "  \"inspector\": \"string\", // The name of the inspector.\n"
        "  \"estimated_yield_percentage\": \"float\", // The estimated yield of the product.\n"
        "  \"defects_fruit_total\": \"integer\", // The total number of defective fruits. If not a valid integer, use null.\n"
        "  \"packs_with_defects\": \"integer\", // The number of packs with defects. If not a valid integer, use null.\n"
        "  \"waste_tot\": \"integer\", // The total waste. If not a valid integer, use null.\n"
        "  \"waste_fruit_total\": \"integer\", // The total waste fruit. If not a valid integer, use null.\n"
        "  \"packs_with_waste\": \"integer\", // The number of packs with waste. If not a valid integer, use null.\n"
        "  \"minor_defects_tot\": \"integer\", // The total number of minor defects. If not a valid integer, use null.\n"
        "  \"minor_fruit_total\": \"integer\", // The total number of minor defective fruits. If not a valid integer, use null.\n"
        "  \"major_defects_tot\": \"integer\", // The total number of major defects. If not a valid integer, use null.\n"
        "  \"major_fruit_total\": \"integer\", // The total number of major defective fruits. If not a valid integer, use null.\n"
        "  \"packs_with_major\": \"integer\", // The number of packs with major defects. If not a valid integer, use null.\n"
        "  \"box_pack_weights\": \"string\", // Weights of the boxes/packs.\n"
        "  \"under_weight_percentage\": \"float\", // Percentage of under weight.\n"
        "  \"weight_readings\": \"string\", // Weight readings.\n"
        "  \"fruit_weights\": \"string\", // Weights of the fruits.\n"
        "  \"under_size_percentage\": \"float\", // Percentage of under size.\n"
        "  \"qa_comments\": \"string\", // Quality assurance comments.\n"
        "  \"packs_fruits_inspected_sample_size\": \"integer\", // The sample size of packs/fruits inspected. If not a valid integer, use null.\n"
        "  \"boxes_inspected\": \"integer\" // The number of boxes inspected. If not a valid integer, use null.\n"
        "}\n\n"
        "### **Strict Extraction Rules:**\n"
        "- RAG will be the color eg: RED, GREEN, BLUE, AMBER etc... look a color from the text. If no color is found, use null.\n"
        "- Some fields would be empty if you find large space followed with a `anyname :` then keep null.\n"
        "- Extract values **exactly as they appear** in the text.\n"
        "- If a field is **missing**, return it as **null**.\n"
        "- Do **not** infer or add extra information.\n"
        "- Remove unnecessary spaces from extracted values.\n"
        "- Output must be **pure JSON** with **no explanations, notes, or formatting errors**.\n"
        "- Return exactly **one** JSON object. Do not produce multiple.\n"
        "- If a date field only contains the year, month, and day, set the time to 00:00:00.\n"
        "- If a numerical field contains non-numeric characters, remove them before converting to an integer. If the field cannot be converted to an integer, return null.\n"
        "- If there are multiple possible values for a field, choose the one that appears most relevant in the context of the document.\n\n"
        "### **Page Text:**\n"
    )

    full_prompt = f"{report_prompt}{text}"

    # # Truncate the prompt if it exceeds the maximum token limit
    # if len(full_prompt) > MAX_MODEL_TOKENS:
    #     truncated_text = text[:MAX_MODEL_TOKENS - len(report_prompt) - 10]  # Leave some buffer
    #     full_prompt = f"{report_prompt}{truncated_text}"

    return full_prompt
