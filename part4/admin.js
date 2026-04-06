// ===== Admin Dashboard JavaScript =====

const API_URL = 'http://localhost:5000/api/v1';

// ===== Cookie Helper =====
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// ===== Check if user is Admin =====
async function checkAdmin() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'login.html';
        return false;
    }
    
    try {
        // Decode JWT to check is_admin claim
        const payload = JSON.parse(atob(token.split('.')[1]));
        if (!payload.is_admin) {
            alert('Access denied. Admin privileges required.');
            window.location.href = 'index.html';
            return false;
        }
        return true;
    } catch (err) {
        console.error(err);
        window.location.href = 'login.html';
        return false;
    }
}

// ===== Load Dashboard Data =====
async function loadDashboard() {
    const token = getCookie('token');
    
    try {
        // Fetch all users
        const usersRes = await fetch(`${API_URL}/users/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const users = await usersRes.json();
        displayUsers(users);
        
        // Fetch all places
        const placesRes = await fetch(`${API_URL}/places/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const places = await placesRes.json();
        displayPlaces(places);
        
        // Fetch all amenities
        const amenitiesRes = await fetch(`${API_URL}/amenities/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const amenities = await amenitiesRes.json();
        displayAmenities(amenities);
        
    } catch (err) {
        console.error(err);
        document.getElementById('dashboard-content').innerHTML = 
            '<p class="error">Error loading dashboard data. Make sure the server is running.</p>';
    }
}

// ===== Display Users Table =====
function displayUsers(users) {
    const container = document.getElementById('users-list');
    if (!container) return;
    
    if (!users || users.length === 0) {
        container.innerHTML = '<tr><td colspan="5">No users found</td></tr>';
        return;
    }
    
    container.innerHTML = users.map(user => `
        <tr>
            <td>${escapeHtml(user.id.substring(0, 8))}...</td>
            <td>${escapeHtml(user.first_name)} ${escapeHtml(user.last_name)}</td>
            <td>${escapeHtml(user.email)}</td>
            <td>${user.is_admin ? '✅ Admin' : '👤 User'}</td>
            <td>
                <button class="btn-edit" onclick="editUser('${user.id}')">Edit</button>
                <button class="btn-delete" onclick="deleteUser('${user.id}')">Delete</button>
            </td>
        </tr>
    `).join('');
}

// ===== Display Places Table =====
function displayPlaces(places) {
    const container = document.getElementById('admin-places-list');
    if (!container) return;
    
    if (!places || places.length === 0) {
        container.innerHTML = '<tr><td colspan="5">No places found</td></tr>';
        return;
    }
    
    container.innerHTML = places.map(place => `
        <tr>
            <td>${escapeHtml(place.title)}</td>
            <td>$${place.price}</td>
            <td>${escapeHtml(place.owner?.first_name || 'Unknown')}</td>
            <td>
                <button class="btn-delete" onclick="deletePlace('${place.id}')">Delete</button>
            </td>
        </tr>
    `).join('');
}

// ===== Display Amenities =====
function displayAmenities(amenities) {
    const container = document.getElementById('amenities-list');
    if (!container) return;
    
    if (!amenities || amenities.length === 0) {
        container.innerHTML = '<tr><td colspan="3">No amenities found</td></tr>';
        return;
    }
    
    container.innerHTML = amenities.map(amenity => `
        <tr>
            <td>${escapeHtml(amenity.id.substring(0, 8))}...</td>
            <td>${escapeHtml(amenity.name)}</td>
            <td>
                <button class="btn-edit" onclick="editAmenity('${amenity.id}')">Edit</button>
                <button class="btn-delete" onclick="deleteAmenity('${amenity.id}')">Delete</button>
            </td>
        </tr>
    `).join('');
}

// ===== Admin Actions =====
async function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user? This will also delete all their places and reviews.')) {
        return;
    }
    
    const token = getCookie('token');
    try {
        const res = await fetch(`${API_URL}/users/${userId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (res.ok) {
            alert('User deleted successfully');
            loadDashboard();
        } else {
            const error = await res.json();
            alert(`Failed to delete user: ${error.error}`);
        }
    } catch (err) {
        console.error(err);
        alert('Network error');
    }
}

async function deletePlace(placeId) {
    if (!confirm('Are you sure you want to delete this place?')) return;
    
    const token = getCookie('token');
    try {
        const res = await fetch(`${API_URL}/places/${placeId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (res.ok) {
            alert('Place deleted successfully');
            loadDashboard();
        } else {
            const error = await res.json();
            alert(`Failed to delete place: ${error.error}`);
        }
    } catch (err) {
        console.error(err);
        alert('Network error');
    }
}

async function deleteAmenity(amenityId) {
    if (!confirm('Are you sure you want to delete this amenity?')) return;
    
    const token = getCookie('token');
    try {
        const res = await fetch(`${API_URL}/amenities/${amenityId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (res.ok) {
            alert('Amenity deleted successfully');
            loadDashboard();
        } else {
            const error = await res.json();
            alert(`Failed to delete amenity: ${error.error}`);
        }
    } catch (err) {
        console.error(err);
        alert('Network error');
    }
}

// ===== Create Amenity Form =====
document.addEventListener('DOMContentLoaded', () => {
    const createForm = document.getElementById('create-amenity-form');
    if (createForm) {
        createForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const token = getCookie('token');
            const name = document.getElementById('amenity-name').value;
            const description = document.getElementById('amenity-description').value;
            
            try {
                const res = await fetch(`${API_URL}/amenities/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ name, description })
                });
                
                if (res.ok) {
                    alert('Amenity created successfully');
                    createForm.reset();
                    loadDashboard();
                } else {
                    const error = await res.json();
                    alert(`Failed to create amenity: ${error.error}`);
                }
            } catch (err) {
                console.error(err);
                alert('Network error');
            }
        });
    }
});

// ===== Edit Functions (Modal) =====
function editUser(userId) {
    // You can implement a modal for editing user
    alert(`Edit user ${userId} - Feature to be implemented`);
}

function editAmenity(amenityId) {
    // You can implement a modal for editing amenity
    alert(`Edit amenity ${amenityId} - Feature to be implemented`);
}

// ===== Helper Functions =====
function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// ===== Initialize Admin Page =====
document.addEventListener('DOMContentLoaded', async () => {
    const isAdmin = await checkAdmin();
    if (isAdmin) {
        loadDashboard();
    }
});
