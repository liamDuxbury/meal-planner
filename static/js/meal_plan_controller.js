const MealPlanController = {
    init(generateUrl, containerId, buttonId, overrideExistingCheckboxId) {
        this.generateUrl = generateUrl;
        this.container = document.getElementById(containerId);
        this.overrideExistingCheckbox = document.getElementById(overrideExistingCheckboxId);
        document.getElementById(buttonId).addEventListener('click', () => this.generate());
    },

    generate() {
        const overrideExisting = this.overrideExistingCheckbox.checked;

        fetch(this.generateUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ overrideExisting }),
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