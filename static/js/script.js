// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    const forms = {
        'summaryForm': '/summarize',
        'urlForm': '/summarize_url',
        'wikipediaForm': '/wikipedia_summary',
        'stockForm': '/stock_info',
        'sentimentForm': '/analyze_sentiment',
        'keywordForm': '/extract_keywords',
        'nerForm': '/named_entity_recognition',
        'translateForm': '/translate_text',
        'currencyForm': '/convert_currency',
        'readabilityForm': '/get_readability_score',
        'questionForm': '/generate_questions'
    };

    Object.keys(forms).forEach(formId => {
        document.getElementById(formId).addEventListener('submit', async function(event) {
            event.preventDefault();
            
            const formData = new FormData(this);
            const inputData = {};
            for (let [key, value] of formData.entries()) {
                inputData[key] = value.trim();
            }

            // Check if any input field is empty or only contains whitespace
            const emptyFields = Object.entries(inputData).filter(([key, value]) => value === '');
            if (emptyFields.length > 0) {
                alert(`Please enter a value for ${emptyFields.map(([key]) => key).join(', ')}.`);
                return;
            }

            document.getElementById('loader').classList.remove('hidden');
            document.getElementById('result').classList.add('hidden');

            try {
                const response = await fetch(forms[formId], {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(inputData)
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || `HTTP error! status: ${response.status}`);
                }

                // Update the UI with the response
                const resultElement = document.getElementById('resultText');
                if (data.summary) {
                    resultElement.textContent = data.summary;
                } else if (data.info) {
                    resultElement.textContent = data.info;
                } else if (data.sentiment) {
                    resultElement.textContent = `Sentiment: ${data.sentiment}`;
                } else if (data.keywords) {
                    resultElement.textContent = `Keywords: ${data.keywords.join(', ')}`;
                } else if (data.entities) {
                    resultElement.textContent = `Named Entities: ${JSON.stringify(data.entities)}`;
                } else if (data.translation) {
                    resultElement.textContent = `Translation: ${data.translation}`;
                } else if (data.conversion) {
                    resultElement.textContent = `Converted Amount: ${data.conversion}`;
                } else if (data.readability_score !== undefined) {
                    resultElement.textContent = `Readability Score: ${data.readability_score.toFixed(2)}`;
                } else if (data.questions) {
                    resultElement.textContent = `Generated Questions:\n${data.questions.join('\n')}`;
                } else {
                    resultElement.textContent = "No result was generated.";
                }

                document.getElementById('result').classList.remove('hidden');
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('resultText').textContent = `An error occurred: ${error.message}`;
                document.getElementById('result').classList.remove('hidden');
            } finally {
                document.getElementById('loader').classList.add('hidden');
            }
        });
    });

    document.getElementById('copyButton').addEventListener('click', function() {
        const resultText = document.getElementById('resultText').textContent;
        navigator.clipboard.writeText(resultText).then(() => {
            alert('Result copied to clipboard!');
        });
    });
});
