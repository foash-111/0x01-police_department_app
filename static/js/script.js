
// Wait for the DOM to fully load
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("addPersonAndChargeForm");

    const responseMessage = document.getElementById("responseMessage");

    // Attach a submit event listener to the form
    form.addEventListener("submit", async function(event) {
        event.preventDefault(); // Prevent default form submission

        // Show loading indicator
        responseMessage.innerHTML = 'جاري الإضافة...';
        
        // Prepare form data
        let formData = new FormData(form);

        try {
            // Send AJAX POST request
            let response = await fetch("/add_person_and_charge", {
                method: "POST",
                body: formData
            });

            if (!response.ok) throw new Error('Network response was not ok');
            let data = await response.json();
            
            // Display the message from the server
            responseMessage.innerHTML = `${data.message}`;

            // Optionally, clear the form if the submission was successful
            if (data.message.includes("تمت إضافة البيانات والتهمة بنجاح")) {
                form.reset(); // Clear the form fields
            }
        } catch (error) {
            // Handle any errors
            responseMessage.innerHTML = `<p>حدث خطأ: ${error.message}</p>`;
        }
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("addManagerForm");
    const responseMessage = document.getElementById("responseMessage");

    // Attach a submit event listener to the form
    form.addEventListener("submit", async function(event) {
        event.preventDefault(); // Prevent default form submission

        // Show loading indicator
        responseMessage.innerHTML = 'جاري الإضافة...';
        
        // Prepare form data
        let formData = new FormData(form);

        try {
            // Send AJAX POST request
            let response = await fetch("/register_manager", {
                method: "POST",
                body: formData
            });

            if (!response.ok) throw new Error('المدير موجود بالفعل');
            let data = await response.json();
            
            // Display the message from the server
            responseMessage.innerHTML = `<p>${data.message}</p>`;

            // Optionally, clear the form if the submission was successful
            if (data.message.includes("تمت إضافة المدير بنجاح")) {
                form.reset(); // Clear the form fields
            }
        } catch (error) {
            // Handle any errors
            responseMessage.innerHTML = `<p>حدث خطأ: ${error.message}</p>`;
        }
    });
});
function goBack() {
    window.history.back();
}
