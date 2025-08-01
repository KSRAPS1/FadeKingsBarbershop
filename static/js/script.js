document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("booking-form");
    const successMessage = document.getElementById("successMessage");

    form.addEventListener("submit", (e) => {
        const name = form.name.value;
        const phone = form.phone.value;

        //Simple check: if name and phoneare too short to prevent submission
        if (name.length < 3 || phone.length < 10) {
            e.preventDefault(); // Prevent form submission
            alert("Please enter a valid name and phone number.");
            return;
        } else {
            successMessage.textContent = "Booking submitted successfully!"
        }
    });
});