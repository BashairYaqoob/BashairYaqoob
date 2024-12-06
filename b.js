// Bank Account Class
class BankAccount {
    constructor(title, accountNumber, iban, balance) {
        this.accountTitle = title;
        this.accountNumber = accountNumber;
        this.ibanNumber = iban;
        this.accountBalance = balance;
        this.products = []; // List of products (Debit Cards or Retail Loans)
    }

    // Add a product to the account
    addProduct(product) {
        if (product.type === "DebitCard" || product.type === "RetailLoan") {
            this.products.push(product);
            if (product.type === "RetailLoan") {
                this.accountBalance += product.loanAmount; // Add loan amount to balance
            }
        } else {
            console.log("Invalid product type.");
        }
    }

    // Display account details
    displayAccountDetails() {
        console.log(`Account Title: ${this.accountTitle}`);
        console.log(`Account Number: ${this.accountNumber}`);
        console.log(`IBAN Number: ${this.ibanNumber}`);
        console.log(`Account Balance: ${this.accountBalance}`);
        console.log("Products:");
        this.products.forEach((product, index) => {
            console.log(`  ${index + 1}. ${product.getDetails()}`);
        });
    }
}

// Debit Card Class
class DebitCard {
    constructor(category, validTill, cardNumber, cvv) {
        this.type = "DebitCard";
        this.category = category;
        this.validTill = validTill;
        this.cardNumber = cardNumber;
        this.cvv = cvv;
    }

    // Get details of the debit card
    getDetails() {
        return `Debit Card [Category: ${this.category}, Valid Till: ${this.validTill}, Card Number: ${this.cardNumber}, CVV: ${this.cvv}]`;
    }
}

// Retail Loan Class
class RetailLoan {
    constructor(creditScore, loanAmount) {
        this.type = "RetailLoan";
        this.creditScore = creditScore;
        this.loanAmount = loanAmount;
    }

    // Get details of the retail loan
    getDetails() {
        return `Retail Loan [Credit Score: ${this.creditScore}, Loan Amount: ${this.loanAmount}]`;
    }
}

// Example Usage

// Create a new bank account
const account1 = new BankAccount("John Doe", "1234567890", "PK123456789012345678", 5000);

// Create a debit card and add to the account
const debitCard = new DebitCard("Gold", "12/28", 1234567890123456, 123);
account1.addProduct(debitCard);

// Create a retail loan and add to the account
const retailLoan = new RetailLoan(750, 10000);
account1.addProduct(retailLoan);

// Display account details
account1.displayAccountDetails();
