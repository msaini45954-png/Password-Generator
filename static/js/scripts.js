let checkboxes = document.querySelectorAll('input[name="option"]');

checkboxes.forEach(cb => {
    cb.addEventListener('change', () => {
        let checkedCount = document.querySelectorAll('input[name="option"]:checked').length;

        if (checkedCount === 0) {
            cb.checked = true; // re-check it
            //alert("At least one checkbox must remain checked!");
        }
    });
});

let range = document.getElementById("myRange");
let output = document.getElementById("output");

// Show default value
output.textContent = range.value;

// Update value when slider moves
range.oninput = function () {
    output.textContent = this.value;
    // console.log(this.value); // check in console
};

function copyPassword() {
    const password = document.getElementById("pass").value;

    if (!password) {
        alert("No password to copy!");
        return;
    }

    navigator.clipboard.writeText(password)
        .then(() => alert("Copied!"))
        .catch(() => alert("Copy failed!"));
}

const copyButton = document.getElementById("copy_password");
copyButton.addEventListener("click", copyPassword);

const form = document.querySelector("form");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const generateButton = document.getElementById("generate");
    const passwordField = document.getElementById("pass");
    const strengthHeading = document.querySelector("#strength");

    generateButton.disabled = true;
    generateButton.textContent = "Generating...";

    try {
        const formData = new FormData(form);

        const response = await fetch(window.location.href, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        });

        if (!response.ok) {
            throw new Error("Password generation failed");
        }

        const data = await response.json();

        passwordField.value = data.new_password;

        if (data.strength) {
            strengthHeading.textContent = data.strength;
        }
    } catch (error) {
        console.error(error);
        alert("Something went wrong. Please try again.");
    } finally {
        generateButton.disabled = false;
        generateButton.textContent = "Generate";
    }
});

