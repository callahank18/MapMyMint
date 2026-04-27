
const BASE_URL = "http://127.0.0.1:8000";

async function loginUser() {
    const username = document.getElementById("name").value;
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
            localStorage.setItem('loggedIn', 'true');
            window.location.href = "index.html";
        }
        else {
            console.error(data.detail || "Login failed");
        }

    } catch (error) {
        console.error("Login error:", error);
    }
}

async function registerUser() {
    const username = document.getElementById("name").value;
    const password = document.getElementById("password").value;
    const confirm = document.getElementById("confirm-password").value;

    if (password !== confirm) {
        console.error("Passwords do not match");
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
            window.location.href = "login.html";
        } else {
            console.error(data.detail || "Registration failed");
        }

    } catch (error) {
        console.error("Register error:", error);
    }
}

function getCurrentUserId() {
    return localStorage.getItem("currentUserId");
}
});
