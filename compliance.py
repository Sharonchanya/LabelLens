def screen_compliance(
    net_quantity,
    mrp,
    manufacturer,
    date_information
):

    screening_results = []

    # Check Net Quantity
    if net_quantity:
        screening_results.append({
            "field": "Net Quantity",
            "value": net_quantity,
            "status": "Detected"
        })
    else:
        screening_results.append({
            "field": "Net Quantity",
            "value": "Not detected",
            "status": "Review Required"
        })

    # Check MRP
    if mrp:
        screening_results.append({
            "field": "MRP",
            "value": mrp,
            "status": "Detected"
        })
    else:
        screening_results.append({
            "field": "MRP",
            "value": "Not detected",
            "status": "Review Required"
        })

    # Check Manufacturer Details
    if manufacturer:
        screening_results.append({
            "field": "Manufacturer Details",
            "value": manufacturer,
            "status": "Detected"
        })
    else:
        screening_results.append({
            "field": "Manufacturer Details",
            "value": "Not detected",
            "status": "Review Required"
        })

    # Check Date Information
    if date_information:
        screening_results.append({
            "field": "Date Information",
            "value": date_information,
            "status": "Detected"
        })
    else:
        screening_results.append({
            "field": "Date Information",
            "value": "Not detected",
            "status": "Review Required"
        })

    return screening_results