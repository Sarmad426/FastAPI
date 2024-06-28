document.addEventListener('DOMContentLoaded', fetchTotalPoints);

async function fetchTotalPoints() {
    const url = 'http://127.0.0.1:8000/points/total';

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        document.getElementById('total-points').innerText = data.points;
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
}
