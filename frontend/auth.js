
const BASE_URL = "http://127.0.0.1:8000";

async function loginUser() {
    const username = document.getElementById("email").value;
    const password = document.getElementById("password").value;

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

            alert("Login successful!");
            localStorage.setItem('loggedIn', 'true');
            window.location.href = "index.html";
        }
        else {
            alert(data.detail || "Login failed");
        }

    } catch (error) {
        console.error("Login error:", error);
        alert("Server error during login");
    }
}

async function registerUser() {
    const username = document.getElementById("name").value;
    const password = document.getElementById("password").value;
    const confirm = document.getElementById("confirm-password").value;

    if (password !== confirm) {
        alert("Passwords do not match");
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/register`, {
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
            alert("Account created successfully!");
            window.location.href = "login.html";
        } else {
            alert(data.detail || "Login failed");
        }

    } catch (error) {
        console.error("Register error:", error);
        alert("Server error during registration");
    }
}

function getCurrentUserId() {
    return localStorage.getItem("currentUserId");
}

function requireLogin() {
    const user = getCurrentUserId();
    if (!user) {
        alert("Please log in first");
        window.location.href = "login.html";
        return false;
    }
    return true;
}

function logout() {
    localStorage.removeItem("currentUserId");
    alert("Logged out");
    window.location.href = "login.html";
}
window.addEventListener("load", () => {
    const page = window.location.pathname.split("/").pop();

    if (page === "index.html") {
        requireLogin();
    }
});