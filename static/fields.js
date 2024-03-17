function validateForm(event) {
    event.preventDefault();


    const callNumber = document.getElementById('activeCallNumber').value;
    const whatsappNumber = document.getElementById('activeWhatsappNumber').value;

    if (!/^\d+$/.test(callNumber) || !/^\d+$/.test(whatsappNumber)) {
        alert("Please enter valid phone numbers.");
        return;
    }

    const formData = {
        name: document.getElementById('name').value,
        parts: document.getElementById('parts').value,
        program: document.getElementById('program').value,
        campusLocation: document.getElementById('campusLocation').value,
        hallOfResidence: document.getElementById('hallOfResidence').value,
        activeCallNumber: callNumber,
        activeWhatsappNumber: whatsappNumber,
        society: document.getElementById('society').value,
        circuit: document.getElementById('circuit').value,
        Diocese: document.getElementById('Diocese').value,
    };

    
    document.getElementById('choirForm').reset();

    alert("Form submitted successfully!");
    
}