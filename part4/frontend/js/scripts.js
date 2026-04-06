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
    const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
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
    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
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

    /* ===================== LOGIN ===================== */
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    /* ===================== INDEX - PLACES ===================== */
    const placesContainer = document.getElementById('places-list');
    if (placesContainer) {
        checkAuthentication(); // appelle fetchPlaces si token
    }

    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        setupPriceFilter();
    }

    /* ===================== ADD REVIEW ===================== */
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        const token = checkAuthentication(); // redirige si pas auth
        const placeId = getPlaceIdFromURL();

        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById('review-text').value;
            if (!reviewText.trim()) {
                alert("Le texte de la review ne peut pas être vide !");
                return;
            }
            await submitReview(token, placeId, reviewText);
        });
    }

    /* ===================== FONCTIONS ===================== */

    // Récupère cookie
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    // Vérifie auth et affiche login
    function checkAuthentication() {
        const token = getCookie('token');
        const loginLink = document.getElementById('login-link');
        if (!token) {
            if (loginLink) loginLink.style.display = 'block';
        } else {
            if (loginLink) loginLink.style.display = 'none';
        }
        return token;
    }

    // LOGIN
    async function loginUser(email, password) {
        try {
            const response = await fetch('/api/v1/auth/login', {
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
        } catch (err) {
            console.error('Login error:', err);
        }
    }

    // FETCH PLACES
    async function fetchPlaces(token) {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
                }
            });
            if (response.ok) {
                const places = await response.json();
                displayPlaces(places);
            } else {
                alert('Erreur lors de la récupération des places : ' + response.statusText);
            }
        } catch (err) {
            console.error('Fetch error:', err);
        }
    }

    // DISPLAY PLACES
    function displayPlaces(places) {
        if (!placesContainer) return;
        placesContainer.innerHTML = '';
        places.forEach(place => {
            const placeCard = document.createElement('article');
            placeCard.className = 'place-card';
            placeCard.innerHTML = `
                <h2>${place.name}</h2>
                <p>Prix par nuit : $${place.price}</p>
                <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">Voir les détails</button>
            `;
            placesContainer.appendChild(placeCard);
        });
    }

    // SETUP PRICE FILTER
    function setupPriceFilter() {
        const options = [10, 50, 100, 'All'];
        priceFilter.innerHTML = '';
        options.forEach(o => {
            const opt = document.createElement('option');
            opt.value = o;
            opt.textContent = o;
            priceFilter.appendChild(opt);
        });
        priceFilter.addEventListener('change', (event) => {
            const maxPrice = event.target.value;
            const placeCards = document.querySelectorAll('.place-card');
            placeCards.forEach(card => {
                const price = parseFloat(card.querySelector('p').textContent.replace(/\D/g, ''));
                card.style.display = (maxPrice === 'All' || price <= maxPrice) ? 'block' : 'none';
            });
        });
    }

    // Récupère l'ID place depuis URL
    function getPlaceIdFromURL() {
        const params = new URLSearchParams(window.location.search);
        return params.get('id');
    }

    // POST REVIEW
    async function submitReview(token, placeId, reviewText) {
        try {
            const response = await fetch('/api/v1/reviews', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ place_id: placeId, text: reviewText })
            });
            await handleResponse(response);
        } catch (err) {
            alert("Erreur réseau : " + err.message);
        }
    }

    // HANDLE RESPONSE
    async function handleResponse(response) {
        if (response.ok) {
            alert('Review soumise avec succès !');
            const reviewInput = document.getElementById('review-text');
            if (reviewInput) reviewInput.value = '';
        } else {
            const errorData = await response.json().catch(() => ({}));
            alert('Erreur lors de la soumission : ' + (errorData.message || response.statusText));
        }
    }

});
