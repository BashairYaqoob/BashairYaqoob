// Bank Account Class
class BankAccount {
    constructor(title, accountNumber, iban, balance) {
        this.accountTitle = title;
        this.accountNumber = accountNumber;
        this.ibanNumber = iban;
        this.accountBalance = balance;
        this.products = []; // List of products
    }

    // Add a product to the account
    addProduct(product) {
        this.products.push(product);
        if (product.type === "RetailLoan") {
            this.accountBalance += product.loanAmount; // Add loan amount to balance
        }
    }

    // Display account details
    displayAccountDetails() {
        console.log(`Account Title: ${this.accountTitle}`);
        console.log(`Account Number: ${this.accountNumber}`);
        console.log(`IBAN Number: ${this.ibanNumber}`);
        console.log(`Account Balance: ${this.accountBalance}`);
        console.log("Products:", this.products.map((p) => p.getDetails()));
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

    getDetails() {
        return `Retail Loan [Credit Score: ${this.creditScore}, Loan Amount: ${this.loanAmount}]`;
    }
}

// Task 1: Create a list of bank accounts
const accounts = [
    new BankAccount("Fatima Javed", "123456789012", "PK123123456789123456", 5000),
    new BankAccount("Hassan Anjum", "223456789012", "PK121123456789123456", 3000),
    new BankAccount("Hassan Raza", "323456789012", "PK112123456789123467", 4000),
];

// Add existing products to accounts
accounts[0].addProduct(new DebitCard("Platinum", "11/29", 123456788, 123));
accounts[1].addProduct(new RetailLoan(500, 2000));
accounts[2].addProduct(new DebitCard("Gold", "09/28", 123456789, 456));
accounts[2].addProduct(new RetailLoan(500, 2000));

// Task 2: Add a loan for account 223456789012 if eligible
function processLoan(accountNumber, creditScore, requestedLoan) {
    const account = accounts.find((acc) => acc.accountNumber === accountNumber);
    if (!account) {
        console.log("Account not found.");
        return;
    }

    if (creditScore >= 50 && creditScore <= 100 && requestedLoan <= 3000) {
        const loan = new RetailLoan(creditScore, requestedLoan);
        account.addProduct(loan);
        console.log(`Loan approved for ${account.accountTitle}.`);
    } else {
        console.log("Loan not approved due to eligibility criteria.");
    }
}

// Process loan for Hassan Anjum
processLoan("223456789012", 70, 1000);

// Task 3: Add a new product to an account
function addNewProduct(accountNumber, productDetails) {
    const account = accounts.find((acc) => acc.accountNumber === accountNumber);
    if (!account) {
        console.log("Account not found.");
        return;
    }

    console.log(`Account Title: ${account.accountTitle}`);

    if (productDetails.type === "DebitCard") {
        const debitCard = new DebitCard(
            productDetails.category,
            productDetails.validTill,
            productDetails.cardNumber,
            productDetails.cvv
        );
        account.addProduct(debitCard);
    } else if (productDetails.type === "RetailLoan") {
        const retailLoan = new RetailLoan(productDetails.creditScore, productDetails.loanAmount);
        account.addProduct(retailLoan);
    } else {
        console.log("Invalid product details.");
    }
}

// Add a new debit card to Fatima Javed's account
addNewProduct("123456789012", {
    type: "DebitCard",
    category: "Gold",
    validTill: "12/30",
    cardNumber: 987654321,
    cvv: 789,
});

// Display account details for all accounts
accounts.forEach((account) => account.displayAccountDetails());

