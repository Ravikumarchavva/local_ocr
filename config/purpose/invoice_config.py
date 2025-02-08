invoice_schema = {
    "type": "object",
    "properties": {
        "invoice_number": {"type": "string", "nullable": True},
        "invoice_date": {"type": "string", "format": "date", "nullable": True},
        "supplier_name": {"type": "string", "nullable": True},
        "customer_name": {"type": "string", "nullable": True},
        "total_net_amount": {"type": "string", "nullable": True},
        "total_vat_amount": {"type": "string", "nullable": True},
        "total_invoice_amount": {"type": "string", "nullable": True},
        "line_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "product_code": {"type": "string", "nullable": True},
                    "description": {"type": "string", "nullable": True},
                    "quantity": {"type": "string", "nullable": True},
                    "price_per_unit": {"type": "string", "nullable": True},
                    "vat_percent": {"type": "string", "nullable": True},
                    "net_price": {"type": "string", "nullable": True}
                }
            }
        },
        "due_date": {"type": "string", "format": "date", "nullable": True},
        "payment_date": {"type": "string", "format": "date", "nullable": True},
        "currency": {"type": "string", "nullable": True},
        "payment_details": {
            "type": "object",
            "properties": {
                "iban": {"type": "string", "nullable": True},
                "swift": {"type": "string", "nullable": True},
                "account_number": {"type": "string", "nullable": True}
            }
        },
    }
}


def get_prompt(text):
    prompt = f"""
    You are an **invoice extractor**. Your task is to extract structured invoice details from the provided text and output a **valid JSON format** as per the following schema:

    ### **General Information:**
    - "invoice_number": (string) Unique identifier of the invoice. If missing, set to `null`.
    - "invoice_date": (string) Date of issue in `YYYY-MM-DD` format. If missing, set to `null`.
    - "supplier_name": (string) Name of the supplier. If missing, set to `null`.
    - "customer_name": (string) Name of the customer. If missing, set to `null`.

    ### **Financial Information:**
    - "total_net_amount": (float) Amount before VAT. If missing, set to `null`.
    - "total_vat_amount": (float) VAT amount applied. If missing, set to `null`.
    - "total_invoice_amount": (float) Final total including VAT. If missing, set to `null`.

    ### **Line Items (if present):**
    Each line item should include:
    - "product_code": (string) Code or ID of the product/service. If missing, set to `null`.
    - "description": (string) Description of the item. If missing, set to `null`.
    - "quantity": (int) Number of units. If missing, set to `null`.
    - "price_per_unit": (float) Cost per unit. If missing, set to `null`.
    - "vat_percent": (float) VAT rate applied. If missing, set to `null`.
    - "net_price": (float) Total for the particular line item. If missing, set to `null`.

    ### **Payment Information (if available):**
    - "iban": (string) IBAN (International Bank Account Number). If missing, set to `null`.
    - "swift": (string) SWIFT/BIC code. If missing, set to `null`.
    - "account_number": (string) Bank account number. If missing, set to `null`.
    - "payment_date": (string) Date of payment. If missing, set to `null`.

    ### **Strict Output Rules:**
    - **If any value is missing, set it to `null`. Do not infer missing details or hallucinate.**
    - **Return only the fields listed above. Do not include any additional information or guess values.**
    - **Strictly adhere to the data types specified (e.g., integer for quantities, float for prices).**
    - **Preserve exact structure and key names.**
    
    ### **Invoice Text:**
    {text}
    """
    return prompt
