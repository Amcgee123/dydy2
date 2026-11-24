
// Get saved demo accounts from the current browser session

function getAccounts() {
    return JSON.parse(sessionStorage.getItem("accounts") || "[]");
}

// Save demo accounts

function saveAccounts(accounts) {
    sessionStorage.setItem("accounts", JSON.stringify(accounts));
}

// Create a salted password hash using PBKDF2

async function hashPassword(password, salt) {

    const encoder = new TextEncoder();

    const key = await crypto.subtle.importKey(
        "raw",
        encoder.encode(password),
        "PBKDF2",
        false,
        ["deriveBits"]
    );

    const result = await crypto.subtle.deriveBits(
        {
            name: "PBKDF2",
            salt: salt,
            iterations: 100000,
            hash: "SHA-256"
        },
        key,
        256
    );

    return Array.from(new Uint8Array(result))
        .map(byte => byte.toString(16).padStart(2, "0"))
        .join("");
}

// Signup page functionality

const signupForm = document.getElementById("signupForm");

if (signupForm) {

    signupForm.addEventListener("submit", async function(event) {

        event.preventDefault();

        const username = document.getElementById("username").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;
        const message = document.getElementById("message");

        if (username.length < 3) {
            message.textContent = "Username must be at least 3 characters.";
            return;
        }

        if (password.length < 6) {
            message.textContent = "Password must be at least 6 characters.";
            return;
        }

        if (password !== confirmPassword) {
            message.textContent = "Passwords do not match!";
            return;
        }

        const accounts = getAccounts();

        const existingUser = accounts.find(account =>
            account.username.toLowerCase() === username.toLowerCase()
        );

        if (existingUser) {
            message.textContent = "Username already exists!";
            return;
        }

        const salt = crypto.getRandomValues(new Uint8Array(16));

        const hashedPassword = await hashPassword(password, salt);

        const saltString = Array.from(salt)
            .map(byte => byte.toString(16).padStart(2, "0"))
            .join("");

        accounts.push({
            username: username,
            email: email,
            passwordHash: hashedPassword,
            salt: saltString
        });

        saveAccounts(accounts);

        message.textContent = "Account created successfully!";

        setTimeout(function() {
            window.location.href = "login.html";
        }, 1500);

    });

}

// Login page functionality

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", async function(event) {

        event.preventDefault();

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value;
        const message = document.getElementById("message");

        const accounts = getAccounts();

        const account = accounts.find(account =>
            account.username.toLowerCase() === username.toLowerCase()
        );

        if (!account) {
            message.textContent = "Username or password is incorrect.";
            return;
        }

        const salt = new Uint8Array(
            account.salt.match(/.{2}/g).map(byte => parseInt(byte, 16))
        );

        const hashedPassword = await hashPassword(password, salt);

        if (hashedPassword !== account.passwordHash) {
            message.textContent = "Username or password is incorrect.";
            return;
        }

        sessionStorage.setItem("loggedInUser", account.username);

        message.textContent = "Login successful! Welcome " + account.username + "!";

    });

}
