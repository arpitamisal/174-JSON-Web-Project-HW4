#!/usr/bin/python3

import cgi
import cgitb
import json
import os
import html

cgitb.enable()

134
print("Content-Type: text/html")
print()

form = cgi.FieldStorage()
filename = form.getvalue("file")

if not filename:
    print("Error: Missing file name.")
    raise SystemExit

if "/" in filename or ".." in filename:
    print("Error: Invalid file name.")
    raise SystemExit

file_path = os.path.join("/var/www/html", filename)

if not os.path.exists(file_path):
    print("Error: File does not exist.")
    raise SystemExit

try:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        raise SystemExit

    if "Mainline" not in data or "Table" not in data["Mainline"]:
        print("Error: JSON structure is invalid or missing required fields.")
        raise SystemExit

    table = data["Mainline"]["Table"]

    if "Header" not in table or "Data" not in table["Header"] or not isinstance(table["Header"]["Data"], list):
        print("Error: Table header data is missing or invalid.")
        raise SystemExit

    if "Row" not in table or not isinstance(table["Row"], list):
        print("Error: Table row data is missing or invalid.")
        raise SystemExit

    if len(table["Row"]) == 0:
        print("Error: No trucking companies found in the JSON file.")
        raise SystemExit

    headers = table["Header"]["Data"]
    rows = table["Row"]

    html_output = """
    <html>
    <head>
      <title>Top Trucking Companies</title>
      <style>
        body {
          font-family: "Times New Roman", serif;
          margin: 20px;
          background-color: white;
          color: black;
        }
        h2 {
          text-align: center;
        }
        table {
          width: 100%;
          border-collapse: collapse;
        }
        table, th, td {
          border: 1px solid black;
        }
        th, td {
          padding: 10px;
        }
        th {
          text-align: center;
        }
        .leftMiddle {
          text-align: left;
          vertical-align: middle;
        }
        .leftTop {
          text-align: left;
          vertical-align: top;
        }
        .centerMiddle {
          text-align: center;
          vertical-align: middle;
        }
        img {
          max-width: 140px;
          max-height: 100px;
          display: block;
          margin: 0 auto;
        }
      </style>
    </head>
    <body>
      <h2>Top Trucking Companies</h2>
      <table>
        <tr>
    """

    for header in headers:
        html_output += f"<th>{html.escape(str(header))}</th>"

    html_output += "</tr>"

    for company in rows:
        hub_html = ""

        if "Hubs" in company and isinstance(company["Hubs"], dict) and "Hub" in company["Hubs"] and isinstance(company["Hubs"]["Hub"], list):
            hub_html = "<ul>"
            for i, hub in enumerate(company["Hubs"]["Hub"]):
                if i == 0:
                    hub_html += f"<li><b>{html.escape(str(hub))}</b></li>"
                else:
                    hub_html += f"<li>{html.escape(str(hub))}</li>"
            hub_html += "</ul>"

        home_page_html = "N/A"
        homepage = company.get("HomePage", "")
        if isinstance(homepage, str) and (homepage.startswith("http://") or homepage.startswith("https://")):
            safe_url = html.escape(homepage, quote=True)
            home_page_html = f'<a href="{safe_url}" target="_blank">{safe_url}</a>'
	
        logo_html = "No Logo Available"
        logo = company.get("Logo", "")
        company_name = html.escape(str(company.get("Company", "Company")))

        if logo:
            safe_logo = html.escape(str(logo), quote=True)
            logo_html = f'''
            <div style="width:150px; height:100px; display:flex; align-items:center; justify-content:center;">
              <img src="/{safe_logo}" style="max-width:100%; max-height:100%;">
            </div>
            '''

        html_output += f"""
        <tr>
          <td class="leftMiddle">{html.escape(str(company.get("Company", "")))}</td>
          <td class="leftMiddle">{html.escape(str(company.get("Services", "")))}</td>
          <td class="leftTop">{hub_html}</td>
          <td class="leftMiddle">{html.escape(str(company.get("Revenue", "")))}</td>
          <td class="leftMiddle">{home_page_html}</td>
          <td class="centerMiddle">{logo_html}</td>
        </tr>
        """

    html_output += """
      </table>
    </body>
    </html>
    """

    print(html_output)

except Exception as e:
    print(f"Error: {html.escape(str(e))}")
