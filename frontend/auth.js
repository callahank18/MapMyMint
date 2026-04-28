
const BASE_URL = "http://127.0.0.1:8000";

async function loginUser() {
    const username = document.getElementById("name").value;
    const password = document.getElementById("password").value;

    if (!username || !password) {
        alert("Please enter both username and password.");
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/login/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("currentUserId", data.user_id);
            localStorage.setItem("currentUsername", data.username);
            localStorage.setItem('loggedIn', 'true');
            window.location.href = "index.html";
        }
        else {
            console.error(data.detail || "Login failed");
            // Show the user why it failed (e.g., "bad_password")
            alert("Login Failed: " + (data.detail || "Invalid credentials"));
        }

    } catch (error) {
        console.error("Login error:", error);
        alert("Could not connect to the server. Is the backend running?");
    }
}

async function registerUser() {
    const username = document.getElementById("name").value;
    const password = document.getElementById("password").value;
    const confirm = document.getElementById("confirm-password").value;

    if (password !== confirm) {
        console.error("Passwords do not match");
        alert("Passwords do not match!");
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/register/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert("Registration successful! Please log in.");
            window.location.href = "login.html";
        } else {
            console.error(data.detail || "Registration failed");
        }

    } catch (error) {
        console.error("Register error:", error);
    }
}

function logoutUser() {
    localStorage.removeItem("currentUserId");
    localStorage.removeItem("currentUsername");
    localStorage.removeItem("loggedIn");
    window.location.href = "home.html";
}

function getCurrentUserId() {
    return localStorage.getItem("currentUserId");
};
