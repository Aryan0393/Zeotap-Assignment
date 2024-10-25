# Rule Engine App

## Description
A simple rule engine application built with Flask that allows users to create and combine rules.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rule-engine-app.git

2. Navigate into the project directory:
    
   cd rule-engine-app

3. Create a virtual environment (optional):
   
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

4. Install dependencies:
   
   pip install -r requirements.txt

Usage

To create a rule, send a POST request to /create_rule:
 
  curl -X POST http://localhost:5000/create_rule -H "Content-Type: application/json" -d '{"rule_string": "your_rule_here"}'

To combine rules, send a POST request to /combine_rules:
 
 curl -X POST http://localhost:5000/combine_rules -H "Content-Type: application/json" -d '{"rules": ["rule1", "rule2"]}'

API Endpoints

POST /create_rule: Creates a new rule.
POST /combine_rules: Combines multiple rules into a single rule.


Testing

To run the tests, execute:

pytest


Contributing
Contributions are welcome! Please see the CONTRIBUTING.md file for details.

License
This project is licensed under the MIT License.

Contact
For questions, contact aryansikchi@gmail.com.


Just replace `Aryan0393` in the clone URL and `aryansikchi@gmail.com` with your actual GitHub username and email address.
