document.addEventListener('DOMContentLoaded', function () {
    const numVariablesSelect = document.getElementById('numVariables');
    const numGenerationsSelect = document.getElementById('numGenerations');
    const populationSizeSelect = document.getElementById('populationSize');
    const xMinSelect = document.getElementById('xMin');
    const xMaxSelect = document.getElementById('xMax');
    const coefficientsContainer = document.getElementById('coefficientsContainer');
    const calculateButton = document.getElementById('calculateButton');
    const resultContainer = document.getElementById('resultContainer');

    // Listen for changes to the number of variables selection
    numVariablesSelect.addEventListener('change', function () {
        coefficientsContainer.innerHTML = '';
        const numVariables = parseInt(numVariablesSelect.value);
        const numGenerations = parseInt(numGenerationsSelect.value);
        const populationSize = parseInt(populationSizeSelect.value);
        const xMin = parseInt(xMinSelect.value);
        const xMax = parseInt(xMaxSelect.value);

        for (let i = 0; i <= numVariables; i++) {
            const div = document.createElement('div');
            div.className = 'input-group mb-3';

            const label = document.createElement('label');
            label.className = 'input-group-text';
            label.textContent = `Coefficient a${i}`;

            const input = document.createElement('input');
            input.type = 'number';
            input.name = `a${i}`;
            input.className = 'form-control';
            input.required = true;

            div.appendChild(label);
            div.appendChild(input);
            coefficientsContainer.appendChild(div);
        }
    });

    // Listen for calculate button click
    calculateButton.addEventListener('click', function () {
        const formData = new FormData(document.getElementById('polynomialForm'));

        fetch("/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                'X-Requested-With': 'XMLHttpRequest'  // Ensures Django recognizes it as AJAX
            },
            body: formData
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Server responded with status " + response.status);
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                resultContainer.classList.remove('d-none');
                resultContainer.innerHTML = `<strong>Best value of x:</strong> ${data.best_x.toFixed(2)}<br>
                                 <strong>Result of polynomial f(x):</strong> ${data.result.toFixed(2)}`;
            })
            .catch(error => {
                console.error("Error:", error);
                resultContainer.classList.remove('d-none');
                resultContainer.classList.add('alert-danger');
                resultContainer.innerHTML = `An error occurred: ${error.message}`;
            });
    });
});
