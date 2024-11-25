document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        const resultDiv = document.getElementById('result');
        if (response.ok) {
            resultDiv.innerHTML = `
                <div class="result-success">
                    <h3>Predicted Wine Quality</h3>
                    <p>${result.predicted_quality.toFixed(2)} / 8</p>
                </div>
            `;
        } else {
            resultDiv.innerHTML = `
                <div class="result-error">
                    <h3>Error</h3>
                    <p>${result.detail}</p>
                </div>
            `;
        }
    } catch (error) {
        document.getElementById('result').innerHTML = `
            <div class="result-error">
                <h3>Error</h3>
                <p>Something went wrong. Please try again.</p>
            </div>
        `;
    }
});

// Optional: Add sample data population
document.addEventListener('DOMContentLoaded', () => {
    const sampleData = {
        fixed_acidity: 7.4,
        volatile_acidity: 0.7,
        citric_acid: 0.2,
        residual_sugar: 2.1,
        chlorides: 0.076,
        free_sulfur_dioxide: 11.0,
        total_sulfur_dioxide: 34.0,
        density: 0.9978,
        ph: 3.51,
        sulphates: 0.56,
        alcohol: 9.4
    };

    const populateSampleBtn = document.createElement('button');
    populateSampleBtn.textContent = 'Fill Sample Data';
    populateSampleBtn.className = 'submit-btn';
    populateSampleBtn.style.marginBottom = '1rem';
    populateSampleBtn.style.backgroundColor = '#666';
    
    document.querySelector('form').insertBefore(populateSampleBtn, document.querySelector('.form-grid'));
    
    populateSampleBtn.addEventListener('click', (e) => {
        e.preventDefault();
        Object.keys(sampleData).forEach(key => {
            document.getElementById(key).value = sampleData[key];
        });
    });
}); 