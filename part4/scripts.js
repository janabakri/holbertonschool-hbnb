// ===== Configuration =====
const API_URL = 'http://localhost:5000/api/v1';

// ===== Cookie Helper =====
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value}; path=/; expires=${expires.toUTCString()}`;
}

function deleteCookie(name) {
    document.cookie = `${name}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;`;
}

// ===== Authentication Check =====
function isAuthenticated() {
    return !!getCookie('token');
}

function checkAuthAndRedirect() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// ===== LOGIN PAGE =====
document.addEventListener('DOMContentLoaded', () => {
    // Login form handling
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const res = await fetch(`${API_URL}/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                if (res.ok) {
                    const data = await res.json();
                    setCookie('token', data.access_token);
                    window.location.href = 'index.html';
                } else {
                    const error = await res.json();
                    document.getElementById('error-message').textContent = 
                        error.error || 'Login failed. Check your credentials.';
                }
            } catch (err) {
                document.getElementById('error-message').textContent = 'Network error. Is the server running?';
            }
        });
    }

    // ===== INDEX PAGE (Places List) =====
    const placesList = document.getElementById('places-list');
    if (placesList) {
        // Show/hide login link based on authentication
        const loginLink = document.getElementById('login-link');
        if (loginLink) {
            if (isAuthenticated()) {
                loginLink.style.display = 'none';
            } else {
                loginLink.style.display = 'block';
            }
        }
        
        fetchPlaces();
        
        // Price filter
        const priceFilter = document.getElementById('price-filter');
        if (priceFilter) {
            priceFilter.addEventListener('change', filterPlacesByPrice);
        }
    }

    // ===== PLACE DETAILS PAGE =====
    const placeId = new URLSearchParams(window.location.search).get('id');
    if (placeId && document.getElementById('place-details')) {
        loadPlaceDetails(placeId);
        
        // Show/hide add review section based on authentication
        const addReviewSection = document.getElementById('add-review-section');
        if (addReviewSection) {
            if (isAuthenticated()) {
                addReviewSection.style.display = 'block';
                // Set place_id in hidden field for review form
                const placeIdField = document.getElementById('place-id');
                if (placeIdField) placeIdField.value = placeId;
            } else {
                addReviewSection.style.display = 'none';
            }
        }
    }

    // ===== ADD REVIEW FORM =====
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        // Redirect if not authenticated
        if (!isAuthenticated()) {
            window.location.href = 'index.html';
            return;
        }
        reviewForm.addEventListener('submit', submitReview);
    }
});

// ===== PLACES FUNCTIONS =====
async function fetchPlaces() {
    try {
        const token = getCookie('token');
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const res = await fetch(`${API_URL}/places`, { headers });
        if (!res.ok) throw new Error('Failed to fetch places');
        
        const places = await res.json();
        displayPlaces(places);
    } catch (err) {
        console.error(err);
        document.getElementById('places-list').innerHTML = '<p>Error loading places. Make sure the API server is running.</p>';
    }
}

function displayPlaces(places) {
    const container = document.getElementById('places-list');
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
            <h3>${escapeHtml(place.title)}</h3>
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

// ===== PRICE FILTER =====
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

// ===== PLACE DETAILS FUNCTIONS =====
async function loadPlaceDetails(placeId) {
    try {
        const res = await fetch(`${API_URL}/places/${placeId}`);
        if (!res.ok) throw new Error('Place not found');
        
        const place = await res.json();
        displayPlaceDetails(place);
        
        // Load reviews separately
        await loadReviews(placeId);
    } catch (err) {
        console.error(err);
        document.getElementById('place-details').innerHTML = '<p>Error loading place details.</p>';
    }
}

function displayPlaceDetails(place) {
    const container = document.getElementById('place-details');
    container.innerHTML = `
        <h2>${escapeHtml(place.title)}</h2>
        <p class="description">${escapeHtml(place.description || 'No description available.')}</p>
        <p class="price"><strong>Price:</strong> $${place.price} / night</p>
        <p class="location"><strong>Location:</strong> ${place.latitude}, ${place.longitude}</p>
        <div class="owner-info">
            <strong>Host:</strong> ${escapeHtml(place.owner?.first_name || 'Unknown')} ${escapeHtml(place.owner?.last_name || '')}
        </div>
        <div class="amenities">
            <strong>Amenities:</strong>
            <ul>
                ${place.amenities?.map(a => `<li>${escapeHtml(a.name)}</li>`).join('') || '<li>No amenities listed</li>'}
            </ul>
        </div>
    `;
}

async function loadReviews(placeId) {
    try {
        const res = await fetch(`${API_URL}/reviews/places/${placeId}/reviews`);
        if (!res.ok) throw new Error('Failed to load reviews');
        
        const reviews = await res.json();
        displayReviews(reviews);
    } catch (err) {
        console.error(err);
        document.getElementById('reviews-list').innerHTML = '<p>Unable to load reviews.</p>';
    }
}

function displayReviews(reviews) {
    const container = document.getElementById('reviews-list');
    
    if (!reviews || reviews.length === 0) {
        container.innerHTML = '<p>No reviews yet. Be the first to review!</p>';
        return;
    }
    
    container.innerHTML = '';
    reviews.forEach(review => {
        const card = document.createElement('div');
        card.className = 'review-card';
        card.innerHTML = `
            <p class="review-text">"${escapeHtml(review.text)}"</p>
            <p class="review-rating">⭐ ${review.rating}/5</p>
            <p class="review-author">- ${escapeHtml(review.user?.first_name || 'Anonymous')}</p>
        `;
        container.appendChild(card);
    });
}

// ===== REVIEW SUBMISSION =====
async function submitReview(e) {
    e.preventDefault();
    
    const token = getCookie('token');
    if (!token) {
        alert('You must be logged in to submit a review.');
        window.location.href = 'login.html';
        return;
    }
    
    const placeId = document.getElementById('place-id')?.value || 
                    new URLSearchParams(window.location.search).get('id');
    const reviewText = document.getElementById('review-text').value;
    const rating = parseInt(document.getElementById('rating').value);
    
    if (!reviewText || !rating) {
        alert('Please fill in all fields.');
        return;
    }
    
    try {
        const res = await fetch(`${API_URL}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: rating,
                place_id: placeId
            })
        });
        
        if (res.ok) {
            alert('Review submitted successfully!');
            document.getElementById('review-form').reset();
            // Reload reviews to show the new one
            await loadReviews(placeId);
        } else {
            const error = await res.json();
            alert(`Failed to submit review: ${error.error || 'Unknown error'}`);
        }
    } catch (err) {
        console.error(err);
        alert('Network error. Could not submit review.');
    }
}

// ===== HELPER FUNCTIONS =====
function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}
