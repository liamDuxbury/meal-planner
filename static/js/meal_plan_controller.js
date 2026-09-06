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
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => { throw new Error(text); });
                }
                return response.text();
            })
            .then(html => this.render(html))
            .catch(error => alert(error.message));
    },

    render(html) {
        this.container.innerHTML = html;
    },
};