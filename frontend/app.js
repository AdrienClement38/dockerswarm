const API_URL = 'http://localhost:5000/api';

async function loadItems() {
    try {
        const response = await fetch(`${API_URL}/items`);
        const data = await response.json();
        const itemsDiv = document.getElementById('items');
        itemsDiv.innerHTML = `<p><em>Source: ${data.source}</em></p>`;

        if (data.items.length === 0) {
            itemsDiv.innerHTML += '<p>No items yet.</p>';
        } else {
            data.items.forEach(item => {
                itemsDiv.innerHTML += `
                    <div class="item">
                        <h3>${item.name}</h3>
                        <p>${item.description}</p>
                    </div>
                `;
            });
        }
    } catch (error) {
        document.getElementById('items').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
}

async function addItem() {
    const name = document.getElementById('itemName').value;
    const description = document.getElementById('itemDescription').value;

    if (!name) {
        alert('Name is required');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/items`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, description })
        });

        if (response.ok) {
            document.getElementById('itemName').value = '';
            document.getElementById('itemDescription').value = '';
            loadItems();
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Load items on page load
window.onload = loadItems;
