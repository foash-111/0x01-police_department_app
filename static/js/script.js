document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('addPersonAndChargeForm');
    const responseMessage = document.getElementById('responseMessage');

    // Prevent form submission on pressing the "Enter" key inside the form fields
    form.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    });

    let isSubmitting = false; // Flag to prevent multiple submissions

    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent default form submission

        // If the form is already being submitted, stop further action
        if (isSubmitting) return;

        // Validate form inputs
        const fullName = document.getElementById('name').value.trim();
        const nationalId = document.getElementById('id_number').value.trim();
        let valid = true; // Default to true, will change to false if validation fails

        // Name validation
        const nameError = document.getElementById('nameError');
        if (fullName.length < 3 || fullName.length > 60) {
            nameError.textContent = 'يجب أن يكون الاسم بين 3 و 60 حرفاً.';
            valid = false; // Invalidate the form
        } else {
            nameError.textContent = ''; // Clear error if valid
        }

        // National ID validation
        const idError = document.getElementById('idError');
        if (nationalId.length !== 14 && nationalId !== '') {
            idError.textContent = 'يجب أن يكون الرقم القومي 14 رقماً.';
            valid = false; // Invalidate the form
        } else {
            idError.textContent = ''; // Clear error if valid
        }

        // Age validation (optional check, assuming age is required)
        const age = document.getElementById('age').value.trim();
        const ageError = document.getElementById('ageError');
        if (age && (age < 1 || age > 120)) {
            ageError.textContent = 'يرجى إدخال سن صحيح بين 1 و 120.';
            valid = false; // Invalidate the form
        } else {
            ageError.textContent = ''; // Clear error if valid
        }

        // If the form is invalid, show error message in red and do not proceed
        if (!valid) {
            responseMessage.textContent = 'الرجاء تصحيح الأخطاء في النموذج قبل الإرسال.'; // Show error message
            setTimeout(() => {
                responseMessage.classList.remove('error-message');
                responseMessage.textContent = ''; // Show error message

            }, 5000); // 5000 milliseconds = 5 seconds
            responseMessage.classList.add('error-message'); // Add error-message class to show in red
            responseMessage.classList.remove('success-message'); // Remove success-message class, if any
            return; // Stop form submission
        }

        // Clear any previous error styles
        responseMessage.classList.remove('error-message');
        responseMessage.classList.remove('success-message');
        responseMessage.innerHTML = 'جاري الإضافة...'; // Show loading message
        isSubmitting = true; // Set the flag to prevent multiple submissions

        const formData = new FormData(form); // Collect form data

        try {
            // Perform AJAX request to the server
            const response = await fetch("/add_person_and_charge", {
                method: "POST",
                body: formData
            });

            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();

            // Display server's response message
            responseMessage.innerHTML = data.message;

            // If successful, display success message in blue
            if (data.message.includes("تمت إضافة البيانات بنجاح")) {
                responseMessage.classList.add('success-message'); // Add success-message class to show in blue
                responseMessage.classList.remove('error-message');
                form.reset(); // Clear form fields
            }
        } catch (error) {
            // Handle any errors and display an error message
            responseMessage.innerHTML = `حدث خطأ: ${error.message}`;
            responseMessage.classList.add('error-message'); // Add error-message class for red text
        } finally {
            // Reset the flag to allow future submissions
            isSubmitting = false;
        }
    });
});

// sdit
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('editPersonForm');
    const responseMessage = document.getElementById('responseMessage');

    // Prevent form submission on pressing the "Enter" key inside the form fields
    form.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    });

    let isSubmitting = false; // Flag to prevent multiple submissions

    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent default form submission

        // If the form is already being submitted, stop further action
        if (isSubmitting) return;

        // Validate form inputs
        const fullName = document.getElementById('name').value.trim();
        const nationalId = document.getElementById('id_number').value.trim();
        let valid = true; // Default to true, will change to false if validation fails

        // Name validation
        const nameError = document.getElementById('nameError');
        if (fullName.length < 3 || fullName.length > 60) {
            nameError.textContent = 'يجب أن يكون الاسم بين 3 و 60 حرفاً.';
            valid = false; // Invalidate the form
        } else {
            nameError.textContent = ''; // Clear error if valid
        }

        // National ID validation
        const idError = document.getElementById('idError');
        if (nationalId.length !== 14 && nationalId !== '') {
            idError.textContent = 'يجب أن يكون الرقم القومي 14 رقماً.';
            valid = false; // Invalidate the form
        } else {
            idError.textContent = ''; // Clear error if valid
        }

        // Age validation (optional check, assuming age is required)
        const age = document.getElementById('age').value.trim();
        const ageError = document.getElementById('ageError');
        if (age && (age < 1 || age > 120)) {
            ageError.textContent = 'يرجى إدخال سن صحيح بين 1 و 120.';
            valid = false; // Invalidate the form
        } else {
            ageError.textContent = ''; // Clear error if valid
        }

        // If the form is invalid, show error message in red and do not proceed
        if (!valid) {
            responseMessage.textContent = 'الرجاء تصحيح الأخطاء في النموذج قبل الإرسال.'; // Show error message
                setTimeout(() => {
                    responseMessage.classList.remove('error-message');
                }, 5000); // 5000 milliseconds = 5 seconds
            responseMessage.classList.add('error-message'); // Add error-message class to show in red
            responseMessage.classList.remove('success-message'); // Remove success-message class, if any
            return; // Stop form submission
        }

        // Clear any previous error styles
        responseMessage.classList.remove('error-message');
        responseMessage.classList.remove('success-message');
        responseMessage.innerHTML = 'جاري تعديل البيانات...'; // Show loading message
        isSubmitting = true; // Set the flag to prevent multiple submissions

        const formData = new FormData(form); // Collect form data

        try {
            // Perform AJAX request to the server
            const response = await fetch(`/edit_person_and_charge/${personId}`, {
                method: "POST",
                body: formData
            });

            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();

            // Display server's response message
            responseMessage.innerHTML = data.message;

            // If successful, display success message in blue
            if (data.message.includes("تم تعديل البيانات بنجاح")) {
                responseMessage.classList.add('success-message'); // Add success-message class to show in blue
                responseMessage.classList.remove('error-message');
            }
        } catch (error) {
            // Handle any errors and display an error message
            responseMessage.innerHTML = `حدث خطأ: ${error.message}`;
            responseMessage.classList.add('error-message'); // Add error-message class for red text
        } finally {
            // Reset the flag to allow future submissions
            isSubmitting = false;
        }
    });
});

// 

function goBack() {
    window.history.back();
}

document.getElementById('addCrimeButton').addEventListener('click', function () {
    const crimeContainer = document.querySelector('.grid-container-01');
    const errorMessage = document.getElementById('crimeErrorMessage');
    const yearErrorMessage = document.getElementById('yearErrorMessage');

    // Get the last set of inputs for validation
    const lastChargeNumber = document.querySelectorAll('input[name="charge_number[]"]');
    const lastChargeYear = document.querySelectorAll('input[name="charge_year[]"]');
    const lastCaseType = document.querySelectorAll('select[name="case_type[]"]');
    const lastPoliceStation = document.querySelectorAll('input[name="police_station[]"]');
    const lastCrimeMethod = document.querySelectorAll('textarea[name="crime_method[]"]');
    const lastJudgement = document.querySelectorAll('textarea[name="judgement[]"]');

    const isFilled = [
        lastChargeNumber[lastChargeNumber.length - 1]?.value,
        lastChargeYear[lastChargeYear.length - 1]?.value,
        lastCaseType[lastCaseType.length - 1]?.value,
        lastPoliceStation[lastPoliceStation.length - 1]?.value,
        lastCrimeMethod[lastCrimeMethod.length - 1]?.value,
        lastJudgement[lastJudgement.length - 1]?.value,
    ].every(value => value !== '');

    const currentYear = new Date().getFullYear();
    const chargYear = lastChargeYear[lastChargeYear.length - 1]?.value;
    if ((chargYear > currentYear || chargYear < 1800)) {
        yearErrorMessage.style.display = "block";
        // Hide the error message after 5 seconds
        setTimeout(() => {
            yearErrorMessage.style.display = "none";
        }, 5000);
    
    }
    else if (isFilled) {
        errorMessage.style.display = "none";

       

        // Create and append new crime fields
        const newChargeNumber = document.createElement('div');
        newChargeNumber.className = 'grid-item-01';
        newChargeNumber.innerHTML = '<input type="number" name="charge_number[]" >';

        const newChargeYear = document.createElement('div');
        newChargeYear.className = 'grid-item-01';
        newChargeYear.innerHTML = '<input type="number" name="charge_year[]" >';

        const newCaseType = document.createElement('div');
        newCaseType.className = 'grid-item-01';
        newCaseType.innerHTML = `
            <select name="case_type[]">
                <option value="جنح">جنح</option>
                <option value="اداري">إداري</option>
                <option value="جنايات">جنايات</option>
            </select>
        `;

        const newPoliceStation = document.createElement('div');
        newPoliceStation.className = 'grid-item-01';
        newPoliceStation.innerHTML = '<input type="text" name="police_station[]" >';

        const newCrimeMethod = document.createElement('div');
        newCrimeMethod.className = 'grid-item-01';
        newCrimeMethod.innerHTML = `
            <input name="crime_method[]"  class="crime_method"  id="crime_method" oninput="autoResize(this)">
        `;

        const newJudgement = document.createElement('div');
        newJudgement.className = 'grid-item-01';
        newJudgement.innerHTML = `
            <input name="judgement[]" class="judgement" id="judgement" oninput="autoResize(this)">
        `;

        // Append new fields to the container
        crimeContainer.appendChild(newChargeNumber);
        crimeContainer.appendChild(newChargeYear);
        crimeContainer.appendChild(newCaseType);
        crimeContainer.appendChild(newPoliceStation);
        crimeContainer.appendChild(newCrimeMethod);
        crimeContainer.appendChild(newJudgement);
    } else {
        errorMessage.style.display = "block";
        // Hide the error message after 5 seconds
        setTimeout(() => {
            errorMessage.style.display = "none";
        }, 5000);
    }
});

// Function to auto-resize textareas
function autoResize(textarea) {
    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";
}





// إضافة حقول جديدة للعلامات المميزة ورقم مكانها
document.getElementById('addSpecialSignButton').addEventListener('click', function() {
    const distinctiveMarksContainer = document.querySelector('.special-sign');
    const errorMessage = document.getElementById('errorMessage');

    const lastDistinctiveMark = document.querySelectorAll('input[name="distinctive_marks[]"]');
    const lastPlaceNumber = document.querySelectorAll('input[name="place_number[]"]');
    
    const lastMarkValue = lastDistinctiveMark[lastDistinctiveMark.length - 1].value;
    const lastPlaceValue = lastPlaceNumber[lastPlaceNumber.length - 1].value;
    
    if (lastMarkValue && lastPlaceValue) {
        errorMessage.style.display = "none";
        const newSign = document.createElement('div');
        newSign.className = 'grid-item special-sign-item';
        newSign.innerHTML = '<input type="text" name="distinctive_marks[]" placeholder="علامة مميزة">';
        
        const newPlaceNumber = document.createElement('div');
        newPlaceNumber.className = 'grid-item special-sign-item';
        newPlaceNumber.innerHTML = '<input type="number" name="place_number[]" placeholder="رقم مكانها">';
        
        distinctiveMarksContainer.appendChild(newSign);
        distinctiveMarksContainer.appendChild(newPlaceNumber);
    } else {
        errorMessage.style.display = "block";
         // Hide the error message after 5 seconds
         setTimeout(() => {
            errorMessage.style.display = "none";
        }, 5000); // 5000 milliseconds = 5 seconds
    }
});


$('#searchForm').on('submit', function(event) {
    event.preventDefault();

    const searchInput = $('#searchInput').val();

    $.ajax({
        type: 'POST',
        url: '/search_person',
        data: { 
            searchInput: searchInput,
        },
        success: function(response) {
            // تفريغ الجدول القديم
            $('#resultsTable tbody').empty();

            if (response.length > 0) {
                response.forEach(function(person) {
                    const address = person.address ? person.address : 'لا يوجد';
                    const caseNumber = person.case_number ? person.case_number : 'لا يوجد';
                    $('#resultsTable tbody').append(`
                        <tr>
                            <td><a href="/profile/${person.id}">${person.name}</a></td>
                            <td>${address}</td>
                            <td>${caseNumber}</td>
                        </tr>
                    `);
                });
                // عرض الـ pop-up
                $('#searchResultsPopup').css('display', 'block');
            } else {
                $('#resultsTable tbody').append('<tr><td colspan="3">لم يتم العثور على نتائج.</td></tr>');
                $('#searchResultsPopup').css('display', 'block');
            }
        },
        error: function(error) {
            console.log('Error:', error);
            $('#resultsTable tbody').append('<tr><td colspan="3">حدث خطأ أثناء البحث.</td></tr>');
            $('#searchResultsPopup').css('display', 'block');
        }
    });
});

// اغلاق الـ pop-up عند الضغط على زر الإغلاق
$('.close').on('click', function() {
    $('#searchResultsPopup').css('display', 'none');
});

// اغلاق الـ pop-up عند الضغط خارج النافذة
$(window).on('click', function(event) {
    if (event.target.id === 'searchResultsPopup') {
        $('#searchResultsPopup').css('display', 'none');
    }
});

//
// Wait for the DOM to fully load
document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/login_manager', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

       
    } catch (error) {
        // Handle unexpected errors
        const errorMessageDiv = document.getElementById('errorLogin');
        errorMessageDiv.innerText = 'حدث خطأ أثناء تسجيل الدخول. حاول مرة أخرى.';
        errorMessageDiv.style.display = 'block';
    }
});


    function toggleSpouseName() {
        var maritalStatus = document.getElementById("marital_status").value;
        var spouseNameField = document.getElementById("spouseNameField");
    
        if (maritalStatus !== "أعزب") {
            spouseNameField.style.display = "block";
        } else {
            spouseNameField.style.display = "none";
        }
    }
    