
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

document.getElementById('addCrimeButton').addEventListener('click', function() {
    const crimeContainer = document.querySelector('.grid-container-01');
    
    // إنشاء عناصر جديدة لرقم القضية
    const newChargeNumber = document.createElement('div');
    newChargeNumber.className = 'grid-item-01';
    newChargeNumber.innerHTML = '<input type="text" name="charge_number[]" placeholder="رقم القضية">';
    
    // إنشاء عناصر جديدة لسنة القضية
    const newChargeYear = document.createElement('div');
    newChargeYear.className = 'grid-item-01';
    newChargeYear.innerHTML = '<input type="text" name="charge_year[]" placeholder="سنة القضية">';
    
    // إنشاء عناصر جديدة لقسم الشرطة
    const newPoliceStation = document.createElement('div');
    newPoliceStation.className = 'grid-item-01';
    newPoliceStation.innerHTML = '<input type="text" name="police_station[]" placeholder="قسم/مركز الشرطة">';
    
    // إنشاء عناصر جديدة للجريمة والأسلوب
    const newCrimeMethod = document.createElement('div');
    newCrimeMethod.className = 'grid-item-01';
    newCrimeMethod.innerHTML = '<input type="text" name="crime_method[]" placeholder="الجريمة والأسلوب">';
    
    // إضافة العناصر الجديدة إلى الحاوية
    crimeContainer.appendChild(newChargeNumber);
    crimeContainer.appendChild(newChargeYear);
    crimeContainer.appendChild(newPoliceStation);
    crimeContainer.appendChild(newCrimeMethod);
});




// إضافة حقول جديدة للعلامات المميزة ورقم مكانها
document.getElementById('addSpecialSignButton').addEventListener('click', function() {
    const signContainer = document.querySelector('.special-sign');
    
    const newSign = document.createElement('div');
    newSign.className = 'special-sign-item';
    newSign.innerHTML = '<input type="text" name="distinctive_marks[]" placeholder="علامة مميزة">';
    
    const newPlaceNumber = document.createElement('div');
    newPlaceNumber.className = 'special-sign-item';
    newPlaceNumber.innerHTML = '<input type="text" name="place_number[]" placeholder="رقم مكانها">';
    
    signContainer.appendChild(newSign);
    signContainer.appendChild(newPlaceNumber);
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
