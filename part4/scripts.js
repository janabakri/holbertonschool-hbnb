// ========== scripts.js ==========
// pages: login, index, place, add_review

// ===== login page (login.html) =====
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorDiv = document.getElementById('error-message');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch(`${API_URL}/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (response.ok) {
                    setCookie('token', data.access_token);
                    window.location.href = 'index.html';
                } else {
                    const msg = data.error || data.msg || 'Login failed';
                    if (errorDiv) errorDiv.textContent = msg;
                    else alert(msg);
                }
            } catch (error) {
                const msg = 'Connection error. Make sure the backend is running on port 5000.';
                if (errorDiv) errorDiv.textContent = msg;
                else alert(msg);
                console.error(error);
            }
        });
    }
});

// ===== Homepage (index.html) - Show Places =====
const placesList = document.getElementById('places-list');
if (placesList) {
// Verify authentication and update login/logout link
    const loginLink = document.getElementById('login-link');
    if (loginLink) {
        if (isAuthenticated()) {
            loginLink.textContent = 'Logout';
            loginLink.href = '#';
            loginLink.addEventListener('click', (e) => {
                e.preventDefault();
                logout();
            });
        } else {
            loginLink.textContent = 'Login';
            loginLink.href = 'login.html';
        }
    }

// display places
    fetchPlaces();

// Price filter
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', filterPlacesByPrice);
    }
}

async function fetchPlaces() {
    const container = document.getElementById('places-list');
    if (!container) return;

    try {
        const token = getToken();
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

        const response = await fetch(`${API_URL}/places`, { headers });

        if (!response.ok) {
            if (response.status === 401) window.location.href = 'login.html';
            throw new Error('Failed to fetch places');
        }

        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        console.error(error);
        container.innerHTML = '<p class="error">Error loading places. Make sure the server is running.</p>';
    }
}

function displayPlaces(places) {
    const container = document.getElementById('places-list');
    if (!container) return;
    container.innerHTML = '';

    if (!places || places.length === 0) {
        container.innerHTML = '<p>No places available.</p>';
        return;
    }

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.setAttribute('data-price', place.price);
        card.innerHTML = `
            <h3>${escapeHtml(place.title || place.name)}</h3>
            <p class="price">$${place.price} / night</p>
            <button class="details-button" data-id="${place.id}">View Details</button>
        `;

        const button = card.querySelector('.details-button');
        button.addEventListener('click', () => {
            window.location.href = `place.html?id=${place.id}`;
        });

        container.appendChild(card);
    });
}

function filterPlacesByPrice() {
    const maxPrice = document.getElementById('price-filter').value;
    const cards = document.querySelectorAll('.place-card');

    cards.forEach(card => {
        const price = parseFloat(card.getAttribute('data-price'));
        if (maxPrice === 'all' || price <= parseFloat(maxPrice)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// ===== Place Details Page (place.html) =====
const placeId = new URLSearchParams(window.location.search).get('id');
if (placeId && document.getElementById('place-details')) {
    loadPlaceDetails(placeId);

    // إظهار/إخفاء قسم إضافة التقييم
    const addReviewSection = document.getElementById('add-review-section');
    if (addReviewSection) {
        if (isAuthenticated()) {
            addReviewSection.style.display = 'block';
            const placeIdField = document.getElementById('place-id');
            if (placeIdField) placeIdField.value = placeId;
        } else {
            addReviewSection.style.display = 'none';
        }
    }
}

async function loadPlaceDetails(placeId) {
    try {
        const response = await fetch(`${API_URL}/places/${placeId}`);
        if (!response.ok) throw new Error('Place not found');

        const place = await response.json();
        displayPlaceDetails(place);
        await loadReviews(placeId);
    } catch (error) {
        console.error(error);
        const container = document.getElementById('place-details');
        if (container) {
            container.innerHTML = '<p class="error">Error loading place details.</p>';
        }
    }
}

function displayPlaceDetails(place) {
    const container = document.getElementById('place-details');
    if (!container) return;

    const amenitiesList = place.amenities && place.amenities.length > 0
        ? place.amenities.map(a => typeof a === 'object' ? escapeHtml(a.name) : escapeHtml(a)).join(', ')
        : 'None';

    container.innerHTML = `
        <div class="card place-details-card">
            <h2>${escapeHtml(place.title || place.name)}</h2>
            <p class="description">${escapeHtml(place.description || 'No description available.')}</p>
            <p class="price"><strong>Price:</strong> $${place.price} / night</p>
            <p class="host"><strong>Host:</strong> ${escapeHtml(place.owner?.first_name || place.host_name || 'Owner')}</p>
            <p class="amenities"><strong>Amenities:</strong> ${amenitiesList}</p>
        </div>
    `;
}

async function loadReviews(placeId) {
    try {
        const response = await fetch(`${API_URL}/reviews/places/${placeId}/reviews`);
        const reviews = await response.json();
        displayReviews(reviews);
    } catch (error) {
        console.error(error);
        const container = document.getElementById('reviews-list');
        if (container) container.innerHTML = '<p>Unable to load reviews.</p>';
    }
}

function displayReviews(reviews) {
    const container = document.getElementById('reviews-list');
    if (!container) return;

    if (!reviews || reviews.length === 0) {
        container.innerHTML = '<p>No reviews yet. Be the first to review!</p>';
        return;
    }

    container.innerHTML = reviews.map(review => `
        <div class="review-card">
            <p class="review-text">"${escapeHtml(review.text || review.comment)}"</p>
            <p class="review-rating">${getStarRating(review.rating)}</p>
            <p class="review-author">- ${escapeHtml(review.user?.first_name || 'User')}</p>
        </div>
    `).join('');
}

// ===== Add a review (add_review.html or form in place.html) =====
const reviewForm = document.getElementById('review-form');
if (reviewForm) {
// If you are at add_review.html and it is not logged in, return to the main page
    if (window.location.pathname.includes('add_review.html') && !isAuthenticated()) {
        window.location.href = 'index.html';
    }

    reviewForm.addEventListener('submit', submitReview);
}

async function submitReview(e) {
    e.preventDefault();

    const token = getToken();
    if (!token) {
        alert('You must be logged in to submit a review.');
        window.location.href = 'login.html';
        return;
    }

    let placeId = document.getElementById('place-id')?.value;
    if (!placeId) {
        placeId = new URLSearchParams(window.location.search).get('id');
    }

    const reviewText = document.getElementById('review-text')?.value;
    const rating = parseInt(document.getElementById('rating')?.value || document.getElementById('review-rating')?.value);

    if (!reviewText || !rating) {
        alert('Please fill in all fields.');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                place_id: placeId,
                text: reviewText,
                rating: rating
            })
        });

        if (response.ok) {
            alert('Review submitted successfully!');

            if (document.getElementById('review-text')) document.getElementById('review-text').value = '';
            if (document.getElementById('rating')) document.getElementById('rating').value = '5';

        // Either reload the ratings or guide
            if (document.getElementById('reviews-list')) {
                await loadReviews(placeId);
            } else {
                window.location.href = `place.html?id=${placeId}`;
            }
        } else {
            const error = await response.json();
            alert(`Failed: ${error.error || error.msg || 'Error occurred'}`);
        }
    } catch (error) {
        console.error(error);
        alert('Connection error.');
    }
}
