const MealPlanController = {
    init({ generateUrl, containerId, buttonId, overrideCheckboxId, cuisineToggleId, cuisineOptionsId }) {
        this.generateUrl = generateUrl;
        this.container = document.getElementById(containerId);
        this.overrideCheckbox = document.getElementById(overrideCheckboxId);
        this.cuisineToggle = document.getElementById(cuisineToggleId);
        this.cuisineOptions = document.getElementById(cuisineOptionsId);

        this.cuisineToggle.addEventListener('change', () => {
            this.cuisineOptions.disabled = !this.cuisineToggle.checked;
        });

        document.getElementById(buttonId).addEventListener('click', () => this.generate());
    },

    selectedCuisines() {
        if (!this.cuisineToggle.checked) {
            return [];
        }
        return Array.from(this.cuisineOptions.querySelectorAll('input:checked')).map(input => input.value);
    },

    generate() {
        fetch(this.generateUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                overrideExisting: this.overrideCheckbox.checked,
                cuisines: this.selectedCuisines(),
            }),
        })
            .then(response => response.text())
            .then(html => this.render(html))
            .catch(() => this.render('<p class="error">Could not reach the server. Check it is running and try again.</p>'));
    },

    render(html) {
        this.container.innerHTML = html;
    },
};
