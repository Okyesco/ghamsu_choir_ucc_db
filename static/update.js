function submitForm() {
    const choirsterIDValue = document.getElementById('choirsterID').value;
    const userInputValue = document.getElementById('userInput').value;
    const dropdownValue = document.getElementById('dropdownMenu').value;

    alert(`Submitted:\nChoirster ID: ${choirsterIDValue}\nNew input: ${userInputValue}\nSelected Field: ${dropdownValue}`);
}
