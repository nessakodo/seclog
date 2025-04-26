async function loadEvents() {
    const response = await fetch('detected_events.json');
    const events = await response.json();
    const eventsDiv = document.getElementById('events');
    eventsDiv.innerHTML = '';

    events.forEach(event => {
        const div = document.createElement('div');
        div.className = 'event';
        div.innerHTML = `<strong>File:</strong> ${event.filepath}<br><strong>Time:</strong> ${event.timestamp}<br><strong>Content:</strong> ${event.content}`;
        eventsDiv.appendChild(div);
    });
}


// Load on page load
window.onload = loadEvents;
