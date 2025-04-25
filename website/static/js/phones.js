class PhoneInputHandler {
  constructor() {
    this.initializeInputs();

  }

  initializeInputs() {
    document.addEventListener("DOMContentLoaded", () => {
      const input = document.querySelector("#telefone");
      window.intlTelInput(input, {
        initialCountry: "auto",
        geoIpLookup: callback => {
          fetch("https://ipapi.co/json")
            .then(response => response.json())
            .then(data => callback(data.country_code))
            .catch(() => callback("br"));
        },
        separateDialCode: true,
        fixDropdownWidth: true,
        loadUtils: () => import("https://cdn.jsdelivr.net/npm/intl-tel-input@25.3.1/build/js/utils.js"),
      });
    })
  }


}

const phones = new PhoneInputHandler();
