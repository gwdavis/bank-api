**ACCOUNTS**
----
  Returns json data about all accounts or optionally shows json data about a single account.  Alternatively on POST creates a new account for a given customer id with an initial deposit amount; creates transaction records and updates running account balance to reflect initial deposit

* **URL**

  `/accounts` or `/accounts/<account_number>`

* **Method:**

  `GET` | `POST` 
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   `account_number as integer`  

   example: /accounts/12345678

* **Data Params**

  `{
  "customer_id":3,
  "initial_deposit":1000
  }`

* **Success Response:**
  
  * **Code:** 201 CREATED <br />
    **Content:** `{
                  "account_id": 5,
                  "account_number": "48739779",
                  "active": true,
                  "balance": 1000,
                  "customer": "Gordon Baird",
                  "customer_id": 3,
                  "type": "dda"
                  }`

  OR
  
  * **Code:** 200 OK <br />
    **Content:** `{
                  "balance": 97000
                  }`

  OR
  
  * **Code:** 200 OK <br />
    **Content:** `{
  "accounts": [
    {
      "account_id": 1,
      "account_number": "12345678",
      "active": true,
      "balance": 97000,
      "customer": "treasury",
      "customer_id": 1,
      "type": "dda"
    },
    {
      "account_id": 2,
      "account_number": "48739278",
      "active": true,
      "balance": 1000,
      "customer": "Gary Davis",
      "customer_id": 2,
      "type": "dda"
    }]`

* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{
                  "reason": "No customer with id 55 found",
                  "status": "error"
                }`

  OR

  * **Code:** 404 BAD REQUEST <br />
    **Content:** `{
                  "reason": "initial_deposit must be a positive decimal number.",
                  "status": "error"
                }`

  OR

  * **Code:** 200 OK <br />
    **Content:** `{
                  "reason": "Missing mandatory parameter customer_id",
                  "status": "error"
                }`

  OR

  * **Code:** 200 OK <br />
    **Content:** `{
                  "reason": "Missing mandatory parameter customer_id",
                  "status": "error"
                }`

* **Sample Call:**



  `curl -X POST -H "Content-Type: application/json" -d '{"customer_id":3,
"initial_deposit":1000}' "http://localhost:5000/api/accounts"`

* **Notes:**

  None  

**CUSTOMERS**
----
  Returns json data about all customers or optionally shows json data about a single customer, or on POST creates a new customer for a given name and phone number.

* **URL**

  `/customers` or `/customers/<customer_id>`

* **Method:**

  `GET` | `POST` 
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   `customer_id as integer`  

   example: /customers/3

* **Data Params**

  `{
    "customer_name": "Gaynoll Davis",
    "mobile_number": "914-419-9789"
  }`  

* **Success Response:**  

* **Error Response:**

* **Sample Call:**  

  ```curl -X POST -H "Content-Type: application/json" -d '{
    "customer_name": "Gaynoll Davis",
    "mobile_number": "914-419-9789"
}' "http://localhost:5000/api/customers"```   

* **Notes:**

  None  

**TRANSACTIONS**
----
  Updates database with new a transaction record and adjusts running balance on accounts.  Returns JSON transaction id.

* **URL**

  `/transacttions`

* **Method:**

   `POST` 
  
*  **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

* **Data Params**

  `{
    "amount": "100",
    "reference": "Settlement of accounts",
    "originator": "48739278",
    "beneficiary": "48739777"
}`  

* **Success Response:**  

* **Error Response:**

* **Sample Call:**  

  ```curl -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -H "Postman-Token: 7402ff44-71f3-fc35-0b58-9e3b2516df96" -d '{
    "amount": "100",
    "reference": "Settlement of accounts",
    "originator": "48739278",
    "beneficiary": "48739777"
}' "http://bank-api-stage.herokuapp.com/api/transactions"```  

* **Notes:**

  None