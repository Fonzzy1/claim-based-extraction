async function fetchGraphHTML() {
    try {
        const response = await fetch('http://localhost:5000/base-distribution');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const html = await response.text();
        document.getElementById('graph-container').outerHTML = html;

        // Extract and run the script from the returned HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const scripts = doc.querySelectorAll('script');
        scripts.forEach(script => {
            const newScript = document.createElement('script');
            newScript.text = script.innerHTML;
            document.body.appendChild(newScript);
        });
    } catch (error) {
        console.error('Error fetching graph HTML:', error);
    }
}

// Call the function to fetch and display the graph once the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    fetchGraphHTML();
});
