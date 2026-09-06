const MealPlanController = {
    init(generateUrl, containerId, buttonId) {
        this.generateUrl = generateUrl;
        this.container = document.getElementById(containerId);
        document.getElementById(buttonId).addEventListener('click', () => this.generate());
    },

    generate() {
        fetch(this.generateUrl, { method: 'POST' })
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