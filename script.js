async function loadEvents() {
    try {
        const response = await fetch('detected_events.json');
        const events = await response.json();
        const eventsDiv = document.getElementById('events');
        const totalEventsSpan = document.getElementById('total-events');
        const lastUpdatedSpan = document.getElementById('last-updated');

        eventsDiv.innerHTML = '';

        events.reverse().forEach(event => {
            const div = document.createElement('div');
            div.className = 'event';
            div.innerHTML = `
                <strong>File:</strong> ${event.filepath}<br>
                <strong>Time:</strong> ${event.timestamp}<br>
                <strong>Content:</strong> ${event.content}
            `;
            eventsDiv.appendChild(div);
        });

        totalEventsSpan.textContent = `Total Events: ${events.length}`;

        if (events.length > 0) {
            lastUpdatedSpan.textContent = `Last Updated: ${events[0].timestamp}`;
        } else {
            lastUpdatedSpan.textContent = `Last Updated: No events yet`;
        }
    } catch (error) {
        console.error('Error loading events:', error);
    }
}

// Auto-refresh every 5 seconds
setInterval(loadEvents, 5000);

// Initial load
window.onload = loadEvents;
