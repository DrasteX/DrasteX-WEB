document.addEventListener('DOMContentLoaded', () => {
    // Select all add and remove buttons and number of items input fields
    const addItemButtons = document.querySelectorAll("#add_item");
    const removeItemButtons = document.querySelectorAll("#remove_item");
    const numberOfItemsInputs = document.querySelectorAll("#number_of_items");

    addItemButtons.forEach((button, index) => {
        button.addEventListener("click", () => {
            // Get the corresponding input field
            const input = numberOfItemsInputs[index];
            let currentValue = parseInt(input.value);
            if (!isNaN(currentValue)) {
                input.value = currentValue + 1;
            }
        });
    });

    removeItemButtons.forEach((button, index) => {
        button.addEventListener("click", () => {
            // Get the corresponding input field
            const input = numberOfItemsInputs[index];
            let currentValue = parseInt(input.value);
            if (!isNaN(currentValue) && currentValue > 0) {
                input.value = currentValue - 1;
            }
        });
    });


    
});
