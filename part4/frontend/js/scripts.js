/* 
This is a SAMPLE FILE to get you started.
Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    /* DO SOMETHING */
});

/* Place en dur (à changer) */

const places = [
    { name: "Beach House", price: 120, location: "Miami, FL", amenities: "Pool, Wi-Fi, Parking" },
    { name: "Mountain Cabin", price: 90, location: "Aspen, CO", amenities: "Fireplace, Hot Tub" },
    { name: "City Apartment", price: 75, location: "New York, NY", amenities: "Wi-Fi, Elevator" }
];

/*message submit login */
async function loginUser(email, password) {
    const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    if (response.ok) {
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = 'index.html';
    } else {
        alert('Login failed: ' + response.statusText);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }
});