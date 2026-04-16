/* admin.js uses API_URL and helpers from scripts.js */


/**
 * Checks if the user is an admin by parsing the JWT token.
 * Redirects to index.html if not authorized.
 */
function checkAdminAccess() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'login.html';
        return null;
    }

    const payload = parseJwt(token);
    if (!payload || !payload.is_admin) {
        alert('Access denied: Admin privileges required.');
        window.location.href = 'index.html';
        return null;
    }

    return token;
}

/**
 * Fetches and displays the list of users.
 */
async function fetchUsers(token) {
    try {
        const response = await fetch(`${API_URL}/users/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error('Failed to fetch users');

        const users = await response.json();
        const list = document.getElementById('users-list');
        list.innerHTML = '';

        users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><code>${user.id.substring(0, 8)}...</code></td>
                <td>${user.first_name} ${user.last_name}</td>
                <td>${user.email}</td>
                <td><span class="amenity-tag" style="margin: 0; padding: 2px 8px;">${user.is_admin ? 'Admin' : 'User'}</span></td>
                <td class="admin-actions-cell">
                    <button class="details-button" style="margin: 0; padding: 4px 12px; font-size: 0.7rem;" onclick="alert('User details/edit coming soon!')">Edit</button>
                </td>
            `;
            list.appendChild(row);
        });
    } catch (error) {
        document.getElementById('users-list').innerHTML = `<tr><td colspan="5">Error: ${error.message}</td></tr>`;
    }
}

/**
 * Fetches and displays the list of places.
 */
async function fetchPlaces(token) {
    try {
        const response = await fetch(`${API_URL}/places/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error('Failed to fetch places');

        const places = await response.json();
        const list = document.getElementById('admin-places-list');
        list.innerHTML = '';

        places.forEach(place => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><a href="place.html?id=${place.id}" style="color: var(--primary-purple); font-weight: 600; text-decoration: none;">${place.title}</a></td>
                <td>$${place.price}</td>
                <td>${place.owner_name || 'N/A'}</td>
                <td class="admin-actions-cell">
                    <a href="place.html?id=${place.id}" class="details-button" style="margin: 0; padding: 4px 12px; font-size: 0.7rem;">View</a>
                </td>
            `;
            list.appendChild(row);
        });
    } catch (error) {
        document.getElementById('admin-places-list').innerHTML = `<tr><td colspan="4">Error: ${error.message}</td></tr>`;
    }
}

/**
 * Fetches and displays the list of amenities.
 */
async function fetchAmenities(token) {
    try {
        const response = await fetch(`${API_URL}/amenities/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error('Failed to fetch amenities');

        const amenities = await response.json();
        const list = document.getElementById('amenities-list');
        list.innerHTML = '';

        amenities.forEach(amenity => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${amenity.id}</td>
                <td>${amenity.name}</td>
                <td>
                    <button class="btn-delete" onclick="deleteAmenity('${amenity.id}')">Delete</button>
                </td>
            `;
            list.appendChild(row);
        });
    } catch (error) {
        document.getElementById('amenities-list').innerHTML = `<tr><td colspan="3">Error: ${error.message}</td></tr>`;
    }
}

/**
 * Deletes an amenity by ID.
 */
async function deleteAmenity(amenityId) {
    if (!confirm('Are you sure you want to delete this amenity?')) return;

    const token = getCookie('token');
    try {
        const response = await fetch(`${API_URL}/amenities/${amenityId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            alert('Amenity deleted successfully');
            fetchAmenities(token);
        } else {
            const data = await response.json();
            alert('Error: ' + (data.error || 'Failed to delete amenity'));
        }
    } catch (error) {
        alert('Connection error');
    }
}

/**
 * Handles the creation of a new amenity.
 */
async function setupAmenityForm(token) {
    const form = document.getElementById('create-amenity-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('amenity-name').value.trim();
        const description = document.getElementById('amenity-description').value.trim();

        try {
            const response = await fetch(`${API_URL}/amenities/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ name, description })
            });

            if (response.ok) {
                alert('Amenity created successfully');
                form.reset();
                fetchAmenities(token);
            } else {
                const data = await response.json();
                alert('Error: ' + (data.error || 'Failed to create amenity'));
            }
        } catch (error) {
            alert('Connection error');
        }
    });
}

// Logout is handled by the global function in scripts.js

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    const token = checkAdminAccess();
    if (token) {
        fetchUsers(token);
        fetchPlaces(token);
        fetchAmenities(token);
        setupAmenityForm(token);
    }
});
