async function fetchGraphHTML() {
    try {
        const response = await fetch('http://localhost:5000/base-distribution');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const html = await response.text();
        setGraph(html)
    } catch (error) {
        console.error('Error fetching graph HTML:', error);
    }
}

function setGraph(html) {
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
}




async function handleSubmit(event) {
    event.preventDefault(); // Prevent the default form submission

    const messageTextarea = document.getElementById('message');
    const messageText = messageTextarea.value;

    try {
        const response = await fetch('http://localhost:5000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: messageText })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        document.getElementById('result').value = JSON.stringify(result, null, 2); // Display the result nicely in the result textarea

        setGraph(result.plot)
        const probabilityTableRow = document.querySelector('.tables-container table');
        if (probabilityTableRow) {
            probabilityTableRow.innerHTML = `
                <th>Probability</th>
                <th>${result.p}</th>
            `;
        } else {
            console.error('Probability table row not found');
        }

        const claimsTableBody = document.querySelector('.tables-container table:last-of-type tbody');
        if (claimsTableBody) {
            claimsTableBody.innerHTML = ''; // Clear previous entries

            result.claims.forEach(claim => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${claim.quote}</td>
                    <td>${claim.infrastructure}</td>
                    <td>${claim.judgement}</td>
                    <td>${claim.dimension}</td>
                    <td>${claim.valence}</td>
                `;
                claimsTableBody.appendChild(row);
            });
        } else {
            console.error('Claims table body not found');
        }


    } catch (error) {
        console.error('Error analyzing text:', error);
    }
}

// Call the function to fetch and display the graph once the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    fetchGraphHTML();

    const form = document.querySelector('form');
    form.addEventListener('submit', handleSubmit);
});
