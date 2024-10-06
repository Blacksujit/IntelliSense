// static/js/script.js
document.getElementById('summaryForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const textInput = document.getElementById('textInput').value;

    // Send the text to the backend for summarization
    const response = await fetch('/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'text': textInput
        })
    });

    const data = await response.json();

    // Update the UI with the summary
    const summaryTextElement = document.getElementById('summaryText');
    if (data.summary) {
        summaryTextElement.textContent = data.summary;
    } else {
        summaryTextElement.textContent = "An error occurred.";
    }
});
