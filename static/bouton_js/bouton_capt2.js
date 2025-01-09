document.addEventListener("DOMContentLoaded", function() { 
    // this function runs when the DOM is ready, i.e. when the document has been parsed
      var btn = document.querySelector(".Bouton_Capt2");
      //var txt = document.querySelector("p");
      
      btn.addEventListener("click", updateBtn);
      
      function updateBtn() {
        if (btn.value === "Off") {
          btn.value = "On";
          btn.style = "background-color: green;"
          //txt.textContent = "On";
        } else {
          btn.value = "Off";
          btn.style = "background-color: red;"
          //txt.textContent = "off";
        }
      }
  });