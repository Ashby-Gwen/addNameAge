async function addUser() {
    const name = document.getElementById('name').value;
    const age = document.getElementById('age').value;
    const response = await fetch('/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, age })
    });
    const result = await response.json();
    alert(result.message);
    fetchUsers();
}

async function fetchUsers() {
    const response = await fetch('/users');
    const users = await response.json();
    const userList = document.getElementById('userList');
    userList.innerHTML = '';
    users.forEach(user => {
        const li = document.createElement('li');
        li.textContent = `${user[1]} (Age: ${user[2]})`;
        userList.appendChild(li);
    });
}
fetchUsers();
