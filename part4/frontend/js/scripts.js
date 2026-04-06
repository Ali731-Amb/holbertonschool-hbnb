/* 
This is a SAMPLE FILE to get you started.
Please, follow the project instructions to complete the tasks.
*/

/* Place en dur (à changer) */

const places = [
    { name: "Beach House", price: 120, location: "Miami, FL", amenities: "Pool, Wi-Fi, Parking" },
    { name: "Mountain Cabin", price: 90, location: "Aspen, CO", amenities: "Fireplace, Hot Tub" },
    { name: "City Apartment", price: 75, location: "New York, NY", amenities: "Wi-Fi, Elevator" }
];


/*Récuprere les cookies + token */ 

function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (let c of cookies) {
        const [key, value] = c.split('=');
        if (key === name) return value;
    }
    return null;
}

/* ckeck user login */ 

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    if (!token) loginLink.style.display = 'block';
    else {
        loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

/*Fecth */
/*voir pour changer l'adresse + vérfier si bonne methode get */ 
async function fetchPlaces(token) {
    const response = await fetch('/places', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    if (response.ok) {
        const places = await response.json();
        displayPlaces(places);
    } else {
        console.error('Failed to fetch places', response.statusText);
    }
}

/* display place */ 

function displayPlaces(places) {
    const container = document.getElementById('places-list');
    container.innerHTML = ''; // vide la section
    places.forEach(place => {
        const card = document.createElement('article');
        card.classList.add('place-card');
        card.innerHTML = `
            <h2>${place.name}</h2>
            <p>Price: $${place.price}</p>
            <button class="details-button">View Details</button>
        `;
        container.appendChild(card);
    });
}

/* Price Filter */ 

function setupPriceFilter() {
    const filter = document.getElementById('price-filter');

    filter.addEventListener('change', (event) => {
        const maxPrice = event.target.value;
        const cards = document.querySelectorAll('.place-card');

        cards.forEach(card => {
            const priceText = card.querySelector('.price').textContent;
            const price = parseFloat(priceText.replace('Price: $', ''));

            if (maxPrice === 'All' || price <= maxPrice) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

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

    /* Login */ 
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            await loginUser(email, password);
        });
    }

    /*Vérification auth + affichage places (index.html)*/
    const placesContainer = document.getElementById('places-list');
    if (placesContainer) {
        checkAuthentication(); // va appeler fetchPlaces si token
    }

    /*Setup filtre */
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        setupPriceFilter();
    }
});

