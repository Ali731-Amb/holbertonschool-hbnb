/* 
HBNB Part 4 - scripts.js
*/

/* =============================================
   UTILITAIRES (utilisés par toutes les tasks)
   ============================================= */

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

/* =============================================
   TASK 3 - Vérification authentification
   - Affiche/cache le lien #login-link
   - redirect=true : redirige vers index si pas de token (task 5)
   ============================================= */
function checkAuthentication(redirect = false) {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
        if (redirect) window.location.href = 'index.html';
        return null;
    } else {
        if (loginLink) loginLink.style.display = 'none';
        return token;
    }
}

/* =============================================
   TASK 2 - LOGIN
   ============================================= */
async function loginUser(email, password) {
    try {
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
            const errorEl = document.getElementById('login-error');
            if (errorEl) {
                errorEl.classList.add('visible');
            } else {
                alert('Login failed: ' + response.statusText);
            }
        }
    } catch (err) {
        console.error('Login error:', err);
    }
}

/* =============================================
   TASK 3 - FETCH & AFFICHAGE DES PLACES
   ============================================= */
async function fetchPlaces(token) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
            method: 'GET',
            headers
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            console.error('Erreur fetch places:', response.statusText);
        }
    } catch (err) {
        console.error('Fetch error:', err);
    }
}

function displayPlaces(places) {
    const container = document.getElementById('places-list');
    if (!container) return;
    container.innerHTML = '';

    places.forEach(place => {
        const card = document.createElement('article');
        card.className = 'place-card';
        card.dataset.price = place.price;

        card.innerHTML = `
            <h2>${place.title}</h2>
            <p>Price per night: $${place.price}</p>
            <button class="details-button"
                onclick="window.location.href='place.html?id=${place.id}'">
                View Details
            </button>
        `;
        container.appendChild(card);
    });
}

// TASK 3 : filtre price
function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;

    priceFilter.innerHTML = '';
    ['10', '50', '100', 'All'].forEach(val => {
        const opt = document.createElement('option');
        opt.value = val;
        opt.textContent = val;
        if (val === 'All') opt.selected = true;
        priceFilter.appendChild(opt);
    });

    priceFilter.addEventListener('change', (event) => {
        const maxPrice = event.target.value;
        const cards = document.querySelectorAll('.place-card');
        cards.forEach(card => {
            const price = parseFloat(card.dataset.price);
            if (maxPrice === 'All' || price <= parseFloat(maxPrice)) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

/* =============================================
   TASK 4 - PLACE DETAILS
   ============================================= */
async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`/api/v1/places/${placeId}`, {
            method: 'GET',
            headers
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            const det = document.getElementById('place-details');
            if (det) det.innerHTML = '<p>Place not found.</p>';
        }
    } catch (err) {
        console.error('Fetch place details error:', err);
    }
}

function displayPlaceDetails(place) {
    const titleEl = document.getElementById('place-title');
    if (titleEl) titleEl.textContent = place.title;

    const detailsSection = document.getElementById('place-details');
    if (detailsSection) {
        const amenities = Array.isArray(place.amenities)
            ? place.amenities.map(a => a.name || a).join(', ')
            : (place.amenities || 'N/A');

        const ownerName = place.owner
            ? `${place.owner.first_name} ${place.owner.last_name}`
            : 'N/A';

        detailsSection.innerHTML = `
            <div class="place-details">
                <div class="place-info">
                    <p><strong>Host:</strong> ${ownerName}</p>
                    <p><strong>Price per night:</strong> $${place.price}</p>
                    <p><strong>Description:</strong> ${place.description || 'No description.'}</p>
                    <p><strong>Amenities:</strong> ${amenities}</p>
                </div>
            </div>
        `;
    }

    const reviewsSection = document.getElementById('reviews');
    if (reviewsSection) {
        const reviews = place.reviews || [];

        if (reviews.length === 0) {
            reviewsSection.innerHTML = '<h2>Reviews</h2><p>No reviews yet.</p>';
        } else {
            const reviewsHTML = reviews.map(r => {
                const stars = '★'.repeat(r.rating) + '☆'.repeat(5 - r.rating);
                const userName = r.user
                    ? `${r.user.first_name} ${r.user.last_name}`
                    : 'Anonymous';
                return `
                    <div class="review-card">
                        <p class="reviewer-name">${userName}:</p>
                        <p>${r.text}</p>
                        <p>${stars}</p>
                    </div>
                `;
            }).join('');
            reviewsSection.innerHTML = `<h2>Reviews</h2>${reviewsHTML}`;
        }
    }
}

/* =============================================
   TASK 5 - SUBMIT REVIEW
   ============================================= */
async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                place_id: placeId,
                text: reviewText,
                rating: parseInt(rating)
            })
        });

        if (response.ok) {
            alert('Review submitted successfully!');
            const textarea = document.getElementById('review-text');
            const select = document.getElementById('rating');
            if (textarea) textarea.value = '';
            if (select) select.value = '1';
        } else {
            const errorData = await response.json().catch(() => ({}));
            alert('Failed to submit review: ' + (errorData.message || response.statusText));
        }
    } catch (err) {
        alert('Network error: ' + err.message);
    }
}

/* =============================================
   INIT - DOMContentLoaded
   Point d'entrée unique, détecte la page active
   ============================================= */
document.addEventListener('DOMContentLoaded', () => {

    /* ---- PAGE LOGIN (login.html) ---- */
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    /* ---- PAGE INDEX (index.html) ---- */
    const placesContainer = document.getElementById('places-list');
    if (placesContainer) {
        const token = checkAuthentication();
        setupPriceFilter();
        fetchPlaces(token);
    }

    /* ---- PAGE PLACE DETAILS ---- */
    const placeDetailsSection = document.getElementById('place-details');
    const placeTitleEl = document.getElementById('place-title');
    if (placeDetailsSection && placeTitleEl !== null) {
        const token = checkAuthentication();
        const placeId = getPlaceIdFromURL();

        if (!placeId) {
            placeDetailsSection.innerHTML = '<p>No place ID in URL.</p>';
            return;
        }

        const addReviewSection = document.getElementById('add-review');
        if (addReviewSection) {
            addReviewSection.style.display = token ? 'block' : 'none';
        }

        fetchPlaceDetails(token, placeId);

        const reviewFormPlace = document.getElementById('review-form');
        if (reviewFormPlace && token) {
            reviewFormPlace.addEventListener('submit', async (event) => {
                event.preventDefault();
                const reviewText = document.getElementById('review-text').value;
                const rating = document.getElementById('rating').value;
                await submitReview(token, placeId, reviewText, rating);
            });
        }
    }

    const reviewPageTitle = document.getElementById('review-page-title');
    if (reviewPageTitle) {
        // TASK 5 : redirige si non connecté
        const token = checkAuthentication(true);
        const placeId = getPlaceIdFromURL();

        if (placeId && token) {
            fetch(`/api/v1/places/${placeId}`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(r => r.json())
            .then(place => {
                reviewPageTitle.textContent = `Reviewing: ${place.title}`;
            })
            .catch(() => {
                reviewPageTitle.textContent = 'Add a Review';
            });
        }

        const reviewForm = document.getElementById('review-form');
        if (reviewForm) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const reviewText = document.getElementById('review-text').value;
                const rating = document.getElementById('rating').value;

                if (!reviewText.trim()) {
                    alert('Review text cannot be empty!');
                    return;
                }

                await submitReview(token, placeId, reviewText, rating);
            });
        }
    }

});
