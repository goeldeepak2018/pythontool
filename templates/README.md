# Contact Form Automator (PythonTool)

## Project Kya Hai?
Yeh ek web-based automation tool hai jiska main maqsad CSV data ko read karke contact form fields ko automatically populate (fill) karna hai. Is tool mein 2 main sections hain:
1. **Dummy Data Generator:** 30 rows ka ek dummy CSV data (Name, Email, Mobile, Subject, Comment) generate karke download karne ki suvidha.
2. **Auto-Submitter:** Us CSV file ko upload karne ke baad, tool ek-ek karke data ko read karta hai aur live frontend preview mein form ko automatically fill karta hai.

*Future Scope: Iske baad isme ek aur module add hoga jo specifically mobile numbers ki processing ke liye kaam karega.*

## Technologies Used (Kiska Use Kiya Hai?)
* **Python:** Core programming language.
* **Flask:** Backend micro-framework routes aur API requests handle karne ke liye.
* **Pandas:** CSV files ko read, parse aur dictionary (JSON) mein convert karne ke liye.
* **Faker:** Realistic dummy data (Names, Emails, Phone numbers) generate karne ke liye.
* **HTML/CSS/Vanilla JavaScript:** 2-column frontend UI banane aur DOM manipulation (form auto-fill animation) ke liye.
* **Docker:** Production server par deploy karne ke liye environment consistency (bina local setup ke) ensure karne ke liye.