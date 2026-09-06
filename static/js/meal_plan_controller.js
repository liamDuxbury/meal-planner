const MealPlanController = {
    init(generateUrl, containerId, buttonId, overrideExistingCheckboxId, cuisineFilterId) {
        this.generateUrl = generateUrl;
        this.container = document.getElementById(containerId);
        this.overrideExistingCheckbox = document.getElementById(overrideExistingCheckboxId);
        this.cuisineFilter = document.getElementById(cuisineFilterId);
        document.getElementById(buttonId).addEventListener('click', () => this.generate());
    },

    generate() {
        const overrideExisting = this.overrideExistingCheckbox.checked;
        const cuisines = Array.from(this.cuisineFilter.selectedOptions).map(option => option.value);

        fetch(this.generateUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ overrideExisting, cuisines }),
        })
            .then(response => response.text())
            .then(html => this.render(html))
            .catch(() => this.render('<p class="error">Could not reach the server. Check it is running and try again.</p>'));
    },

    render(html) {
        this.container.innerHTML = html;
    },
};